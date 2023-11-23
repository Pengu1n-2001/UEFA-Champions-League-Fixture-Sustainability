import pandas as pd

# Load the match results from the CSV file
df = pd.read_csv('../../Fixtures, Tables and Results/League Stage/league_stage_results.csv')

# Initialize a dictionary to hold team data
teams = {}

# Process each match in the DataFrame
for index, row in df.iterrows():
    # Extract team names and result
    home_team = row['home_team']
    away_team = row['away_team']
    result = row['result']

    # Initialize team data if not already done
    for team_key in ['home_team', 'away_team']:
        team_name = row[team_key]
        if team_name not in teams:
            teams[team_name] = {
                'team_name': team_name,
                'association': row[f'{team_key}_association'],
                'uefa_coefficient': float(row[f'{team_key}_coefficient']),
                'city': row[f'{team_key}_city'],
                'points': 0,
                'wins': 0,
                'draws': 0,
                'losses': 0
            }

    # Update points and win/draw/loss count based on match result
    if result == 'H':
        teams[home_team]['points'] += 3
        teams[home_team]['wins'] += 1
        teams[away_team]['losses'] += 1
    elif result == 'A':
        teams[away_team]['points'] += 3
        teams[away_team]['wins'] += 1
        teams[home_team]['losses'] += 1
    elif result == 'T':
        teams[home_team]['points'] += 1
        teams[away_team]['points'] += 1
        teams[home_team]['draws'] += 1
        teams[away_team]['draws'] += 1

# Convert the teams dictionary to a DataFrame
league_table = pd.DataFrame(teams.values())

# Sort the teams first by points, then by UEFA coefficient (as a tiebreaker)
league_table.sort_values(by=['points', 'uefa_coefficient'], ascending=[False, False], inplace=True)

# Reset index to get the rank
league_table.reset_index(drop=True, inplace=True)
league_table.index += 1
league_table['rank'] = league_table.index

# Select and reorder columns for the final CSV
final_columns = ['rank', 'team_name', 'association', 'uefa_coefficient', 'city', 'points', 'wins', 'draws', 'losses']
league_table = league_table[final_columns]
league_table.to_csv('../../Fixtures, Tables and Results/League Stage/league_stage_table.csv', index=False)


