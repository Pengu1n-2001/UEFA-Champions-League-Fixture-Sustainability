import csv
import random


# loads previous UCL/UEL finalists
with open('../../Teams/UEFA Coefficients/UCL_previous_finalists', 'r', encoding='utf-8') as f:
    ucl_finalists = list(csv.reader(f))

with open('../../Teams/UEFA Coefficients/UEL_previous_finalists', 'r', encoding='utf-8') as f:
    uel_finalists = list(csv.reader(f))

# loads the list of all teams so that other team data can be obtained
with open('../../Teams/UEFA Coefficients/all_potential_teams.csv', 'r', encoding='utf-8') as f:
    all_teams = list(csv.reader(f))


# chooses a UCL/UEL winner from last 10 UCL/UEL finals (winners get 2 points and runners-up get 1 point)
def choose_winner(finalists):
    total_weight = 0
    weights = {}

    for team in finalists[1:]:
        weight = int(team[1]) * 2 + int(team[2])
        total_weight += weight
        weights[team[0]] = weight

    rand_value = random.randint(1, total_weight)

    for team, weight in weights.items():
        rand_value -= weight
        if rand_value <= 0:
            return team


# choose UCL winner
ucl_winner = choose_winner(ucl_finalists)

# choose UEL winner, ensuring it's not the same as the UCL winner
uel_winner = choose_winner(uel_finalists)
while ucl_winner == uel_winner:
    uel_winner = choose_winner(uel_finalists)

# write winners to the League Stage as they auto qualify
with open('../../Teams/League Stage/league_stage_teams.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["team_name", "association", "uefa_coefficient", "city", "status"])
    for team in all_teams[1:]:
        if team[0] == ucl_winner:
            writer.writerow(team + ["UEFA Champions League Winner"])
        elif team[0] == uel_winner:
            writer.writerow(team + ["UEFA Europa League Winner"])
