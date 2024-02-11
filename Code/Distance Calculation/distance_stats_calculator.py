import csv
from collections import defaultdict


def calculate_team_stats(input_file, output_file):
    # Read fixture data
    with open(input_file, 'r', encoding='utf-8') as fixture_csv:
        fixtures = list(csv.reader(fixture_csv))

    # Initialize team stats dictionary
    team_stats = defaultdict(lambda: defaultdict(int))

    # Process each fixture
    for fixture in fixtures[1:]:  # Assuming the header is present
        home_team = fixture[0]
        away_team = fixture[2]
        double_legged_status = int(fixture[4]) if fixture[4] else 0  # Convert to integer, default to 0 if empty
        distance = round(float(fixture[5]))  # Round to the nearest whole number

        # Update away team's stats
        team_stats[away_team][f'game_{team_stats[away_team]["games_travelled_to"] + 1}'] += distance
        team_stats[away_team]['games_travelled_to'] += 1

        # Handle double-legged fixtures
        if double_legged_status == 1:
            # Update home team's stats for the second leg
            team_stats[home_team][f'game_{team_stats[home_team]["games_travelled_to"] + 1}'] += distance
            team_stats[home_team]['games_travelled_to'] += 1
        else:
            # Update home team's stats
            team_stats[home_team][f'game_{team_stats[home_team]["games_travelled_to"] + 1}'] += 0
            team_stats[home_team]['games_travelled_to'] += 1

    # Calculate average distance and create CSV data
    csv_data = [['team'] + [f'game_{i}' for i in range(1, 11)] + ['average_distance_travelled_per_away_game',
                                                                  'total_distance_travelled']]

    for team in team_stats:
        total_distance = sum(team_stats[team][f'game_{i}'] for i in range(1, 11))
        games = [team_stats[team][f'game_{i}'] for i in range(1, 11)]

        if any(map(lambda x: x > 0, games[-2:])):
            # The team played a double-legged fixture
            average_distance_travelled = round(total_distance / 5) if team_stats[team]['games_travelled_to'] > 0 else 0
        else:
            # The team didn't play a double-legged fixture
            average_distance_travelled = round(total_distance / 4) if team_stats[team]['games_travelled_to'] > 0 else 0

        csv_data.append([team] + games + [average_distance_travelled, total_distance])

    # Write team stats to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
        csv_writer = csv.writer(output_csv)
        csv_writer.writerows(csv_data)


# Replace with your file paths
input_file_path = '../../Fixtures, Tables and Results/Fixtures for Distance Calculation/league_stage_and_poko_fixtures_distances.csv'
output_file_path = '../../Fixtures, Tables and Results/Stats/team_stats.csv'

# Use the function with your file paths
calculate_team_stats(input_file_path, output_file_path)
