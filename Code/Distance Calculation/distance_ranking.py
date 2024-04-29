import pandas as pd

# Load the CSV files
teams_df = pd.read_csv('../../Teams/UEFA Coefficients/all_potential_teams.csv')
distance_matrix_df = pd.read_csv('../../Teams/UEFA Coefficients/distance_matrix.csv')
distance_matrix_df.set_index('Unnamed: 0', inplace=True)
distance_matrix_df.index.name = 'city'

# Filter out teams from the association with the code 'RUS'
teams_df = teams_df[teams_df['association'] != 'RUS']

# Function to calculate distances and sort teams by mean distance
def calculate_distances(teams_df, distance_matrix_df):
    team_distances = []
    for index, row in teams_df.iterrows():
        team_city = row['city'].lower()  # Convert to lowercase to match matrix
        if team_city in distance_matrix_df.index:
            distances = distance_matrix_df.loc[team_city]
            total_distance = distances.sum()
            mean_distance = round(distances.mean())  # Round mean to the nearest integer
            median_distance = distances.median()
            team_distances.append({
                'team_name': row['team_name'],
                'association': row['association'],
                'city': row['city'],  # Maintain original case for city names
                'uefa_coefficient': row['uefa_coefficient'],
                'total_distance': total_distance,
                'mean_distance': mean_distance,
                'median_distance': median_distance
            })

    ranking_df = pd.DataFrame(team_distances)
    ranking_df.sort_values(by='mean_distance', inplace=True)
    ranking_df.reset_index(drop=True, inplace=True)
    return ranking_df

# Example usage
ranking_df = calculate_distances(teams_df, distance_matrix_df)
print(ranking_df)

# To save the output to a CSV file
ranking_df.to_csv('../../Teams/UEFA Coefficients/ranked_teams.csv', index=False)
