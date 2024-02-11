import subprocess
import os
import sys
import csv
from alive_progress import alive_bar; import time

def run_python_script(script_path):
    python_executable = sys.executable
    absolute_script_path = os.path.abspath(script_path)
    working_directory = os.path.dirname(absolute_script_path)
    subprocess.run([python_executable, absolute_script_path], cwd=working_directory)


def update_coefficents():
    run_python_script('./UEFA Coefficients/UEFA_Club_Coefficients_Updater.py') # LOCKED TO COEFFICENTS AFTER UCL GROUP STAGE CONCLUSION 2023

def update_matrix():
    run_python_script('./Distance Calculation/distance_matrix_generator.py')

def total_stats():
    run_python_script('./Statistics/total_statistics.py')
    file_path = "../Fixtures, Tables and Results/Stats/total_distance_analysis.csv"
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        teams = [row for row in reader]
    for team in teams:
        print(f"Average Distance per Team: {team['average_distance_travelled_per_team']}")
        print(f"Average Distance per Game: {team['average_distance_travelled_per_game']}")
        print(f"Total Distance Travelled: {team['total_distance_travelled']}")
        print(f"Longest Distance Travelled by a Team: {team['longest_distance_travelled_by_a_team']}")
        print(f"Fixture with Longest Distance: {team['fixture_with_longest_distance']}")

def run_new_format(runs):
    with alive_bar(runs, force_tty=True) as bar:
        for x in range(runs):
            run_python_script('./Pre-Tournement Sorting/CSV Contents Clear.py')
            run_python_script('./Pre-Tournement Sorting/League Rankings Simulator.py')
            run_python_script('./Pre-Tournement Sorting/Titleholders_Selector.py')
            run_python_script('./Pre-Tournement Sorting/League Teams Sorter.py')
            run_python_script('./Pre-Tournement Sorting/Champions Path Teams Sorter.py')
            run_python_script('./Pre-Tournement Sorting/Champions Path Balance Checking.py')
            run_python_script('./Qualification Rounds/Champions_Path_Round_1_Simulator.py')
            run_python_script('./Qualification Rounds/Champions_Path_Round_2_Simulator.py')
            run_python_script('./Qualification Rounds/Champions_Path_Round_3_Simulator.py')
            run_python_script('./Qualification Rounds/Champions_Path_Play_off_Round_Simulator.py')
            run_python_script('./Pre-Tournement Sorting/League Path Teams Sorter.py')
            run_python_script('./Qualification Rounds/League_Path_Round_2_Simulator.py')
            run_python_script('./Qualification Rounds/League_Path_Round_3_Simulator.py')
            run_python_script('./Qualification Rounds/League_Path_Play_off_Round_Simulator.py')
            run_python_script('League Stage/League_Stage_Pot_Seeding.py')
            run_python_script('League Stage/League_Stage_Fixture_Generator.py')
            run_python_script('./League Stage/League_Stage_Simulator.py')
            run_python_script('./League Stage/League_Table_Generator.py')
            run_python_script('./Knockout Round/Knockout_Round_Simulator.py')
            run_python_script('Distance Calculation/league_stage_and_poko_fixtures_concatenater.py')
            run_python_script('./Distance Calculation/fixture_distance_calculator.py')
            run_python_script('./Distance Calculation/distance_stats_calculator.py')
            run_python_script('./Distance Calculation/per_run_distance.py')
            run_python_script('./Statistics/Qualifying Stats/qualification_round_stats.py')
            bar()

settings_choice=input("Would you like to view settings? Y/N: ")
if settings_choice.lower() == ("y"):
    settings_choice2=input("""1. Update UEFA Coefficents (NOT RECOMMENDED)
    2.Update distance matrix""")
    if settings_choice2 == ("1"):
        update_coefficents()
    elif settings_choice2 == ("2"):
        update_matrix()
else:
    runs=int(input("Enter amount of runs: "))
    clear_stats=input("Would you like to clear stats? Y/N: ")
    if clear_stats.lower()==("y"):
        run_python_script('./Statistics/statistics_clear.py')
    run_new_format(runs)
    total_stats()