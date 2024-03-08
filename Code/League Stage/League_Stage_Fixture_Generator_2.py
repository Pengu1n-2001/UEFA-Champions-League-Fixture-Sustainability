import pandas as pd
from ortools.sat.python import cp_model
import random
import csv
# Function for Fitness Proportionate Selection based on inverse distance
def fitness_proportionate_selection(distances):
    total_distance = sum(1/d for d in distances)
    threshold = random.uniform(0, total_distance)
    cumulative_sum = 0
    for idx, distance in enumerate(distances):
        cumulative_sum += 1/distance
        if cumulative_sum >= threshold:
            return idx
    return len(distances) - 1  # Return the last index if not selected

# Function to select fixtures based on distance
def select_fixtures_by_distance(match_vars, distances, selected_teams, intra_association_matches):
    chosen_team_idx = fitness_proportionate_selection(distances)
    while chosen_team_idx is not None:
        chosen_team = chosen_team_idx
        selected_teams.add(chosen_team)
        if len(selected_teams) == len(match_vars):
            break
        feasible_teams = []
        for idx in range(len(distances)):
            if idx not in selected_teams and not intra_association_matches[chosen_team][idx]:
                feasible_teams.append(idx)
        if not feasible_teams:
            break
        distances = [distances[idx] for idx in feasible_teams]
        chosen_team_idx = fitness_proportionate_selection(distances)
    return selected_teams

# Function to generate fixtures using distance-based selection
def generate_fixtures_with_distance(model, match_vars, allow_intra_association, distances):
    selected_teams = set()
    intra_association_matches = [[associations[i] == associations[j] for j in range(len(match_vars))] for i in range(len(match_vars))]
    selected_teams = select_fixtures_by_distance(match_vars, distances, selected_teams, intra_association_matches)
    for home_team in selected_teams:
        for away_team in selected_teams:
            if home_team != away_team:
                model.Add(match_vars[home_team, away_team] == 1)
    return model

# Read fixture data
fixtures_file_path = '../../Fixtures, Tables and Results/Fixtures for Distance Calculation/league_stage_and_poko_fixtures.csv'
df_fixtures = pd.read_csv(fixtures_file_path)

# Read distance matrix
distance_matrix_file_path = '../../Teams/UEFA Coefficients/distance_matrix.csv'
df_distance_matrix = pd.read_csv(distance_matrix_file_path)

# Extract cities and coordinates
cities = df_distance_matrix.columns[1:].tolist()
coordinates = {row[0].lower(): row[1:] for row in df_distance_matrix.values}

# Create distances for each fixture using the matrix
distances = []
for index, fixture in df_fixtures.iterrows():
    home_team = fixture['home_team_city'].lower()
    away_team = fixture['away_team_city'].lower()
    if home_team in coordinates and away_team in coordinates:
        home_idx = cities.index(home_team)
        away_idx = cities.index(away_team)
        distance = float(coordinates[home_team][away_idx])
        distances.append(distance)


# Makes sure teams additional info is included
df_teams = pd.read_csv('../../Teams/League Stage/league_stage_teams_seeded_into_pots.csv')
teams = df_teams['team_name'].tolist()
associations = df_teams['association'].tolist()
pots = df_teams['pot'].tolist()
num_teams = len(teams)

# Function to build the constraint model
def build_model(allow_intra_association):
    model = cp_model.CpModel()

    # Creating match variables
    match_vars = {}
    for i in range(num_teams):
        for j in range(num_teams):
            if i != j:
                match_vars[i, j] = model.NewBoolVar(f'match_{i}_{j}')

    # Constraints for home and away games and matchups based on pots
    for team in range(num_teams):
        model.Add(sum(match_vars[team, opp] for opp in range(num_teams) if opp != team) == 4)  # Home games
        model.Add(sum(match_vars[opp, team] for opp in range(num_teams) if opp != team) == 4)  # Away games

    for pot in set(pots):
        pot_teams = [i for i in range(num_teams) if pots[i] == pot]
        for team in range(num_teams):
            # ensures that there is exactly two games (one home, one away) against teams in this pot
            model.Add(sum(match_vars[team, opp] for opp in pot_teams if opp != team) == 1)
            model.Add(sum(match_vars[opp, team] for opp in pot_teams if opp != team) == 1)

    # Constraint for same association matches
    if allow_intra_association:
        for assoc in set(associations):
            assoc_teams = [i for i in range(num_teams) if associations[i] == assoc]
            for i in range(num_teams):
                if associations[i] == assoc:
                    model.Add(sum(match_vars[i, j] + match_vars[j, i] for j in assoc_teams) <= 1)
    else:
        for i in range(num_teams):
            for j in range(num_teams):
                if i != j and associations[i] == associations[j]:
                    model.Add(match_vars[i, j] == 0)

    # Constraint for one match between each pair of teams
    for i in range(num_teams):
        for j in range(i + 1, num_teams):
            model.Add(match_vars[i, j] + match_vars[j, i] <= 1)

    return model, match_vars

# Solve the model
model, match_vars = build_model(allow_intra_association=False)
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Attempt to solve the model with distance-based selection
if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
    model, match_vars = build_model(allow_intra_association=False)
    model = generate_fixtures_with_distance(model, match_vars, allow_intra_association=False, distances=distances)
    status = solver.Solve(model)

# If no solution is found, attempt again with intra-association matches allowed
if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
    model, match_vars = build_model(allow_intra_association=True)
    model = generate_fixtures_with_distance(model, match_vars, allow_intra_association=True, distances=distances)
    status = solver.Solve(model)

# Generating the fixture list
if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
    fixtures = []
    match_number = 1
    for i in range(num_teams):
        for j in range(num_teams):
            if i != j and solver.Value(match_vars[i, j]):
                home_team = teams[i]
                away_team = teams[j]
                fixtures.append([
                    match_number,
                    home_team, df_teams.loc[df_teams['team_name'] == home_team]['uefa_coefficient'].values[0],
                    df_teams.loc[df_teams['team_name'] == home_team]['city'].values[0],
                    df_teams.loc[df_teams['team_name'] == home_team]['association'].values[0],
                    away_team, df_teams.loc[df_teams['team_name'] == away_team]['uefa_coefficient'].values[0],
                    df_teams.loc[df_teams['team_name'] == away_team]['city'].values[0],
                    df_teams.loc[df_teams['team_name'] == away_team]['association'].values[0]
                ])
                match_number += 1
    with open('../../Fixtures, Tables and Results/League Stage/league_stage_fixtures.csv', 'w', newline='', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(['match', 'home_team', 'home_team_coefficient', 'home_team_city', 'home_team_association',
                         'away_team', 'away_team_coefficient', 'away_team_city', 'away_team_association'])
        writer.writerows(fixtures)
else:
    print("No solution found.")