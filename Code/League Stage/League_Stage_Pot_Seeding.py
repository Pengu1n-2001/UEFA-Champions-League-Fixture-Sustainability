import pandas as pd

df = pd.read_csv('../../Teams/League Stage/league_stage_teams.csv')

cl_winner = df[df['status'] == 'UEFA Champions League Winner']
df = df[df['status'] != 'UEFA Champions League Winner']

sorted_teams = df.sort_values(by='uefa_coefficient', ascending=False)
sorted_teams = pd.concat([cl_winner, sorted_teams])

for i in range(4):
    pot_number = i + 1
    sorted_teams.loc[sorted_teams.index[i*9:(i+1)*9], 'pot'] = pot_number

# Convert the 'pot' column to integer type
sorted_teams['pot'] = sorted_teams['pot'].astype(int)

# Select only the required columns for the final output
final_output = sorted_teams[['team_name', 'association', 'uefa_coefficient', 'city', 'pot']]

final_output.to_csv('../../Teams/League Stage/league_stage_teams_seeded_into_pots.csv', index=False)
