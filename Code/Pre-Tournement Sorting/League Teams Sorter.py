import csv
import os

# different file paths
coefficients_path = '../../Teams/UEFA Coefficients/UEFA_national_coefficient_ranking.csv'
league_winners_path = '../../Teams/League Stage/league_stage_teams.csv'
domestic_leagues_path = '../../Teams/Domestic Leagues'

# loads current UCL and UEL titleholders
ucl_winner_data = None
uel_winner_data = None
with open(league_winners_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if 'UEFA Champions League Winner' in row['status']:
            ucl_winner_data = row
        elif 'UEFA Europa League Winner' in row['status']:
            uel_winner_data = row

# loads UEFA Assocation coefficents, skipping excluded nations
associations = {}
with open(coefficients_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['status'].lower() != 'excluded':
            associations[row['association_code']] = int(row['rank'])

# creates a list of uefa associations
eligible_associations = {k: v for k, v in sorted(associations.items(), key=lambda item: item[1])}

# loads the league results for a given association
def load_league_results(association_code, path=domestic_leagues_path):
    league_results_path = os.path.join(path, f"{association_code}_league_results.csv")
    with open(league_results_path, mode='r', encoding='utf-8') as file:
        return list(csv.DictReader(file))

# data setup
league_stage_teams = []

# selects teams based on their league postions
def select_teams_by_position(association_code, position, count):
    teams = load_league_results(association_code)
    selected = [team for team in teams if int(team['rank']) == position][:count]
    league_stage_teams.extend(selected)

# selects teams based on the criteria for the different rounds
for code in eligible_associations.keys():
    rank = eligible_associations[code]
    if rank <= 4:
        select_teams_by_position(code, 4, 1) # selects 4th place from top 4 associations
    if rank <= 5:
        select_teams_by_position(code, 3, 1) # selects 3rd place from top 5 associations
    if rank <= 6:
        select_teams_by_position(code, 2, 1) # selects 2nd place from top 6 associations
    if rank <= 10:
        select_teams_by_position(code, 1, 1) # selects 1st palce from top 10 associations

# gives a 5th spot to the two highest assocations
top_two_associations = list(eligible_associations.keys())[:2]
for code in top_two_associations:
    select_teams_by_position(code, 5, 1)

# handles exceptional cases where the UCL/UEL teams have already qualified
def find_next_highest_team(teams, league_stage_team_names):
    teams_sorted = sorted(teams, key=lambda x: float(x['uefa_coefficient']), reverse=True)
    for team in teams_sorted:
        if team['team_name'] not in league_stage_team_names:
            return team
    return None

league_stage_team_names = [team['team_name'] for team in league_stage_teams]

# finds the next eligible team if the UCL titleholders are already qualified
if ucl_winner_data and ucl_winner_data['team_name'] in league_stage_team_names:
    for code in eligible_associations.keys():
        if eligible_associations[code] > 10:
            next_highest_team = find_next_highest_team(load_league_results(code), league_stage_team_names)
            if next_highest_team:
                league_stage_teams.append(next_highest_team)
                break

# finds the next eligible team if the UEL titleholders are already qualified
if uel_winner_data and uel_winner_data['team_name'] in league_stage_team_names:
    excluded_ranks = set(range(1, 5)).union(range(11, 15))
    for code, rank in eligible_associations.items():
        if rank not in excluded_ranks:
            next_highest_team = find_next_highest_team(load_league_results(code), league_stage_team_names)
            if next_highest_team:
                league_stage_teams.append(next_highest_team)
                break

# update league_stage_teams.csv with the selected teams
with open(league_winners_path, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['team_name', 'association', 'uefa_coefficient', 'city', 'status']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # writes UCL and UEL winners first
    if ucl_winner_data:
        writer.writerow({k: ucl_winner_data[k] for k in fieldnames if k in ucl_winner_data})
    if uel_winner_data:
        writer.writerow({k: uel_winner_data[k] for k in fieldnames if k in uel_winner_data})

    # writes the other qualified teams, ensuring no duplicates
    for team in league_stage_teams:
        if team['team_name'] not in [ucl_winner_data['team_name'], uel_winner_data['team_name']]:
            writer.writerow({k: team[k] for k in fieldnames if k in team})