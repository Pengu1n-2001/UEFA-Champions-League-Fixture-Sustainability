import csv
import random
import os

# reads the teams from the csv into a dictionary
def read_teams(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

# writes the teams into the selected csv file
def write_teams(file_path, teams, mode='a'):
    with open(file_path, mode=mode, newline='', encoding='utf-8') as file:
        fieldnames = ["team_name", "association", "uefa_coefficient", "city"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if mode == 'w':  # Write header only if in write mode
            writer.writeheader()
        for team in teams:
            writer.writerow(team)

# different file paths
input_file_path = '../../Teams/Qualification Rounds/League Path Play-off Round/league_path_play_off_round_teams.csv'
output_file_path = '../../Teams/League Stage/league_stage_teams.csv'

# read the teams from the input file
teams = read_teams(input_file_path)

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
write_teams(output_file_path, winners)

