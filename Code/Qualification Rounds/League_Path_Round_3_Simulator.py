import csv
import random
import os

# Function to read teams from a CSV file
def read_teams(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

# Function to write teams to a CSV file
def write_teams(file_path, teams, mode='a'):  # Default mode is 'a' to append
    with open(file_path, mode=mode, newline='', encoding='utf-8') as file:
        fieldnames = ["team_name", "association", "uefa_coefficient", "city"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if mode == 'w':  # Write header only if in write mode
            writer.writeheader()
        for team in teams:
            writer.writerow(team)

# Path to the CSV files
input_file_path = '../../Teams/Qualification Rounds/League Path Round 3/league_path_round_3_teams.csv'
output_file_path = '../../Teams/Qualification Rounds/League Path Play-off Round/league_path_play_off_round_teams.csv'

# Read the teams from the input file
teams = read_teams(input_file_path)

# Check if there is an odd number of teams and handle bye
if len(teams) % 2 == 1:
    teams_by_coefficient = sorted(teams, key=lambda x: float(x['uefa_coefficient']), reverse=True)
    bye_team = teams_by_coefficient.pop(0)  # Remove the top team for a bye
    # Write the bye team directly to the output file
    write_teams(output_file_path, [bye_team])

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
write_teams(output_file_path, winners)

