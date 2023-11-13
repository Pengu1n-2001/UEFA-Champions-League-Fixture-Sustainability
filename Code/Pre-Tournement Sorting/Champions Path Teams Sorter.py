import csv
import os

# File paths
coefficients_path = '../../Teams/UEFA Coefficients/UEFA_national_coefficient_ranking.csv'
league_stage_path = '../../Teams/League Stage/league_stage_teams.csv'
play_off_round_path = '../../Teams/Qualification Rounds/Champions Path Play-off Round/champions_path_play_off_round_teams.csv'
round_2_path = '../../Teams/Qualification Rounds/Champions Path Round 2/champions_path_round_2_teams.csv'
round_1_path = '../../Teams/Qualification Rounds/Champions Path Round 1/champions_path_round_1_teams.csv'
domestic_leagues_path = '../../Teams/Domestic Leagues'

# Load league stage teams
league_stage_teams = set()
with open(league_stage_path, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        league_stage_teams.add(row['team_name'])

# Function to write teams to CSV
def write_teams_to_csv(teams, file_path):
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['team_name', 'association', 'uefa_coefficient', 'city']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for team in teams:
            # Filter out keys not in fieldnames
            team_filtered = {k: team[k] for k in fieldnames if k in team}
            writer.writerow(team_filtered)

# Function to get the league winner if not in league stage teams
def get_league_winner_if_not_in_league_stage(associations, start_rank, end_rank, output_file, league_stage_teams):
    teams_to_write = []
    current_rank = start_rank
    for rank in range(start_rank, end_rank + 1):
        # Get the association code for the current rank
        code = next((code for code, assoc_rank in associations.items() if assoc_rank == current_rank), None)
        if code:
            league_results_path = os.path.join(domestic_leagues_path, f"{code}_league_results.csv")
            with open(league_results_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if int(row['rank']) == 1 and row['team_name'] not in league_stage_teams:
                        teams_to_write.append(row)
                        break
                else:
                    # If the champion is already in the league stage, treat the next association as the current one
                    end_rank += 1
        current_rank += 1
    write_teams_to_csv(teams_to_write, output_file)

# Load and filter UEFA coefficients, skipping excluded associations
associations = {}
with open(coefficients_path, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['status'].lower() != 'excluded':
            associations[row['association_code']] = int(row['rank'])

# Sorted associations based on coefficient
sorted_associations = {k: v for k, v in sorted(associations.items(), key=lambda item: item[1])}

# Process associations 11-14 for Play-off Round
get_league_winner_if_not_in_league_stage(sorted_associations, 11, 14, play_off_round_path, league_stage_teams)

# Process associations 15-24 for Round 2
get_league_winner_if_not_in_league_stage(sorted_associations, 15, 24, round_2_path, league_stage_teams)

# Process associations 25-55 for Round 1
get_league_winner_if_not_in_league_stage(sorted_associations, 25, 55, round_1_path, league_stage_teams)
