import csv

def read_teams(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader]

def write_teams(file_path, teams):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for team in teams:
            writer.writerow(team)

def overwrite_csv(source_file, destination_file):
    teams = read_teams(source_file)
    write_teams(destination_file, teams)

# Example usage:
source_csv_path = '../../../../Teams/League Stage/league_stage_teams.csv'
destination_csv_path = '../../Teams/league_stage_teams.csv'

overwrite_csv(source_csv_path, destination_csv_path)
