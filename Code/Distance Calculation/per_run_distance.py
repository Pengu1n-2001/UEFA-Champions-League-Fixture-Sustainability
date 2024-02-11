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

# Main program
team_stats_file = "../../Fixtures, Tables and Results/Stats/team_stats.csv"
fixtures_distances_file = "../../Fixtures, Tables and Results/Fixtures for Distance Calculation/league_stage_and_poko_fixtures_distances.csv"
output_file = "../../Fixtures, Tables and Results/Stats/run_distance_analysis.csv"

team_stats = read_csv_file(team_stats_file)
fixtures_distances = read_csv_file(fixtures_distances_file)

# Check the length of the output file to determine the value of 'run'
with open(output_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    rows = list(reader)
    if len(rows) > 0:
        run = int(rows[-1]['run']) + 1
    else:
        run = 1

# Calculate statistics
average_distance_per_team, average_distance_per_game, total_distance_travelled, longest_distance, fixture_with_longest_distance = calculate_statistics(team_stats, fixtures_distances)

# Prepare data for writing
new_entry = {
    'run': run,
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
fieldnames = ['run', 'average_distance_travelled_per_team', 'average_distance_travelled_per_game', 'total_distance_travelled', 'longest_distance_travelled_by_a_team', 'fixture_with_longest_distance']

# Write updated data back to CSV
write_csv_file(output_file, [new_entry], fieldnames)