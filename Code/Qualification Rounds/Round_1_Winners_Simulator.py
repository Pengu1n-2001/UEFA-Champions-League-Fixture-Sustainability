import csv
import random

# Read teams from seeded_teams_round_1.csv with utf-8 encoding
with open('../Teams/Qualification Rounds/seeded_teams_round_1.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    teams = [row for row in reader]

# Shuffle teams and create matchups
random.shuffle(teams)
matchups = [(teams[i], teams[i + 1]) for i in range(0, len(teams), 2)]

winners = []

for matchup in matchups:
    # Calculate the sum of uefa_coefficient for the matchup
    total_coefficient = sum(float(team['uefa_coefficient']) for team in matchup)

    # Generate a random number between 0.001 to the total_coefficient
    random_num = random.uniform(0.001, total_coefficient)

    current_sum = 0
    for team in matchup:
        current_sum += float(team['uefa_coefficient'])
        if random_num <= current_sum:
            winners.append(team)
            #output the game with the winner in bold and underlined
            team1 = matchup[0]['team_name']
            team2 = matchup[1]['team_name']
            if team['team_name'] == team1:
                team1 = "\033[1m\033[4m" + team1 + "\033[0m"
            else:
                team2 = "\033[1m\033[4m" + team2 + "\033[0m"
            print(f"{team1} v {team2}")
            break

# Write the winners to champions_path_round_2_teams.csv with utf-8 encoding
fieldnames = ["team_name", "association", "uefa_coefficient", "city"]
with open('../Teams/Qualification Rounds/champions_path_round_2_teams.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for team in winners:
        writer.writerow(team)
