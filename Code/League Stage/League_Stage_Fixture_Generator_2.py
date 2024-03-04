import pandas as pd
import csv
from ortools.sat.python import cp_model
import random
# Read team data from CSV
df = pd.read_csv('../../Teams/League Stage/league_stage_teams_seeded_into_pots.csv')
teams = df['team_name'].tolist()
pots = df['pot'].tolist()
associations = df['association'].tolist()
coefficients = df['uefa_coefficient'].tolist()
cities = df['city'].tolist()

team_additional_info = {team: {'coefficient': coeff, 'city': city, 'association': assoc}
                        for team, coeff, city, assoc in zip(teams, coefficients, cities, associations)}

num_teams = len(teams)

# Count teams per association
teams_per_association = {assoc: associations.count(assoc) for assoc in set(associations)}

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
            # Ensure that there is exactly two games (one home, one away) against teams in this pot
            model.Add(sum(match_vars[team, opp] for opp in pot_teams if opp != team) == 1)
            model.Add(sum(match_vars[opp, team] for opp in pot_teams if opp != team) == 1)

    # Constraint for same association matches
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

    for i in range(num_teams):
        for j in range(i + 1, num_teams):
            model.Add(match_vars[i, j] + match_vars[j, i] <= 1)

    return model, match_vars

# Function to select viable fixture
def select_viable_fixture(team_index, used_fixtures, match_vars):
    viable_fixtures = []
    for opponent_index in range(num_teams):
        if opponent_index != team_index and (opponent_index, team_index) not in used_fixtures:
            if solver.Value(match_vars[team_index, opponent_index]) == 1:
                viable_fixtures.append(opponent_index)
    if viable_fixtures:
        return random.choice(viable_fixtures)
    else:
        return None

# Define OR-Tools model and solve
model, match_vars = build_model(allow_intra_association=False)
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Generate the fixture list
if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
    fixtures = []
    match_number = 1
    used_fixtures = set()
    for i in range(num_teams):
        for j in range(num_teams):
            if i != j and solver.Value(match_vars[i, j]) == 1:
                home_team_index = i
                away_team_index = select_viable_fixture(home_team_index, used_fixtures, match_vars)
                if away_team_index is not None:
                    used_fixtures.add((home_team_index, away_team_index))
                    used_fixtures.add((away_team_index, home_team_index))
                    home_team = teams[i]
                    away_team = teams[away_team_index]
                    fixtures.append([
                        match_number,
                        home_team, team_additional_info[home_team]['coefficient'], team_additional_info[home_team]['city'],
                        team_additional_info[home_team]['association'],
                        away_team, team_additional_info[away_team]['coefficient'], team_additional_info[away_team]['city'],
                        team_additional_info[away_team]['association']])
                    match_number += 1
    with open('../../Fixtures, Tables and Results/League Stage/league_stage_fixtures.csv', 'w', newline='', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(['match', 'home_team', 'home_team_coefficient', 'home_team_city', 'home_team_association',
                         'away_team', 'away_team_coefficient', 'away_team_city', 'away_team_association'])
        writer.writerows(fixtures)
else:
    print("No solution found.")
