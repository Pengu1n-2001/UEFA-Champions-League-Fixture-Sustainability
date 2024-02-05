import pandas as pd

# loads the league stage match results from the csv
df = pd.read_csv('../../Fixtures, Tables, Stats and Results/League Stage/league_stage_results.csv')

# creates a dictionary to hold the data of the teams
teams = {}

# processes each team
for index, row in df.iterrows():
    # Extract team names and result
    home_team = row['home_team']
    away_team = row['away_team']
    result = row['result']

    # creates an entry in the table for each team
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

    # updates win/draw/loss counters and points based on the results
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

# converts the table into a dataframe
league_table = pd.DataFrame(teams.values())

# sort the teams first by points, then by UEFA coefficient (as a tiebreaker)
league_table.sort_values(by=['points', 'uefa_coefficient'], ascending=[False, False], inplace=True)

# resets the index of the table so that teams have their correct rank
league_table.reset_index(drop=True, inplace=True)
league_table.index += 1
league_table['rank'] = league_table.index

# re-orders the teams to create an ordered league table, and outputs this to the csv
final_columns = ['rank', 'team_name', 'association', 'uefa_coefficient', 'city', 'points', 'wins', 'draws', 'losses']
league_table = league_table[final_columns]
league_table.to_csv('../../Fixtures, Tables, Stats and Results/League Stage/league_stage_table.csv', index=False)


