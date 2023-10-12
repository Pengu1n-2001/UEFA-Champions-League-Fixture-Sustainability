import csv
import random

# Read teams from potential_teams_round_1.csv
with open('../Teams/Qualification Rounds/potential_teams_round_1.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    teams = [row for row in reader]

# Group teams by association
associations = {team['association'] for team in teams}
seeded_teams = []

for association in associations:
    associated_teams = [team for team in teams if team['association'] == association]

    # Calculate the sum of uefa_coefficient for the association
    total_coefficient = sum(float(team['uefa_coefficient']) for team in associated_teams)

    # Generate a random number between 0.001 to the total_coefficient
    random_num = random.uniform(0.001, total_coefficient)

    current_sum = 0
    for team in associated_teams:
        current_sum += float(team['uefa_coefficient'])
        if random_num <= current_sum:
            seeded_teams.append(team)
            break

# Write the selected teams to seeded_teams_round_1.csv
fieldnames = ["team_name", "association", "uefa_coefficient", "city"]
with open('../Teams/Qualification Rounds/seeded_teams_round_1.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for team in seeded_teams:
        writer.writerow(team)