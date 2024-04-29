import subprocess
import os
import sys
import csv
from alive_progress import alive_bar;
import time


def run_python_script(script_path):
    python_executable = sys.executable
    absolute_script_path = os.path.abspath(script_path)
    working_directory = os.path.dirname(absolute_script_path)
    subprocess.run([python_executable, absolute_script_path], cwd=working_directory)


def update_coefficents():
    run_python_script(
        './UEFA Coefficients/UEFA_Club_Coefficients_Updater.py')  # LOCKED TO COEFFICENTS AFTER UCL GROUP STAGE CONCLUSION 2023


def update_matrix():
    run_python_script('./Distance Calculation/distance_matrix_generator.py')


def city_key_check():
    run_python_script('./Distance Calculation/city_key_check.py')



def run_save_state_variation_epslon():
    epsilon = ['0.10','0.25','0.50','0.75','0.90']
    for x in range(5):
        epsilon_value = epsilon[x]
        print(epsilon_value)
        for save_state in range(1, 6):
            save_state_file = f'../Data for Analysis/Greedy-Epsilon/{epsilon_value}/greedy_epsilon_{epsilon_value}_save_state_{save_state}_data.csv'
            save_state_data = f'../Fixtures, Tables and Results/Save States/save_state_{save_state}.csv'
            input_file = save_state_data
            output_file = '../Teams/League Stage/league_stage_teams.csv'
            with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
                reader = csv.reader(infile)
                writer = csv.writer(outfile)
                for row in reader:
                    writer.writerow(row)
            total_runs=10
            with alive_bar(total_runs, force_tty=True) as bar:
                for run_number in range(total_runs):
                    run_python_script('./Pre-Tournement Sorting/CSV Contents Clear.py')
                    run_python_script('League Stage/League_Stage_Pot_Seeding.py')
                    run_python_script(f'League Stage/League_Stage_Fixture_Generator_2.5_Epsilon_{epsilon_value}.py')
                    run_python_script('./League Stage/League_Stage_Simulator.py')
                    run_python_script('./League Stage/League_Table_Generator.py')
                    run_python_script('/League Stage/league_stage_fixture_verification.py')
                    run_python_script('./Knockout Round/Knockout_Round_Simulator.py')
                    run_python_script('./League Stage/distance_calculator.py')
                    fixtures = '../Fixtures, Tables and Results/League Stage/league_stage_fixtures_distances.csv'
                    csv_writer(save_state_file, fixtures, run_number+1)
                    bar()

def csv_writer(source_file_path, data_to_add_file, run_number):
    with open(data_to_add_file, mode='r', newline='') as data_file:
        data_reader = csv.reader(data_file)
        data_headers = next(data_reader)  # Read the headers
        data_rows = list(data_reader)
    with open(source_file_path, mode='r+', newline='') as source_file:
        source_writer = csv.writer(source_file)
        source_reader = csv.reader(source_file)
        try:
            next(source_reader)
        except StopIteration:
            source_writer.writerow(['replicate'] + data_headers)
        source_file.seek(0, 2)
        for row in data_rows:
            new_row = [run_number] + row
            source_writer.writerow(new_row)


while 1 == 1:
    settings_choice = input("Would you like to view settings? Y/N: ")
    if settings_choice.lower() == ("y"):
        settings_choice2 = input("""1.Update UEFA Coefficents (NOT RECOMMENDED)
2.Update distance matrix
3.Check City Keys
4.Exit Settings
""")
        if settings_choice2 == ("1"):
            update_coefficents()
        elif settings_choice2 == ("2"):
            update_matrix()
        elif settings_choice2 == ("3"):
            city_key_check()
    else:
        clear_stats = input("Would you like to clear stats? Y/N: ")
        if clear_stats.lower() == ("y"):
            run_python_script('./Statistics/statistics_clear.py')
        simulation_type = int(input("""What Simulation would you like to run?: 
1. Simulate various optimisation algorithms based on save state
"""))

    if simulation_type == 1:
            run_save_state_variation_epslon()

