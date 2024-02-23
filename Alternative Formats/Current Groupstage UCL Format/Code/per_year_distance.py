import csv
import os

# Function to read CSV file
def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Function to write CSV file
def write_csv_file(file_path, data, headers):
    file_exists = os.path.exists(file_path)
    with open(file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)

# Function to calculate statistics
def calculate_statistics(team_stats, fixtures_distances):
    # Calculate average distance travelled per team
    total_distance_travelled = sum(float(row['total_distance_travelled']) for row in team_stats)
    if len(team_stats) == 0:
        average_distance_per_team = 0
    else:
        average_distance_per_team = total_distance_travelled / len(team_stats)

    # Calculate average distance travelled per game
    total_avg_distance_per_game = sum(float(row['average_distance_travelled_per_away_game']) for row in team_stats)
    average_distance_per_game = total_avg_distance_per_game / len(team_stats)

    # Find longest distance travelled by a team
    max_distance_team = max(team_stats, key=lambda x: float(x['total_distance_travelled']))
    longest_distance = max_distance_team['team'] + " - " + max_distance_team['total_distance_travelled']

    # Find fixture with longest distance
    max_distance_fixture = max(fixtures_distances, key=lambda x: float(x['distance']))
    fixture_with_longest_distance = f"{max_distance_fixture['home_team']} ({max_distance_fixture['home_team_city']}) v {max_distance_fixture['away_team']} ({max_distance_fixture['away_team_city']}) - {max_distance_fixture['distance']}"

    return round(average_distance_per_team), round(average_distance_per_game), round(total_distance_travelled), longest_distance, fixture_with_longest_distance

# Function to run the analysis for different team stats files
def year_analysis(team_stats_file, fixtures_distances_file, output_file):
    team_stats = read_csv_file(team_stats_file)
    fixtures_distances = read_csv_file(fixtures_distances_file)

    # Extract the year from the team_stats_file name
    year = team_stats_file[-8:-4]

    # Calculate statistics
    average_distance_per_team, average_distance_per_game, total_distance_travelled, longest_distance, fixture_with_longest_distance = calculate_statistics(team_stats, fixtures_distances)

    # Prepare data for writing
    new_entry = {
        'year': year,
        'average_distance_travelled_per_team': average_distance_per_team,
        'average_distance_travelled_per_game': average_distance_per_game,
        'total_distance_travelled': total_distance_travelled,
        'longest_distance_travelled_by_a_team': longest_distance,
        'fixture_with_longest_distance': fixture_with_longest_distance
    }

    # Round numerical values to the nearest integer
    for key, value in new_entry.items():
        if isinstance(value, float):
            new_entry[key] = round(value)

    # Specify the fieldnames for writing
    fieldnames = ['year', 'average_distance_travelled_per_team', 'average_distance_travelled_per_game', 'total_distance_travelled', 'longest_distance_travelled_by_a_team', 'fixture_with_longest_distance']

    # Write updated data back to CSV
    write_csv_file(output_file, [new_entry], fieldnames)

def calculate_means_and_longest_entries(teams):
    # Calculate means
    total_entries = len(teams)
    mean_average_distance_per_team = sum(float(team['average_distance_travelled_per_team']) for team in teams) / total_entries
    mean_average_distance_per_game = sum(float(team['average_distance_travelled_per_game']) for team in teams) / total_entries
    mean_total_distance_travelled = sum(float(team['total_distance_travelled']) for team in teams) / total_entries

    # Find the entry with the longest distance travelled by a team
    longest_distance_entry = max(teams, key=lambda x: float(x['longest_distance_travelled_by_a_team'].split(" - ")[-1]))

    # Find the entry with the longest distance fixture
    longest_fixture_entry = max(teams, key=lambda x: float(x['fixture_with_longest_distance'].split(" - ")[-1]))

    return {
        'year': 'Total',
        'average_distance_travelled_per_team': mean_average_distance_per_team,
        'average_distance_travelled_per_game': mean_average_distance_per_game,
        'total_distance_travelled': mean_total_distance_travelled,
        'longest_distance_travelled_by_a_team': longest_distance_entry['longest_distance_travelled_by_a_team'],
        'fixture_with_longest_distance': longest_fixture_entry['fixture_with_longest_distance']
    }


# Example usage:
team_stats_file_2021 = "../../../Alternative Formats/Current Groupstage UCL Format/Teams/team_stats_2021.csv"
team_stats_file_2022 = "../../../Alternative Formats/Current Groupstage UCL Format/Teams/team_stats_2022.csv"
team_stats_file_2023 = "../../../Alternative Formats/Current Groupstage UCL Format/Teams/team_stats_2023.csv"
fixtures_distances_file_2021 = "../../../Alternative Formats/Current Groupstage UCL Format/Distances/2021_distances.csv"
fixtures_distances_file_2022 = "../../../Alternative Formats/Current Groupstage UCL Format/Distances/2022_distances.csv"
fixtures_distances_file_2023 = "../../../Alternative Formats/Current Groupstage UCL Format/Distances/2023_distances.csv"
output_file = "../../../Alternative Formats/Current Groupstage UCL Format/Stats/year_distance_analysis.csv"

year_analysis(team_stats_file_2021, fixtures_distances_file_2021, output_file)
year_analysis(team_stats_file_2022, fixtures_distances_file_2022, output_file)
year_analysis(team_stats_file_2023, fixtures_distances_file_2023, output_file)

# Read the CSV file
teams = read_csv_file(output_file)

# Calculate means and find longest entries
total_entry = calculate_means_and_longest_entries(teams)

# Write the calculated entry to a new CSV
write_csv_file(output_file, [total_entry], headers=["year", "average_distance_travelled_per_team", "average_distance_travelled_per_game", "total_distance_travelled", "longest_distance_travelled_by_a_team", "fixture_with_longest_distance"])
