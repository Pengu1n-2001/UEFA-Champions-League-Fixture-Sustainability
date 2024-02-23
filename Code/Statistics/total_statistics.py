import csv

def read_teams(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def write_teams(file_path, teams, mode='a'):
    with open(file_path, mode=mode, newline='', encoding='utf-8') as file:
        fieldnames = ["run", "average_distance_travelled_per_team", "average_distance_travelled_per_game", "total_distance_travelled", "longest_distance_travelled_by_a_team", "fixture_with_longest_distance"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if mode == 'w':  # Write header only if in write mode
            writer.writeheader()
        for team in teams:
            writer.writerow(team)

def calculate_means_and_longest_entries(teams):
    # Calculate means
    total_entries = len(teams)
    mean_average_distance_per_team = sum(float(team['average_distance_travelled_per_team']) for team in teams) / total_entries
    mean_average_distance_per_game = sum(float(team['average_distance_travelled_per_game']) for team in teams) / total_entries
    mean_total_distance_travelled = sum(float(team['total_distance_travelled']) for team in teams) / total_entries

    # Find the entry with the longest distance travelled by a team
    longest_distance_entry = max(teams, key=lambda x: float(x['longest_distance_travelled_by_a_team'].split(" - ")[-1]))

    # Find the entry with the longest distance fixture
    longest_fixture_entry = max(teams, key=lambda x: float(x['fixture_with_longest_distance'].split(" - ")[-1]))

    return {
        'run': 'Total',
        'average_distance_travelled_per_team': mean_average_distance_per_team,
        'average_distance_travelled_per_game': mean_average_distance_per_game,
        'total_distance_travelled': mean_total_distance_travelled,
        'longest_distance_travelled_by_a_team': longest_distance_entry['longest_distance_travelled_by_a_team'],
        'fixture_with_longest_distance': longest_fixture_entry['fixture_with_longest_distance']
    }
# Read the CSV file
teams = read_teams("../../Fixtures, Tables and Results/Stats/run_distance_analysis.csv")

# Calculate means and find longest entries
total_entry = calculate_means_and_longest_entries(teams)

# Write the calculated entry to a new CSV
write_teams("../../Fixtures, Tables and Results/Stats/total_distance_analysis.csv", [total_entry], mode='w')
