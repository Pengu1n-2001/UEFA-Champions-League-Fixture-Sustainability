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

def city_key_check():
    run_python_script('./Distance Calculation/city_key_check.py')
def total_stats(type):
    if type == 1:
        file_path = '../Fixtures, Tables and Results/Stats/total_distance_analysis.csv'
    elif type == 2:
        file_path = '../Alternative Formats/Current Groupstage UCL Format/Stats/year_distance_analysis.csv'
    elif type == 3:
        file_path = '../Alternative Formats/6 Game Swiss with POKO/Stats/total_distance_analysis.csv'
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        teams = [row for row in reader]
    for team in teams:
        if type == 2:
            print(f"{team[next(iter(team))]}")
        print(f"Average Distance per Team (one-way travel to away games): {team['average_distance_travelled_per_team']} km")
        print(f"Average Distance per Game (one-way travel to away games): {team['average_distance_travelled_per_game']} km")
        print(f"Total Distance Travelled (one-way): {team['total_distance_travelled']} km")
        print(f"Longest Distance Travelled by a Team (one-way): {team['longest_distance_travelled_by_a_team']} km")
        print(f"Fixture with Longest Distance (one-way): {team['fixture_with_longest_distance']} km")

def run_new_format(runs):
    sim_type = 1
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
            run_python_script('./Statistics/total_statistics.py')
            bar()
    total_stats(sim_type)

def run_current_format():
    sim_type = 2
    run_python_script('../Alternative Formats/Current Groupstage UCL Format/Code/groupstage_fixture_generator.py')
    run_python_script('../Alternative Formats/Current Groupstage UCL Format/Code/fixture_distance_calculator.py')
    run_python_script('../Alternative Formats/Current Groupstage UCL Format/Code/distance_stats_calculator.py')
    run_python_script('../Alternative Formats/Current Groupstage UCL Format/Code/per_year_distance.py')
    total_stats(sim_type)

def run_6_game_swiss(runs):
    sim_type = 3
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
            run_python_script('../Alternative Formats/6 Game Swiss with POKO/Code/Simulation/switch_teams_to_format.py')
            run_python_script('../Alternative Formats/6 Game Swiss with POKO/Code/Simulation/League_Stage_Pot_Seeding.py')
            run_python_script('../Alternative Formats/6 Game Swiss with POKO/Code/Simulation/League_Stage_Fixture_Generator.py')
            run_python_script('../Alternative Formats/6 Game Swiss with POKO/Code/Simulation/League_Stage_Simulator.py')
            run_python_script('../Alternative Formats/6 Game Swiss with POKO/Code/Simulation/League_Table_Generator.py')
            run_python_script('../Alternative Formats/6 Game Swiss with POKO/Code/Simulation/Knockout_Round_Simulator.py')
            run_python_script('../Alternative Formats/6 Game Swiss with POKO/Code/Distance Calculation/league_stage_and_poko_fixtures_concatenater.py')
            run_python_script('../Alternative Formats/6 Game Swiss with POKO/Code/Distance Calculation/fixture_distance_calculator.py')
            run_python_script('../Alternative Formats/6 Game Swiss with POKO/Code/Distance Calculation/distance_stats_calculator.py')
            run_python_script('../Alternative Formats/6 Game Swiss with POKO/Code/Distance Calculation/per_run_distance.py')
            run_python_script('../Alternative Formats/6 Game Swiss with POKO/Code/Distance Calculation/total_statistics.py')
            bar()
    total_stats(sim_type)





while 1 == 1:
    settings_choice=input("Would you like to view settings? Y/N: ")
    if settings_choice.lower() == ("y"):
        settings_choice2=input("""1.Update UEFA Coefficents (NOT RECOMMENDED)
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
1. Default Upcoming Swiss Format (randomised draws)
2. Current Group-stage Format Analysis (Last 3 years)
3. 6 Game Swiss with POKO (randomised draws)    
4. ALTERNATIVE FORMAT 2 - COMING SOON
5. ALTERNATIVE FORMAT 3 - COMING SOON
"""))
        if simulation_type == 1:
            print("Now running Default Upcoming Swiss Format")
            runs=int(input("Enter amount of runs: "))
            run_new_format(runs)
        elif simulation_type == 2:
            print("Now running Current Group-stage Format Analysis (Last 3 years)")
            run_current_format()
        elif simulation_type == 3:
            print('Now running 6 Game Swiss with POKO (randomised draws)')
            runs = int(input("Enter amount of runs: "))
            run_6_game_swiss(runs)
        restart = input("Would you like to re-run the program? Y/N: ")
        if restart.lower() == ("n"):
            break
