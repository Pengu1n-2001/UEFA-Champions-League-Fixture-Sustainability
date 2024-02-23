import csv

def populate_fixture_distances(fixtures_file, distance_matrix_file, output_file):
    # Read fixture data
    with open(fixtures_file, 'r', encoding='utf-8') as fixture_csv:
        fixtures = list(csv.reader(fixture_csv))

    # Read distance matrix
    with open(distance_matrix_file, 'r', encoding='utf-8') as matrix_csv:
        distance_matrix_data = list(csv.reader(matrix_csv))

    # Extract cities and coordinates
    cities = distance_matrix_data[0][1:]
    coordinates = {row[0].lower(): row[1:] for row in distance_matrix_data[1:]}

    # Create new data with distances for each fixture using the matrix
    new_data = [['home_team', 'home_team_city', 'away_team', 'away_team_city', 'group', 'distance']]

    for fixture in fixtures[1:]:  # Assuming the header is present
        home_team = fixture[1].lower()
        away_team = fixture[3].lower()

        # Find distances using the matrix
        if home_team in coordinates and away_team in coordinates:
            distances = coordinates[home_team]
            distance = float(distances[cities.index(away_team)])
            new_data.append([fixture[0], home_team, fixture[2], away_team, fixture[4], distance])
        else:
            print(f"Warning: City coordinates not found for fixture {fixture}")

    # Write new data to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
        csv.writer(output_csv).writerows(new_data)

# Replace with your file paths
fixtures_file_path_2021 = '../../../Alternative Formats/Current Groupstage UCL Format/Fixtures/2021_fixtures.csv'
fixtures_file_path_2022 = '../../../Alternative Formats/Current Groupstage UCL Format/Fixtures/2022_fixtures.csv'
fixtures_file_path_2023 = '../../../Alternative Formats/Current Groupstage UCL Format/Fixtures/2023_fixtures.csv'
distance_matrix_file_path = '../../../Teams/UEFA Coefficients/distance_matrix.csv'
output_file_path_2021 = '../../../Alternative Formats/Current Groupstage UCL Format/Distances/2021_distances.csv'
output_file_path_2022 = '../../../Alternative Formats/Current Groupstage UCL Format/Distances/2022_distances.csv'
output_file_path_2023 = '../../../Alternative Formats/Current Groupstage UCL Format/Distances/2023_distances.csv'

populate_fixture_distances(fixtures_file_path_2021, distance_matrix_file_path, output_file_path_2021)
populate_fixture_distances(fixtures_file_path_2022, distance_matrix_file_path, output_file_path_2022)
populate_fixture_distances(fixtures_file_path_2023, distance_matrix_file_path, output_file_path_2023)