import requests
import json
import pandas as pd
url = 'https://comp.uefa.com/v2/coefficients?coefficientType=MEN_CLUB&coefficientRange=OVERALL&seasonYear=2024&page=1&pagesize=500&language=EN'
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.RequestException as e:
    print(f'Could not Update UEFA Co-efficients as an error occurred: {e}')
data = response.json()
with open('../Teams/UEFA Coefficients/UEFA_club_coefficients.json', 'w', encoding='UTF-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
df = pd.read_csv('../Teams/UEFA Coefficients/all_potential_teams.csv')
with open('../Teams/UEFA Coefficients/UEFA_club_coefficients.json', 'r', encoding='utf-8') as f:
    json_text = f.read()
    json_data = json.loads(json_text)
coefficients = {(member['member']['displayName'],
                 member['member']['displayOfficialName'],
                 member['member']['displayNameShort']): member['overallRanking']['totalValue']
                for member in json_data['data']['members']}
for index, row in df.iterrows():
    team_name = row['team_name']
    coefficient = next((value for names, value in coefficients.items() if team_name in names), None)
    if coefficient is not None:
        df.at[index, 'uefa_coefficient'] = coefficient
df.to_csv('../Teams/UEFA Coefficients/all_potential_teams.csv', index=False)