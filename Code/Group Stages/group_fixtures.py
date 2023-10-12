import csv
import random

teams = []

# take the already seeded teams
with open('../Teams/League Stage/league_stage_teams_seeded_into_pots.csv', mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        teams.append(row)

# create the empty pots
pots = [[] for _ in range(4)]  # create 4 empty pots
for team in teams:
    pot_num = int(team['pot']) - 1  # subtract 1 to make it zero-based index
    pots[pot_num].append(team)

fixtures = []

# VERY BASIC MATCHMAKING DOES NOT MEET ALL CONSTRAINTS
for team_data in teams:
    team = team_data['team_name']
    home_matches, away_matches = 4, 4  #attemps to do home and away matches (i have no clue if this is actually working, techically doesnt matter)

    for pot in pots:
        # makes a version of a pot without the team in it so that the team can draw the teams from its own pot
        if team_data in pot:
            pot_without_team = [t for t in pot if t != team_data]
        else:
            pot_without_team = pot

        draw = random.choice(pot_without_team)

        # ensures they are not from the same association and have not been drawn before
        while draw['association'] == team_data['association'] or \
                any(team in fixture and draw['team_name'] in fixture for fixture in fixtures):
            draw = random.choice(pot_without_team)

        if home_matches > 0:
            fixtures.append((team, draw['team_name']))
            home_matches -= 1
        else:
            fixtures.append((draw['team_name'], team))
            away_matches -= 1

for fixture in fixtures:
    print(f"{fixture[0]} vs {fixture[1]}")