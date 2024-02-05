import csv
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# Read fixture data
with open('../../Fixtures, Tables and Results/Fixtures for Distance Calculation/league_stage_and_poko_fixtures.csv', 'r', encoding='utf-8') as fixture_csv:
    fixtures = list(csv.reader(fixture_csv))

# Read city data, skipping the header row
with open('../../Teams/UEFA Coefficients/city_location_data.csv', 'r', encoding='utf-8') as city_csv:
    city_reader = csv.DictReader(city_csv)
    cities = {row['city']: {'lat': float(row['latitude']), 'lon': float(row['longitude'])} for row in city_reader}

# Calculate distances and create new data
new_data = [['home_team', 'home_team_city', 'away_team', 'away_team_city', 'double_legged_status', 'distance']]

for fixture in fixtures:
    home_city = fixture[1]
    away_city = fixture[3]

    try:
        home_coordinates = cities[home_city]
        away_coordinates = cities[away_city]
    except KeyError:
        print(f"KeyError: City not found - home_team_city: {home_city}, away_team_city: {away_city}")
        continue

    distance = haversine(home_coordinates['lat'], home_coordinates['lon'], away_coordinates['lat'], away_coordinates['lon'])

    new_data.append([fixture[0], home_city, fixture[2], away_city, fixture[4], distance])

# Write new data to CSV
with open('../../Fixtures, Tables and Results/Fixtures for Distance Calculation/league_stage_and_poko_fixtures_distances.csv', 'w', newline='', encoding='utf-8') as output_csv:
    csv.writer(output_csv).writerows(new_data)
