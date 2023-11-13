import csv

# Function to clear the contents of a CSV file except for the headers
def clear_csv_content(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader, None)  # Read the headers

    if headers:  # If there were headers, write them back, otherwise do nothing
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)


clear_csv_content('../../Teams/Qualification Rounds/Champions Path Round 3/champions_path_round_3_teams.csv')
clear_csv_content('../../Teams/Qualification Rounds/League Path Play-off Round/league_path_play_off_round_teams.csv')