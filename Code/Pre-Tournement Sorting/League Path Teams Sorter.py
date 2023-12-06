import csv
import os

# different file paths
coefficients_path = '../../Teams/UEFA Coefficients/UEFA_national_coefficient_ranking.csv'
league_stage_path = '../../Teams/League Stage/league_stage_teams.csv'
domestic_leagues_path = '../../Teams/Domestic Leagues'
league_path_round_3 = '../../Teams/Qualification Rounds/League Path Round 3/league_path_round_3_teams.csv'
league_path_round_2 = '../../Teams/Qualification Rounds/League Path Round 2/league_path_round_2_teams.csv'

# loads UEFA Assocation coefficents, skipping excluded nations
def load_filtered_coefficients(coefficients_file):
    with open(coefficients_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return {
            row['association_code']: int(row['rank'])
            for row in reader if row['status'].lower() != 'excluded'
        }

# loads teams that are already in the league stage
def load_league_stage_teams(league_stage_file):
    with open(league_stage_file, mode='r', encoding='utf-8') as file:
        return {row['team_name'] for row in csv.DictReader(file)}

# loads the league results for a given association
def load_league_results(association_code, path=domestic_leagues_path):
    league_results_path = os.path.join(path, f"{association_code}_league_results.csv")
    if os.path.exists(league_results_path):
        with open(league_results_path, mode='r', encoding='utf-8') as file:
            return list(csv.DictReader(file))
    else:
        return []

# finds the next eligible team
def get_next_eligible_team(association_rank, position, excluded_teams, associations):
    for rank in range(association_rank, len(associations) + 1):
        code = [code for code, assoc_rank in associations.items() if assoc_rank == rank][0]
        teams = load_league_results(code)
        for team in teams:
            if int(team['rank']) == position and team['team_name'] not in excluded_teams:
                return team
    return None

# writes the selected team to the csv
def write_teams_to_csv(teams, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['team_name', 'association', 'uefa_coefficient', 'city']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for team in teams:
            if team:  # makes sure there is actually a team to write
                filtered_team = {k: team[k] for k in fieldnames if k in team}
                writer.writerow(filtered_team)

# data setup
associations = load_filtered_coefficients(coefficients_path)
league_stage_teams = load_league_stage_teams(league_stage_path)
selected_teams_round_3 = []
selected_teams_round_2 = []

# finds teams for round 3
selected_teams_round_3.append(get_next_eligible_team(5, 4, league_stage_teams, associations))
selected_teams_round_3.append(get_next_eligible_team(6, 3, league_stage_teams, associations))
for rank in range(7, 10):
    team = get_next_eligible_team(rank, 2, league_stage_teams, associations)
    if team:
        selected_teams_round_3.append(team)

# finds teams for round 2
for rank in range(10, 16):
    team = get_next_eligible_team(rank, 2, league_stage_teams, associations)
    if team:
        selected_teams_round_2.append(team)

# outputs the results to csv files
write_teams_to_csv(selected_teams_round_3, league_path_round_3)
write_teams_to_csv(selected_teams_round_2, league_path_round_2)

