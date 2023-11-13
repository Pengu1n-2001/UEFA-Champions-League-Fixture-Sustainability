import csv
import random
with open('../../Teams/UEFA Coefficients/all_potential_teams.csv', 'r', encoding='utf-8') as f:
    all_teams = list(csv.reader(f))
teams_by_association = {}
for team in all_teams[1:]:
    association_code = team[1]
    if association_code not in teams_by_association:
        teams_by_association[association_code] = []
    teams_by_association[association_code].append(team)
def rank_teams(teams):
    ranked_teams = []

    while teams:
        total_coefficient = sum([float(team[2]) for team in teams])
        random_number = random.uniform(0.001, total_coefficient)
        cumulative_coefficient = 0

        for i, team in enumerate(teams):
            coefficient = float(team[2])
            cumulative_coefficient += coefficient
            if random_number <= cumulative_coefficient:
                ranked_teams.append(team)
                teams.pop(i)
                break

    return ranked_teams


# Rank teams for each association and write to separate CSV files
for association_code, teams in teams_by_association.items():
    ranked_teams = rank_teams(teams)
    file_name = f'../../Teams/Domestic Leagues/{association_code}_league_results.csv'

    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "team_name", "association", "uefa_coefficient", "city"])
        for i, team in enumerate(ranked_teams, 1):
            writer.writerow([i] + team)
