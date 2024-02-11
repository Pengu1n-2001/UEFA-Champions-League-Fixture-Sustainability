import csv

def check_city_matching(teams_file, city_location_file):
    # Read city data
    with open(city_location_file, 'r', encoding='utf-8') as city_csv:
        city_reader = csv.reader(city_csv)
        cities_set = {row[0].lower() for row in city_reader}

    # Check cities in the teams file
    with open(teams_file, 'r', encoding='utf-8') as teams_csv:
        teams_reader = csv.DictReader(teams_csv)
        for team_row in teams_reader:
            team_city = team_row['city'].lower()
            if team_city not in cities_set:
                print(f"City not found in city_location_data.csv for team: {team_row}")

# Replace with your file paths
teams_file_path = '../../Teams/UEFA Coefficients/all_potential_teams.csv'
city_location_file_path = '../../Teams/UEFA Coefficients/city_location_data.csv'

check_city_matching(teams_file_path, city_location_file_path)
