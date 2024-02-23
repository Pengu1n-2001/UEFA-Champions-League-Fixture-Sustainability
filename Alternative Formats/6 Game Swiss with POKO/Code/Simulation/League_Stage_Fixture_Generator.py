import pandas as pd
import csv
from ortools.sat.python import cp_model

# makes sure teams additional info is included
df = pd.read_csv('../../Teams/league_stage_teams_seeded_into_pots.csv')
teams = df['team_name'].tolist()
pots = df['pot'].tolist()
associations = df['association'].tolist()
coefficients = df['uefa_coefficient'].tolist()
cities = df['city'].tolist()

team_additional_info = {team: {'coefficient': coeff, 'city': city, 'association': assoc}
    for team, coeff, city, assoc in zip(teams, coefficients, cities, associations)}

num_teams = len(teams)

# number of teams and associations
num_teams = len(teams)
team_indices = {teams[i]: i for i in range(num_teams)}

# count teams per association
teams_per_association = {assoc: associations.count(assoc) for assoc in set(associations)}

# function to build the constraint model
def build_model(allow_intra_association):
    model = cp_model.CpModel()

    # creating match variables
    match_vars = {}
    for i in range(num_teams):
        for j in range(num_teams):
            if i != j:
                match_vars[i, j] = model.NewBoolVar(f'match_{i}_{j}')

    # constraints for home and away games and matchups based on pots
    for team in range(num_teams):
        model.Add(sum(match_vars[team, opp] for opp in range(num_teams) if opp != team) == 3)  # Home games
        model.Add(sum(match_vars[opp, team] for opp in range(num_teams) if opp != team) == 3)  # Away games

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

    for i in range(num_teams):
        for j in range(i + 1, num_teams):
            model.Add(match_vars[i, j] + match_vars[j, i] <= 1)

    return model, match_vars

# first attempt without same association matches
model, match_vars = build_model(allow_intra_association=False)
solver = cp_model.CpSolver()
status = solver.Solve(model)

# second attempt with conditional same association matches, if necessary
if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
    model, match_vars = build_model(allow_intra_association=True)
    status = solver.Solve(model)

# generating the fixture list
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
                    home_team, team_additional_info[home_team]['coefficient'], team_additional_info[home_team]['city'],
                    team_additional_info[home_team]['association'],
                    away_team, team_additional_info[away_team]['coefficient'], team_additional_info[away_team]['city'],
                    team_additional_info[away_team]['association']])
                match_number += 1
    with open('../../Fixtures/league_stage_fixtures.csv', 'w', newline='', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(['match', 'home_team', 'home_team_coefficient', 'home_team_city', 'home_team_association',
                         'away_team', 'away_team_coefficient', 'away_team_city', 'away_team_association'])
        writer.writerows(fixtures)
else:
    print("No solution found.")
