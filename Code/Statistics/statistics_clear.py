import csv

# used to clear csv files that do not get overwitten so that the code can be ran again
def clear_csv_content(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader, None)  # reads the headers of the csv file

    # writes the headers back if they exist
    if headers:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

# list of csvs that need clearing
clear_csv_content('../../Fixtures, Tables and Results/Stats/run_distance_analysis.csv')
clear_csv_content('../../Fixtures, Tables and Results/Stats/qualified_teams.csv')
