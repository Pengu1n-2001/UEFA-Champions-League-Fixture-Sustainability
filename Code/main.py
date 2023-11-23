import subprocess
import os
import sys


def run_python_script(script_path):
    python_executable = sys.executable
    absolute_script_path = os.path.abspath(script_path)
    working_directory = os.path.dirname(absolute_script_path)
    subprocess.run([python_executable, absolute_script_path], cwd=working_directory)

run_python_script('./UEFA Coefficients/UEFA_Club_Coefficients_Updater.py')
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