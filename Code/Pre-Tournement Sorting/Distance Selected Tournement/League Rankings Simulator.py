import csv

# Load the ranked teams from the CSV file
with open('../../../Teams/UEFA Coefficients/ranked_teams.csv', 'r', encoding='utf-8') as f:
    ranked_teams_list = list(csv.reader(f))

# Since the first row is headers, remove it
headers = ranked_teams_list.pop(0)

# Define a variable to control the sorting direction
sorting_direction = 0  # 0 for ascending, 1 for descending


# Function to sort teams by mean distance with direction control and a tiebreaker on coefficient
def sort_teams_by_mean_and_coefficient(teams, direction):
    if direction == 0:
        # Ascending order
        teams.sort(key=lambda x: (float(x[4]), -float(x[3])))
    else:
        # Descending order
        teams.sort(key=lambda x: (-float(x[4]), -float(x[3])))
    return teams


# Group teams by association
teams_by_association = {}
for team in ranked_teams_list:
    association_code = team[1]
    if association_code not in teams_by_association:
        teams_by_association[association_code] = []
    teams_by_association[association_code].append(team)

# Runs the code for each association and saves the sorted teams back in the CSV file
for association_code, teams in teams_by_association.items():
    sorted_teams = sort_teams_by_mean_and_coefficient(teams, sorting_direction)
    file_name = f'../../../Teams/Domestic Leagues/{association_code}_league_results.csv'

    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "team_name", "association", "uefa_coefficient", "city"])  # Only these headers
        for i, team in enumerate(sorted_teams, 1):
            # Write only the selected columns
            writer.writerow([i, team[0], team[1], team[3], team[2]])
