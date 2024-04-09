import pandas as pd
import csv
import random
from ortools.sat.python import cp_model

# Function to read existing fixtures from CSV
def read_existing_fixtures(file_path):
    existing_fixtures = []
    with open(file_path, 'r', newline='', encoding='UTF-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            print("Row:", row)  # Print row for debugging
            existing_fixtures.append([row[1], row[5]])  # Extract team names
    return existing_fixtures
# makes sure teams additional info is included
df = pd.read_csv('../../Teams/League Stage/league_stage_teams_seeded_into_pots.csv')
teams = df['team_name'].tolist()
pots = df['pot'].tolist()
associations = df['association'].tolist()
coefficients = df['uefa_coefficient'].tolist()
cities = df['city'].tolist()
existing_fixtures = read_existing_fixtures('../../Fixtures, Tables and Results/League Stage/existing_league_stage_fixtures.csv')
team_additional_info = {team: {'coefficient': coeff, 'city': city, 'association': assoc}
                        for team, coeff, city, assoc in zip(teams, coefficients, cities, associations)}

num_teams = len(teams)

# number of teams and associations
num_teams = len(teams)
team_indices = {teams[i]: i for i in range(num_teams)}

# count teams per association
teams_per_association = {assoc: associations.count(assoc) for assoc in set(associations)}

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

    # constraint for same association matches
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

# Read existing fixtures
existing_fixtures = read_existing_fixtures('../../Fixtures, Tables and Results/League Stage/existing_league_stage_fixtures.csv')

# Initialize values
overall_fixtures = len(existing_fixtures)
team_count = 1

# Main loop to generate fixtures
while overall_fixtures < 143:
    current_team = teams[0]  # First team in the list
    fixture_count = 1

    while fixture_count <= 4:
        excluded = [current_team]
        fixture_validated = False

        while not fixture_validated:
            # Function to randomly select a team and update excluded list
            def team_selector(selected, excluded):
                random_team = random.choice(teams)
                while random_team in excluded:
                    random_team = random.choice(teams)
                excluded.append(random_team)
                with open('../../Fixtures, Tables and Results/League Stage/existing_league_stage_fixtures.csv', 'a', newline='', encoding='UTF-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([selected, random_team])  # Write fixture to existing fixtures
                return excluded

            excluded = team_selector(current_team, excluded)

            # Build and solve model
            model, match_vars = build_model(allow_intra_association=False, existing_fixtures=existing_fixtures)
            solver = cp_model.CpSolver()
            status = solver.Solve(model)

            # Check status and update fixtures
            if len(existing_fixtures) + len(read_existing_fixtures('../../Fixtures, Tables and Results/League Stage/existing_league_stage_fixtures.csv')) == 146:
                fixture_count += 1
                fixture_validated = True
            else:
                # Delete last entry in existing fixtures
                with open('../../Fixtures, Tables and Results/League Stage/existing_league_stage_fixtures.csv', 'r+', newline='', encoding='UTF-8') as f:
                    lines = f.readlines()
                    f.seek(0)
                    f.truncate()
                    f.writelines(lines[:-1])  # Remove last line

        team_count += 1
        overall_fixtures = len(existing_fixtures) + len(read_existing_fixtures('../../Fixtures, Tables and Results/League Stage/existing_league_stage_fixtures.csv'))

print("Fixtures generated successfully.")
