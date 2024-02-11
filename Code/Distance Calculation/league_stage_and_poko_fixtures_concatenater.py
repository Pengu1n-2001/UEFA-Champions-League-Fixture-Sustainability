import csv
def create_fixtures_csv(league_stage_file, knockout_stage_file, output_file):
    with open(league_stage_file, 'r',encoding='utf-8') as league_csv:
        league_fixtures = list(csv.reader(league_csv))

    league_fixtures_data = [[row[1], row[3], row[5], row[7], ''] for row in league_fixtures[1:]]

    with open(knockout_stage_file, 'r',encoding='utf-8') as knockout_csv:
        knockout_fixtures = list(csv.reader(knockout_csv))

    knockout_fixtures_data = [[row[1], row[3], row[5], row[7], '1'] for row in knockout_fixtures[1:9]]

    all_fixtures_data = league_fixtures_data + knockout_fixtures_data

    with open(output_file, 'w', newline='',encoding='utf-8') as output_csv:
        csv.writer(output_csv).writerow(['home_team', 'home_team_city', 'away_team', 'away_team_city', 'double_legged_status'])
        csv.writer(output_csv).writerows(all_fixtures_data)

# Replace with your file paths
league_stage_file_path = '../../Fixtures, Tables and Results/League Stage/league_stage_fixtures.csv'
knockout_stage_file_path = '../../Fixtures, Tables and Results/Knockout Stage/knockout_stage_results.csv'
output_file_path = '../../Fixtures, Tables and Results/Fixtures for Distance Calculation/league_stage_and_poko_fixtures.csv'

create_fixtures_csv(league_stage_file_path, knockout_stage_file_path, output_file_path)
