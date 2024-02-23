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
        distance = round(float(fixture[5]))  # Round to the nearest whole number

        # Find the next empty game column for the home team and update with 0
        for i in range(1, 7):  # Only 6 games as per your requirement
            if team_stats[home_team][f'game_{i}'] == 0:
                team_stats[home_team][f'game_{i}'] = 0
                break

        # Update away team's stats in the next available game column
        for i in range(1, 7):  # Only 6 games as per your requirement
            if team_stats[away_team][f'game_{i}'] == 0:
                team_stats[away_team][f'game_{i}'] = distance
                break

    # Calculate average distance and create CSV data
    csv_data = [['team', 'game_1', 'game_2', 'game_3', 'game_4', 'game_5', 'game_6',
                 'average_distance_travelled_per_away_game', 'total_distance_travelled']]

    for team, stats in team_stats.items():
        total_distance = sum(stats[f'game_{i}'] for i in range(1, 7))
        average_distance = round(total_distance / 3)  # As per your requirement, dividing by 3
        csv_data.append([team] + [stats[f'game_{i}'] for i in range(1, 7)] + [average_distance, total_distance])

    # Write team stats to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
        csv_writer = csv.writer(output_csv)
        csv_writer.writerows(csv_data)

# Replace with your file paths
input_file_path_2021 = '../../../Alternative Formats/Current Groupstage UCL Format/Distances/2021_distances.csv'
input_file_path_2022 = '../../../Alternative Formats/Current Groupstage UCL Format/Distances/2022_distances.csv'
input_file_path_2023 = '../../../Alternative Formats/Current Groupstage UCL Format/Distances/2023_distances.csv'
output_file_path_2021 = '../../../Alternative Formats/Current Groupstage UCL Format/Teams/team_stats_2021.csv'
output_file_path_2022 = '../../../Alternative Formats/Current Groupstage UCL Format/Teams/team_stats_2022.csv'
output_file_path_2023 = '../../../Alternative Formats/Current Groupstage UCL Format/Teams/team_stats_2023.csv'

# Use the function with your file paths
calculate_team_stats(input_file_path_2021, output_file_path_2021)
calculate_team_stats(input_file_path_2022, output_file_path_2022)
calculate_team_stats(input_file_path_2023, output_file_path_2023)
