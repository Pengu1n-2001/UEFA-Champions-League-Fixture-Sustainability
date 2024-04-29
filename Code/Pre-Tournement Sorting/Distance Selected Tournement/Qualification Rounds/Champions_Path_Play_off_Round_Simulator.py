import csv
import random

def read_teams(file_path):
    """ Reads teams from a CSV file into a list of dictionaries. """
    with open(file_path, mode='r', encoding='utf-8') as file:
        return [row for row in csv.DictReader(file)]

def write_teams(file_path, teams, mode='a'):
    """ Writes a list of teams to a CSV file. """
    with open(file_path, mode=mode, newline='', encoding='utf-8') as file:
        fieldnames = ["team_name", "association", "uefa_coefficient", "city"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if mode == 'w':  # Write header only if in write mode
            writer.writeheader()
        writer.writerows(teams)

# Toggle for sorting order: 0 for ascending, 1 for descending
sorting_order = 1

ranked_teams_path = '../../../../Teams/UEFA Coefficients/ranked_teams.csv'
input_file_path = '../../../../Teams/Qualification Rounds/Champions Path Play-off Round/champions_path_play_off_round_teams.csv'
output_file_path = '../../../../Teams/League Stage/league_stage_teams.csv'

# Load ranked teams and create a lookup dictionary
ranked_teams = read_teams(ranked_teams_path)
ranked_dict = {team['team_name']: float(team['mean_distance']) for team in ranked_teams}

# Load teams participating in the current round
teams = read_teams(input_file_path)
if len(teams) % 2 == 1:
    # Sort teams by mean distance to handle bye if there's an odd number
    teams_sorted = sorted(teams, key=lambda x: ranked_dict.get(x['team_name'], float('inf')), reverse=bool(sorting_order))
    bye_team = teams_sorted.pop(0)
    write_teams(output_file_path, [bye_team], mode='w')
    teams = teams_sorted

# Randomize team order and create matchups
random.shuffle(teams)
matchups = [(teams[i], teams[i + 1]) for i in range(0, len(teams), 2)]

# Determine winners based on the ranked mean distance
winners = []
for team1, team2 in matchups:
    distance1 = ranked_dict.get(team1['team_name'], float('inf'))
    distance2 = ranked_dict.get(team2['team_name'], float('inf'))
    if (distance1 < distance2 and sorting_order == 0) or (distance1 > distance2 and sorting_order == 1):
        winners.append(team1)
    else:
        winners.append(team2)

# Write the winners to the output CSV
write_teams(output_file_path, winners, mode='a')
