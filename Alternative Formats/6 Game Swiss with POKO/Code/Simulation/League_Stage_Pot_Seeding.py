import pandas as pd
# read the league stage teams
df = pd.read_csv('../../Teams/league_stage_teams.csv')

cl_winner = df[df['status'] == 'UEFA Champions League Winner']
df = df[df['status'] != 'UEFA Champions League Winner']

sorted_teams = df.sort_values(by='uefa_coefficient', ascending=False)
sorted_teams = pd.concat([cl_winner, sorted_teams])

# sorts the teams into 4 pots of 9 teams
for i in range(3):
    pot_number = i + 1 # to account for the UCL Titleholders being seeded as first
    sorted_teams.loc[sorted_teams.index[i*12:(i+1)*12], 'pot'] = pot_number

# convert the 'pot' column to integer type
sorted_teams['pot'] = sorted_teams['pot'].astype(int)

# select only the required columns for the final output
final_output = sorted_teams[['team_name', 'association', 'uefa_coefficient', 'city', 'pot']]

final_output.to_csv('../Teams/league_stage_teams_seeded_into_pots.csv', index=False)
