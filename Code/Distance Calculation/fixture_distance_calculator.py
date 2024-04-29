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
    new_data = [['match', 'home_team', 'home_team_coefficient', 'home_team_city', 'home_team_association',
                 'away_team', 'away_team_coefficient', 'away_team_city', 'away_team_association', 'distance']]

    for fixture in fixtures[1:]:  # Assuming the header is present
        home_team_city = fixture[3].lower()  # Adjust index as needed based on input file structure
        away_team_city = fixture[7].lower()  # Adjust index as needed based on input file structure

        # Find distances using the matrix
        if home_team_city in coordinates and away_team_city in coordinates:
            distance_index = cities.index(away_team_city)
            distance = float(coordinates[home_team_city][distance_index])
            new_data.append([fixture[0], fixture[1], fixture[2], fixture[3], fixture[4],
                             fixture[5], fixture[6], fixture[7], fixture[8], distance])
        else:
            print(f"Warning: City coordinates not found for fixture between {home_team_city} and {away_team_city}")

    # Write new data to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
        csv.writer(output_csv).writerows(new_data)

# Replace with your file paths
fixtures_file_path = '../../Fixtures, Tables and Results/Fixtures for Distance Calculation/league_stage_fixtures.csv'
distance_matrix_file_path = '../../Teams/UEFA Coefficients/distance_matrix.csv'
output_file_path = '../../Fixtures, Tables and Results/Fixtures for Distance Calculation/league_stage_fixtures_distances.csv.csv'

# Use the function with your file paths
populate_fixture_distances(fixtures_file_path, distance_matrix_file_path, output_file_path)
