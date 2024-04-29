import csv
import os

# different file paths
play_off_path = '../../Teams/Qualification Rounds/Champions Path Play-off Round/champions_path_play_off_round_teams.csv'
round_2_path = '../../Teams/Qualification Rounds/Champions Path Round 2/champions_path_round_2_teams.csv'
round_1_path = '../../Teams/Qualification Rounds/Champions Path Round 1/champions_path_round_1_teams.csv'
coefficients_path = '../../Teams/UEFA Coefficients/UEFA_national_coefficient_ranking.csv'


# reads the teams from the different csv files
def read_teams_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        return list(csv.DictReader(file))

# writes the teams back to their csv files
def write_teams_to_csv(teams, file_path):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=teams[0].keys())
        writer.writeheader()
        for team in teams:
            writer.writerow(team)

# loads the national assocation coefficents and creates a ranking
def load_coefficients(file_path):
    associations = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['status'].lower() != 'excluded': # skips over excluded nations
                associations[row['association_code']] = int(row['rank'])
    return associations

# moves a team into a different qualification round if needed
def move_team_by_rank(source_path, destination_path, associations, num_needed):
    source_teams = read_teams_from_csv(source_path)
    destination_teams = read_teams_from_csv(destination_path)
    source_teams.sort(key=lambda x: associations.get(x['association'], float('inf')))
    teams_moved = 0

    for team in source_teams:
        if teams_moved >= num_needed:
            break
        if associations.get(team['association'], 0) != float('inf'):
            destination_teams.append(team)
            source_teams.remove(team)
            teams_moved += 1

    # writes the team into the correct csv file for their round
    write_teams_to_csv(source_teams, source_path)
    write_teams_to_csv(destination_teams, destination_path)

# load the various assocation ranks
associations = load_coefficients(coefficients_path)

# make sure that the play-off round has the right amount of teams, and corrects if not
play_off_teams = read_teams_from_csv(play_off_path)
print(len(play_off_teams))
if len(play_off_teams) < 4:
    move_team_by_rank(round_2_path, play_off_path, associations, 4 - len(play_off_teams))

# make sure that round 2 has the right amount of teams, and corrects if not
round_2_teams = read_teams_from_csv(round_2_path)
if len(round_2_teams) < 9:
    move_team_by_rank(round_1_path, round_2_path, associations, 9 - len(round_2_teams))
