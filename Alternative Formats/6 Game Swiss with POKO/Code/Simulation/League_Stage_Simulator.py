import pandas as pd
import random

# works out the maximum probability of a draw. (set at 0.42 as average draw % in UCL is 21% (* 2 for both teams)
def calculate_tie_probability(home_coeff, away_coeff, base_tie_probability=0.42):
    coeff_diff = abs(home_coeff - away_coeff)
    # adjusts the base probability based on the coefficient difference (closer = more likely)
    adjusted_probability = max(base_tie_probability - coeff_diff * (base_tie_probability / 100), 0)
    return adjusted_probability

# read the fixtures from the CSV
df = pd.read_csv('../../Fixtures/league_stage_fixtures.csv')

# creates a list to store the fixtures with results
updated_fixtures = []

# processes each fixture
for index, row in df.iterrows():
    home_coeff = float(row['home_team_coefficient'])
    away_coeff = float(row['away_team_coefficient'])

    # calculates the weights for home win, away win, and tie
    home_weight = home_coeff
    away_weight = away_coeff
    tie_weight = calculate_tie_probability(home_coeff, away_coeff) * (home_coeff + away_coeff)

    total_weight = home_weight + away_weight + tie_weight
    random_num = random.uniform(0, total_weight)

    # determines the match result using a weighted random selection
    if random_num <= home_weight:
        result = "H"
    elif random_num <= home_weight + away_weight:
        result = "A"
    else:
        result = "T"

    # adds the result to the list of updated fixtures
    updated_fixture = row.to_list() + [result]
    updated_fixtures.append(updated_fixture)

# writes the updated fixtures to a csv file
headers = list(df.columns) + ['result']
new_df = pd.DataFrame(updated_fixtures, columns=headers)
new_df.to_csv('../../Fixtures/league_stage_results.csv', index=False)
