import pandas as pd
import random

# Function to calculate the probability of a tie
def calculate_tie_probability(home_coeff, away_coeff, base_tie_probability=0.40):
    coeff_diff = abs(home_coeff - away_coeff)
    # Adjust the base probability based on the coefficient difference
    adjusted_probability = max(base_tie_probability - coeff_diff * (base_tie_probability / 100), 0)
    return adjusted_probability

# Read the fixtures from the CSV file
df = pd.read_csv('../../Fixtures, Tables and Results/League Stage/league_stage_fixtures.csv')

# List to store the updated fixtures with results
updated_fixtures = []

# Process each fixture
for index, row in df.iterrows():
    home_coeff = float(row['home_team_coefficient'])
    away_coeff = float(row['away_team_coefficient'])

    # Calculate the weights for home win, away win, and tie
    home_weight = home_coeff
    away_weight = away_coeff
    tie_weight = calculate_tie_probability(home_coeff, away_coeff) * (home_coeff + away_coeff)

    total_weight = home_weight + away_weight + tie_weight
    random_num = random.uniform(0, total_weight)

    # Determine the match result
    if random_num <= home_weight:
        result = "H"
    elif random_num <= home_weight + away_weight:
        result = "A"
    else:
        result = "T"

    # Add the result to the fixture and store it
    updated_fixture = row.to_list() + [result]
    updated_fixtures.append(updated_fixture)

# Write the updated fixtures with results to a new CSV file
headers = list(df.columns) + ['result']
new_df = pd.DataFrame(updated_fixtures, columns=headers)
new_df.to_csv('../../Fixtures, Tables and Results/League Stage/league_stage_results.csv', index=False)
