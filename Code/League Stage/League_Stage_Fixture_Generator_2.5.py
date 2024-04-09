import pandas as pd
import csv
import random
from ortools.sat.python import cp_model

def clear_csv_except_header(file_path):
    # Read header
    with open(file_path, 'r', newline='', encoding='UTF-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)

    # Truncate the file
    with open(file_path, 'w', newline='', encoding='UTF-8') as file:
        file.truncate(0)  # Truncate the file content

    # Write back the header
    with open(file_path, 'a', newline='', encoding='UTF-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)

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

team_additional_info = {team: {'coefficient': coeff, 'city': city, 'association': assoc}
                        for team, coeff, city, assoc in zip(teams, coefficients, cities, associations)}

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

def run_model():
    # Read existing fixtures
    existing_fixtures = read_existing_fixtures('../../Fixtures, Tables and Results/League Stage/league_stage_fixtures.csv')

    # Build model and solve
    model, match_vars = build_model(allow_intra_association=False, existing_fixtures=existing_fixtures)
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # generating the updated fixture list
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        fixtures = []
        match_number = len(existing_fixtures) + 1  # Start with the next match number
        for i in range(num_teams):
            for j in range(num_teams):
                if i != j and solver.Value(match_vars[i, j]) and ([teams[i], teams[j]] not in existing_fixtures):
                    home_team = teams[i]
                    away_team = teams[j]
                    fixtures.append([
                        match_number,
                        home_team, team_additional_info[home_team]['coefficient'], team_additional_info[home_team]['city'],
                        team_additional_info[home_team]['association'],
                        away_team, team_additional_info[away_team]['coefficient'], team_additional_info[away_team]['city'],
                        team_additional_info[away_team]['association']])
                    match_number += 1

        with open('../../Fixtures, Tables and Results/League Stage/league_stage_fixtures.csv', 'a', newline='', encoding='UTF-8') as f:
            writer = csv.writer(f)
            writer.writerows(fixtures)
            writer.writerows("")
    #else:
        #print("No solution found.")


def team_selector(selected, excluded):
    opponent_team = random.choice(teams)
    while opponent_team in excluded:
        opponent_team = random.choice(teams)
    excluded.append(opponent_team)
    #print(opponent_team)
    home_team = selected
    away_team = opponent_team
    match_number = len(read_existing_fixtures('../../Fixtures, Tables and Results/League Stage/existing_league_stage_fixtures.csv'))+ 1
    # Write fixture to existing fixtures
    with open('../../Fixtures, Tables and Results/League Stage/existing_league_stage_fixtures.csv', 'a', newline='',
              encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            match_number,
            home_team, team_additional_info[home_team]['coefficient'], team_additional_info[home_team]['city'],
             team_additional_info[home_team]['association'],
             away_team, team_additional_info[away_team]['coefficient'], team_additional_info[away_team]['city'],
             team_additional_info[away_team]['association']])

    return excluded


clear_csv_except_header('../../Fixtures, Tables and Results/League Stage/existing_league_stage_fixtures.csv')
clear_csv_except_header('../../Fixtures, Tables and Results/League Stage/league_stage_fixtures.csv')
current_fixtures = read_existing_fixtures('../../Fixtures, Tables and Results/League Stage/league_stage_fixtures.csv')
# Initialize values
overall_fixtures = 0
team_count = 0

# Main loop to generate fixtures
while overall_fixtures < 143:
    current_team = teams[team_count]  # First team in the list
    fixture_count = 1

    while fixture_count <= 4:
        excluded = [current_team]
        fixture_validated = False

        while not fixture_validated:
            # Function to randomly select a team and update excluded list
            excluded = team_selector(current_team, excluded)
            with open('../../Fixtures, Tables and Results/League Stage/existing_league_stage_fixtures.csv', 'r') as source_file:
                with open('../../Fixtures, Tables and Results/League Stage/league_stage_fixtures.csv', 'w') as destination_file:
                    for line in source_file:
                        destination_file.write(line)
            run_model()

            current_fixtures = read_existing_fixtures('../../Fixtures, Tables and Results/League Stage/league_stage_fixtures.csv')
            # Check status and update fixtures
            if len(current_fixtures) == 144:
                fixture_count += 1
                #print("Validated")
                fixture_validated = True
            else:
                # Delete last entry in existing fixtures
                with open('../../Fixtures, Tables and Results/League Stage/existing_league_stage_fixtures.csv', 'r+', newline='', encoding='UTF-8') as f:
                    lines = f.readlines()
                    f.seek(0)
                    f.truncate()
                    f.writelines(lines[:-1])  # Remove last line
                    #print("Unvalidated")
        overall_fixtures = len(read_existing_fixtures('../../Fixtures, Tables and Results/League Stage/existing_league_stage_fixtures.csv'))
        print(overall_fixtures)
    team_count += 1

print("Fixtures generated successfully.")
with open('../../Fixtures, Tables and Results/League Stage/league_stage_fixtures.csv', 'r+', newline='',
          encoding='UTF-8') as f:
    lines = f.readlines()
    f.seek(0)
    f.truncate()
    f.writelines(lines[:-1])  # Remove last line
run_model()