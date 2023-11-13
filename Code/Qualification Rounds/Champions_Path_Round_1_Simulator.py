import csv
import random

# Function to read teams from a CSV file
def read_teams(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

# Function to write teams to a CSV file
def write_teams(file_path, teams, mode='w'):  # Default mode is 'w' to overwrite
    with open(file_path, mode=mode, newline='', encoding='utf-8') as file:
        fieldnames = ["team_name", "association", "uefa_coefficient", "city"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if mode == 'w':  # Write header only if in write mode
            writer.writeheader()
        for team in teams:
            writer.writerow({k: v for k, v in team.items() if k in fieldnames})

# Path to the CSV files
input_file_path = '../../Teams/Qualification Rounds/Champions Path Round 1/champions_path_round_1_teams.csv'
output_file_path = '../../Teams/Qualification Rounds/Champions Path Round 2/champions_path_round_2_teams.csv'
coefficients_path = '../../Teams/UEFA Coefficients/UEFA_national_coefficient_ranking.csv'

# Read the teams from the input file
teams = read_teams(input_file_path)

# Read association coefficients
association_coefficients = {}
with open(coefficients_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        association_coefficients[row['association_code']] = float(row['coefficient'])

# Update teams with their association's coefficient
for team in teams:
    team['association_coefficient'] = association_coefficients.get(team['association'], 0)

# Check if there is an odd number of teams and handle bye
if len(teams) % 2 == 1:
    teams_by_association_coefficient = sorted(teams, key=lambda x: x['association_coefficient'], reverse=True)
    bye_team = teams_by_association_coefficient.pop(0)  # Remove the top team for a bye
    # Remove the bye team from the teams list
    teams = [team for team in teams if team['team_name'] != bye_team['team_name']]
    write_teams(output_file_path, [bye_team], mode='a')  # Write the bye team to the next round's file

# Shuffle teams and create matchups
random.shuffle(teams)
matchups = [(teams[i], teams[i + 1]) for i in range(0, len(teams), 2)]

# Calculate winners
winners = []
for matchup in matchups:
    total_coefficient = sum(float(team['uefa_coefficient']) for team in matchup)
    random_num = random.uniform(0.001, total_coefficient)
    current_sum = 0
    for team in matchup:
        current_sum += float(team['uefa_coefficient'])
        if random_num <= current_sum:
            winners.append(team)
            break

# Write the winners to the output file
write_teams(output_file_path, winners, mode='a')

# Output matchup results
for matchup in matchups:
    team1_name = matchup[0]['team_name']
    team2_name = matchup[1]['team_name']
    print(f"{team1_name} v {team2_name}")
