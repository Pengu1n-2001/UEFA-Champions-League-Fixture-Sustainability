import pandas as pd
import csv
from ortools.sat.python import cp_model
import random

# Function to read existing fixtures from CSV
def read_existing_fixtures(file_path):
    existing_fixtures = []
    with open(file_path, 'r', newline='', encoding='UTF-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            existing_fixtures.append([row[1], row[5]])  # Extract team names
    return existing_fixtures

# makes sure teams additional info is included
df = pd.read_csv('../../Teams/League Stage/league_stage_teams_seeded_into_pots.csv')
teams = df['team_name'].tolist()
pots = df['pot'].tolist()
associations = df['association'].tolist()
coefficients = df['uefa_coefficient'].tolist()
cities = df['city'].tolist()

team_additional_info = {team: {'association': assoc, 'uefa_coefficient': coeff, 'city': city}
                        for team, assoc, coeff, city in zip(teams, associations, coefficients, cities)}

num_teams = len(teams)

# function to build the constraint model
def build_model(allow_intra_association, existing_fixtures):
    model = cp_model.CpModel()

    # creating match variables
    match_vars = {}
    for i in range(num_teams):
        for j in range(num_teams):
            if i != j:
                match_vars[i, j] = model.NewBoolVar(f'match_{i}_{j}')

    # constraints for home and away games and matchups based on pots
    for team in range(num_teams):
        model.Add(sum(match_vars[team, opp] for opp in range(num_teams) if opp != team) == 4)  # Home games
        model.Add(sum(match_vars[opp, team] for opp in range(num_teams) if opp != team) == 4)  # Away games

    for pot in set(pots):
        pot_teams = [i for i in range(num_teams) if pots[i] == pot]
        for team in range(num_teams):
            # ensures that there is exactly two games (one home, one away) against teams in this pot
            model.Add(sum(match_vars[team, opp] for opp in pot_teams if opp != team) == 1)
            model.Add(sum(match_vars[opp, team] for opp in pot_teams if opp != team) == 1)

    # constraint for same association  matches
    if allow_intra_association:
        for assoc in teams_per_association:
            if teams_per_association[assoc] >= 4:
                for i in range(num_teams):
                    if associations[i] == assoc:
                        assoc_teams = [j for j in range(num_teams) if associations[j] == assoc and j != i]
                        model.Add(sum(match_vars[i, j] + match_vars[j, i] for j in assoc_teams) <= 1)
    else:
        for i in range(num_teams):
            for j in range(num_teams):
                if i != j and associations[i] == associations[j]:
                    model.Add(match_vars[i, j] == 0)

    # Apply constraints based on existing fixtures
    for fixture in existing_fixtures:
        home_index = teams.index(fixture[0])
        away_index = teams.index(fixture[1])
        model.Add(match_vars[home_index, away_index] == 1)

    for i in range(num_teams):
        for j in range(i + 1, num_teams):
            model.Add(match_vars[i, j] + match_vars[j, i] <= 1)

    return model, match_vars
# Function to select a team from the pot
def select_team(home_team, pot_number, excluded_teams):
    pot_teams = [team for team in teams if pots[teams.index(team)] == pot_number and team not in excluded_teams]
    # Randomly select a team from the pot that is not in excluded teams
    return random.choice(pot_teams)

# Read existing fixtures
existing_fixtures = read_existing_fixtures('../../Fixtures, Tables and Results/League Stage/league_stage_fixtures.csv')

# Build model and solve
model, match_vars = build_model(existing_fixtures)
solver = cp_model.CpSolver()

# Counter for home and away games
home_game_counter = {team: 0 for team in teams}
away_game_counter = {team: 0 for team in teams}

# Iterate through each team
for team_index, home_team in enumerate(teams):
    pot_number = 1
    while pot_number <= 4 and (home_game_counter[home_team] < 8 or away_game_counter[home_team] < 8):
        excluded_teams = []
        excluded_teams.append(home_team)  # Add home team to excluded teams
        away_team = select_team(home_team, pot_number, excluded_teams)

        # Check if home and away game counts exceed 8
        if home_game_counter[home_team] >= 8 or away_game_counter[away_team] >= 8:
            pot_number += 1
            continue

        # Add the selected fixture to the CSV and solve
        with open('../../Fixtures, Tables and Results/League Stage/league_stage_fixtures.csv', 'a', newline='', encoding='UTF-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                home_team,
                team_additional_info[home_team]['association'],
                team_additional_info[home_team]['uefa_coefficient'],
                team_additional_info[home_team]['city'],
                away_team,
                team_additional_info[away_team]['association'],
                team_additional_info[away_team]['uefa_coefficient'],
                team_additional_info[away_team]['city']
            ])

        status = solver.Solve(model)

        # If the solver finds a feasible solution, move to the next pot
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            home_game_counter[home_team] += 1
            away_game_counter[away_team] += 1
            pot_number += 1
        else:
            # If no feasible solution found, add the away team to excluded teams and retry
            excluded_teams.append(away_team)
            # Remove the last added fixture from CSV
            with open('../../Fixtures, Tables and Results/League Stage/league_stage_fixtures.csv', 'r+', newline='', encoding='UTF-8') as f:
                lines = f.readlines()
                f.truncate(0)
                f.seek(0)
                f.writelines(lines[:-1])  # Remove the last added fixture