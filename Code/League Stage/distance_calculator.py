import csv

def populate_fixture_distances(fixtures_file, distance_matrix_file, output_file):
    # Read fixture data
    with open(fixtures_file, 'r', encoding='utf-8') as fixture_csv:
        fixtures = list(csv.DictReader(fixture_csv))

    # Read distance matrix
    with open(distance_matrix_file, 'r', encoding='utf-8') as matrix_csv:
        distance_matrix_data = list(csv.reader(matrix_csv))

    # Extract cities and the corresponding column indices
    cities = distance_matrix_data[0][1:]
    coordinates = {row[0].lower(): row[1:] for row in distance_matrix_data[1:]}

    # Create new data with distances for each fixture using the matrix
    new_data = []

    for fixture in fixtures:
        home_team_city = fixture['home_team_city'].lower()
        away_team_city = fixture['away_team_city'].lower()

        # Find distances using the matrix
        if home_team_city in coordinates and away_team_city in coordinates:
            distance_index = cities.index(away_team_city)
            distance = float(coordinates[home_team_city][distance_index])
            fixture['distance'] = distance
        else:
            fixture['distance'] = 'N/A'  # Use 'N/A' if no distance could be found
            print(f"Warning: City coordinates not found for fixture between {home_team_city} and {away_team_city}")

        new_data.append(fixture)

    # Write new data to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
        fieldnames = fixtures[0].keys()  # Get field names from the first row of fixtures
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_data)

# Replace with your file paths
fixtures_file_path = '../../Fixtures, Tables and Results/League Stage/league_stage_fixtures.csv'
distance_matrix_file_path = '../../Teams/UEFA Coefficients/distance_matrix.csv'
output_file_path = '../../Fixtures, Tables and Results/League Stage/league_stage_fixtures_distances.csv'
# Use the function with your file paths
populate_fixture_distances(fixtures_file_path, distance_matrix_file_path, output_file_path)
