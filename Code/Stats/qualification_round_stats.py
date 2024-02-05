import os
import csv

def read_teams(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def write_teams(file_path, teams, mode='a'):
    with open(file_path, mode=mode, newline='', encoding='utf-8') as file:
        fieldnames = ["run", "team_name", "uefa_coefficient", "qualified"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if mode == 'w':  # Write header only if in write mode
            writer.writeheader()
        for team in teams:
            # Filter out fields not in fieldnames
            filtered_team = {key: value for key, value in team.items() if key in fieldnames}
            writer.writerow(filtered_team)


# Step 1: Read existing "qualification_results.csv" file
result_file_path = "../../Fixtures, Tables, Stats and Results/Stats/Qualifying Teams/qualification_results.csv"
run_number = 1

if os.path.exists(result_file_path):
    existing_results = read_teams(result_file_path)
    if existing_results:
        run_number = int(existing_results[-1]['run']) + 1
else:
    # Initialize the headers if the file doesn't exist
    write_teams(result_file_path, [{'run': 'run', 'team_name': 'team_name', 'uefa_coefficient': 'uefa_coefficient', 'qualified': 'qualified'}], mode='w')

# Step 2-4: Process each qualifying round file and identify qualified teams
qualifying_rounds = [
    "Champions Path Play-off Round/champions_path_play_off_round_teams.csv",
    "League Path Play-off Round/league_path_play_off_round_teams.csv",
    "League Path Round 3/league_path_round_3_teams.csv",
    "Champions Path Round 3/champions_path_round_3_teams.csv",
    "League Path Round 2/league_path_round_2_teams.csv",
    "Champions Path Round 2/champions_path_round_2_teams.csv",
    "Champions Path Round 1/champions_path_round_1_teams.csv"
]

qualified_teams = set()

for round_file in qualifying_rounds:
    round_file_path = f"../../Teams/Qualification Rounds/{round_file}"
    round_teams = read_teams(round_file_path)

    for row in round_teams:
        team_name = row['team_name']
        if team_name not in qualified_teams:
            qualified_teams.add(team_name)
            row['run'] = run_number
            row['qualified'] = 0
            existing_results.append(row)

# Step 5: Identify qualified teams from "league_stage_teams.csv" and update "qualification_results.csv"
qualified_teams_in_league = set()

league_teams = read_teams("../../Teams/League Stage/league_stage_teams.csv")
for row in league_teams:
    qualified_teams_in_league.add(row['team_name'])

for row in existing_results:
    team_name = row['team_name']
    qualified = 1 if team_name in qualified_teams_in_league else 0
    row['qualified'] = qualified

write_teams(result_file_path, existing_results, mode='w')
