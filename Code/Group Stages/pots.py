import csv

file_path = '../../Teams/League Stage/league_stage_teams.csv'
teams = []

with open(file_path, mode='r', encoding='utf-8') as file:
    teams = list(csv.DictReader(file))

# get the teams with a special status so that they are seeded first
cl_winner = [team for team in teams if team['special_status'] == 'Champions League Winner']
el_winner = [team for team in teams if team['special_status'] == 'Europa League Winner']
other_teams = [team for team in teams if team['special_status'] not in ['Champions League Winner', 'Europa League Winner']]
other_teams.sort(key=lambda x: float(x['uefa_coefficient']), reverse=True)

pots = [[] for _ in range(4)] # distribute the teams into 4 pots

pots[0].extend(cl_winner + el_winner) # make sure ucl and el winners are seeded first

# seed other teams
for i, team in enumerate(other_teams):
    pots[(i + 2) // 9].append(team)  # the +2 is because of the UCL/EL winners


# writing teams to new csv
output_file_path = '../../Teams/League Stage/league_stage_teams_seeded_into_pots.csv'

with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['team_name', 'association', 'pot'])

    for i, pot in enumerate(pots):
        for team in pot:
            writer.writerow([team['team_name'], team['association'], i + 1])