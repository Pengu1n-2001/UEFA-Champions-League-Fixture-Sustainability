import csv
import random

def read_teams(file_path):
    teams = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            teams.append(row)
    return teams

def choose_random_teams(pairs, teams):
    chosen = []
    non_chosen = []
    for pair in pairs:
        team1 = teams[pair[0] - 1]
        team2 = teams[pair[1] - 1]
        selected = random.choice([team1, team2])
        chosen.append(selected)
        non_chosen.append(team2 if selected == team1 else team1)
    return chosen, non_chosen

def determine_winner(matchup):
    total_coefficient = sum(float(team['uefa_coefficient']) for team in matchup)
    random_num = random.uniform(0.001, total_coefficient)
    current_sum = 0
    for team in matchup:
        current_sum += float(team['uefa_coefficient'])
        if random_num <= current_sum:
            return team

def create_match(home_team, away_team, match_label):
    winner = determine_winner([home_team, away_team])
    return {
        'match': match_label,
        'home_team': home_team['team_name'],
        'home_team_coefficient': home_team['uefa_coefficient'],
        'home_team_city': home_team['city'],
        'home_team_association': home_team['association'],
        'away_team': away_team['team_name'],
        'away_team_coefficient': away_team['uefa_coefficient'],
        'away_team_city': away_team['city'],
        'away_team_association': away_team['association'],
        'result': winner['team_name']
    }

def find_team_by_name(team_name, teams):
    for team in teams:
        if team['team_name'] == team_name:
            return team
    return None

def write_results(file_path, results):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'match', 'home_team', 'home_team_coefficient', 'home_team_city', 'home_team_association',
            'away_team', 'away_team_coefficient', 'away_team_city', 'away_team_association', 'result'
        ])
        writer.writeheader()
        writer.writerows(results)

def tournament():
    # File paths
    input_file = '../../Fixtures, Tables and Results/League Stage/league_stage_table.csv'
    output_file = '../../Fixtures, Tables and Results/Knockout Stage/knockout_stage_results.csv'

    # Read teams from CSV
    teams = read_teams(input_file)

    # Tournament stages and pairing information
    ko_po_pairs = [(15, 16), (17, 18), (9, 10), (23, 24), (11, 12), (21, 22), (13, 14), (19, 20)]
    r16_seeds = [(1, 2), (7, 8), (5, 6), (3, 4)]

    # KO-PO Stage
    chosen_teams, non_chosen_teams = choose_random_teams(ko_po_pairs, teams)
    ko_po_matchups = [
        (chosen_teams[0], non_chosen_teams[1]),
        (chosen_teams[2], non_chosen_teams[3]),
        (chosen_teams[4], non_chosen_teams[5]),
        (chosen_teams[6], non_chosen_teams[7]),
        (non_chosen_teams[6], chosen_teams[7]),
        (non_chosen_teams[4], chosen_teams[5]),
        (non_chosen_teams[2], chosen_teams[3]),
        (non_chosen_teams[0], chosen_teams[1])
    ]
    ko_po_results = [create_match(*matchup, f'KO-PO {i+1}') for i, matchup in enumerate(ko_po_matchups)]

    # R16 Stage
    chosen_r16, non_chosen_r16 = choose_random_teams(r16_seeds, teams)
    r16_matchups = [
        (chosen_r16[0], find_team_by_name(ko_po_results[0]['result'], teams)),
        (chosen_r16[1], find_team_by_name(ko_po_results[1]['result'], teams)),
        (chosen_r16[2], find_team_by_name(ko_po_results[2]['result'], teams)),
        (chosen_r16[3], find_team_by_name(ko_po_results[3]['result'], teams)),
        (non_chosen_r16[3], find_team_by_name(ko_po_results[4]['result'], teams)),
        (non_chosen_r16[2], find_team_by_name(ko_po_results[5]['result'], teams)),
        (non_chosen_r16[1], find_team_by_name(ko_po_results[6]['result'], teams)),
        (non_chosen_r16[0], find_team_by_name(ko_po_results[7]['result'], teams))
    ]
    r16_results = [create_match(*matchup, f'R16-M{i + 1}') for i, matchup in enumerate(r16_matchups)]

    # QF Stage
    qf_matchups = [
        (find_team_by_name(r16_results[0]['result'], teams), find_team_by_name(r16_results[1]['result'], teams)),
        (find_team_by_name(r16_results[2]['result'], teams), find_team_by_name(r16_results[3]['result'], teams)),
        (find_team_by_name(r16_results[4]['result'], teams), find_team_by_name(r16_results[5]['result'], teams)),
        (find_team_by_name(r16_results[6]['result'], teams), find_team_by_name(r16_results[7]['result'], teams))
    ]
    qf_results = [create_match(*matchup, f'QF-{i+1}') for i, matchup in enumerate(qf_matchups)]

    # SF Stage
    sf_matchups = [
        (find_team_by_name(qf_results[0]['result'], teams), find_team_by_name(qf_results[1]['result'], teams)),
        (find_team_by_name(qf_results[2]['result'], teams), find_team_by_name(qf_results[3]['result'], teams))
    ]
    sf_results = [create_match(*matchup, f'SF-{i+1}') for i, matchup in enumerate(sf_matchups)]

    # Final Stage
    final_matchup = (find_team_by_name(sf_results[0]['result'], teams), find_team_by_name(sf_results[1]['result'], teams))
    final_result = [create_match(*final_matchup, 'Final')]

    # Combine all results
    all_results = ko_po_results + r16_results + qf_results + sf_results + final_result

    # Write results to CSV
    write_results(output_file, all_results)

# Run the tournament
tournament()
