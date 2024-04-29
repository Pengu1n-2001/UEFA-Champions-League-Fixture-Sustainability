import csv
import random

def read_teams(file_path):
    """ Reads teams from a CSV file into a list of dictionaries. """
    with open(file_path, mode='r', encoding='utf-8') as file:
        return [row for row in csv.DictReader(file)]

def write_teams(file_path, teams, mode='w'):
    """ Writes a list of teams to a CSV file. """
    with open(file_path, mode=mode, newline='', encoding='utf-8') as file:
        fieldnames = ["team_name", "association", "uefa_coefficient", "city"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if mode == 'w':
            writer.writeheader()
        writer.writerows(teams)

# Toggle for sorting order: 0 for ascending (shortest distance first), 1 for descending (longest distance first)
sorting_order = 1

ranked_teams_path = '../../../../Teams/UEFA Coefficients/ranked_teams.csv'
input_file_path = '../../../../Teams/Qualification Rounds/Champions Path Round 2/champions_path_round_2_teams.csv'
output_file_path = '../../../../Teams/Qualification Rounds/Champions Path Round 3/champions_path_round_3_teams.csv'

# Load ranked teams and create a lookup for mean distance
ranked_teams = read_teams(ranked_teams_path)
ranked_dict = {team['team_name']: float(team['mean_distance']) for team in ranked_teams if 'mean_distance' in team}

# Load teams participating in the current round
teams = read_teams(input_file_path)
teams = [team for team in teams if team['team_name'] in ranked_dict]

# Handle bye if there is an odd number of teams
if len(teams) % 2 == 1:
    teams_sorted = sorted(teams, key=lambda x: ranked_dict[x['team_name']], reverse=bool(sorting_order))
    bye_team = teams_sorted.pop(0)  # Remove the team with the extreme mean distance based on toggle
    write_teams(output_file_path, [bye_team], mode='w')  # Write the bye team in write mode to start a new file
    teams = teams_sorted  # Remaining teams after the bye

# Randomize the order of teams for matchups
random.shuffle(teams)
matchups = [(teams[i], teams[i + 1]) for i in range(0, len(teams), 2)]

# Determine winners based on the ranked mean distance
winners = []
for team1, team2 in matchups:
    distance1 = ranked_dict[team1['team_name']]
    distance2 = ranked_dict[team2['team_name']]
    if (distance1 < distance2 and sorting_order == 0) or (distance1 > distance2 and sorting_order == 1):
        winners.append(team1)
    else:
        winners.append(team2)

# Append winners to the output file
write_teams(output_file_path, winners, mode='a')  # Append winners to the file with the bye team
