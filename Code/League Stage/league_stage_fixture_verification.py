import pandas as pd

# Load the data from CSV files
teams_df = pd.read_csv('../../Teams/League Stage/league_stage_teams_seeded_into_pots.csv')
fixtures_df = pd.read_csv('../../Fixtures, Tables and Results/League Stage/league_stage_fixtures.csv')

# Initialize the new columns for the output DataFrame
for i in range(1, 5):
    teams_df[f'pot {i}_home game'] = 0
    teams_df[f'pot {i}_away game'] = 0

teams_df['same_association'] = 0

# Create a dictionary to quickly find the pot and association of each team
team_pots = teams_df.set_index('team_name')['pot'].to_dict()
team_associations = teams_df.set_index('team_name')['association'].to_dict()

# Process each fixture
for _, fixture in fixtures_df.iterrows():
    home_team = fixture['home_team']
    away_team = fixture['away_team']

    # Ensure that the teams are in the dictionary before updating counts
    if home_team in team_pots and away_team in team_pots:
        home_pot = team_pots[home_team]
        away_pot = team_pots[away_team]
        home_assoc = team_associations[home_team]
        away_assoc = team_associations[away_team]

        # Update home and away game counts
        teams_df.loc[teams_df['team_name'] == home_team, f'pot {away_pot}_home game'] += 1
        teams_df.loc[teams_df['team_name'] == away_team, f'pot {home_pot}_away game'] += 1

        # Update same association count if the associations are the same
        if home_assoc == away_assoc:
            teams_df.loc[teams_df['team_name'] == home_team, 'same_association'] += 1
            teams_df.loc[teams_df['team_name'] == away_team, 'same_association'] += 1

# Check for any invalid fixture by looking for counts greater than 1
invalid_fixture = teams_df[[f'pot {i}_home game' for i in range(1, 5)] + [f'pot {i}_away game' for i in range(1, 5)] + ['same_association']].gt(1).any().any()

if invalid_fixture:
    print("Invalid Fixture List")
else:
    # Save the updated DataFrame to a new CSV file
    output_filename = '../../Fixtures, Tables and Results/League Stage/fixture_verification.csv'
    teams_df.to_csv(output_filename, index=False)
    print(f'Updated data saved to {output_filename}')
