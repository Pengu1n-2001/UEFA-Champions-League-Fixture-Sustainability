import csv
import random

# reads the teams from the csv into a dictionary
def read_teams(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

# writes the teams into the selected csv file
def write_teams(file_path, teams, mode='w'):
    with open(file_path, mode=mode, newline='', encoding='utf-8') as file:
        fieldnames = ["team_name", "association", "uefa_coefficient", "city"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if mode == 'w':  # Write header only if in write mode
            writer.writeheader()
        for team in teams:
            writer.writerow({k: v for k, v in team.items() if k in fieldnames})

# different file paths
input_file_path = '../../Teams/Qualification Rounds/Champions Path Round 1/champions_path_round_1_teams.csv'
output_file_path = '../../Teams/Qualification Rounds/Champions Path Round 2/champions_path_round_2_teams.csv'
coefficients_path = '../../Teams/UEFA Coefficients/UEFA_national_coefficient_ranking.csv'

# read the teams from the input file
teams = read_teams(input_file_path)

# reads the national uefa coefficients into a dictionary
association_coefficients = {}
with open(coefficients_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        association_coefficients[row['association_code']] = float(row['coefficient'])

# updates the teams using their uefa national coefficient
for team in teams:
    team['association_coefficient'] = association_coefficients.get(team['association'], 0)

# checks if there are an odd number of teams and handles a bye if needed
if len(teams) % 2 == 1:
    teams_by_association_coefficient = sorted(teams, key=lambda x: x['association_coefficient'], reverse=True)
    bye_team = teams_by_association_coefficient.pop(0)
    teams = [team for team in teams if team['team_name'] != bye_team['team_name']]
    write_teams(output_file_path, [bye_team], mode='a')

# puts the teams in a random order to generate randomised matchups
random.shuffle(teams)
matchups = [(teams[i], teams[i + 1]) for i in range(0, len(teams), 2)]

# finds the winners based on a weighted random selection based on UEFA Co-efficients
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

# writes the winners to the output csv
write_teams(output_file_path, winners, mode='a')


