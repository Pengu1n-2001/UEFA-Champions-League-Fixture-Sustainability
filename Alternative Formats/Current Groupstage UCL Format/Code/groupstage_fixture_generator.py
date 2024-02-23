import csv

def read_teams(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def write_teams(file_path, teams, mode='a'):
    with open(file_path, mode=mode, newline='', encoding='utf-8') as file:
        fieldnames = ["home_team", "home_team_city", "away_team", "away_team_city", "group"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if mode == 'w':  # Write header only if in write mode
            writer.writeheader()
        for team in teams:
            writer.writerow(team)

def create_fixtures(group_csv, teams_csv):
    # Read group CSV file
    groups = read_teams(group_csv)

    # Read teams CSV file
    teams = read_teams(teams_csv)

    # Create a dictionary to store fixtures for each year
    year_fixtures = {}

    # Iterate through each unique combination of year and group
    for year, group, year_group_teams in group_by_year_group(groups):
        if year not in year_fixtures:
            year_fixtures[year] = []

        # Create fixtures for the current year and group
        for home_team in year_group_teams:
            city_home = get_team_city(home_team['team'], teams)

            # Get all other teams in the same year and group
            other_teams = [team for team in year_group_teams if team['team'] != home_team['team']]

            # Create fixtures against all other teams
            for away_team in other_teams:
                city_away = get_team_city(away_team['team'], teams)
                year_fixtures[year].append({
                    'home_team': home_team['team'],
                    'home_team_city': city_home,
                    'away_team': away_team['team'],
                    'away_team_city': city_away,
                    'group': group
                })

    # Write fixtures to CSV files for each year
    for year, fixtures in year_fixtures.items():
        output_file = f"../../../Alternative Formats/Current Groupstage UCL Format/Fixtures/202{year}_fixtures.csv"
        write_teams(output_file, fixtures, mode='w')


def group_by_year_group(groups):
    grouped = {}
    for group in groups:
        year_group = (group['year'], group['group'])
        if year_group not in grouped:
            grouped[year_group] = []
        grouped[year_group].append(group)
    for key, value in grouped.items():
        yield key[0], key[1], value

def get_team_city(team_name, teams):
    for team in teams:
        if team['team'] == team_name:
            return team['city']

group_stage_file_path = '../../../Alternative Formats/Current Groupstage UCL Format/Teams/groups.csv'
teams_file_path = '../../../Alternative Formats/Current Groupstage UCL Format/Teams/all_potential_teams.csv'

create_fixtures(group_stage_file_path, teams_file_path)