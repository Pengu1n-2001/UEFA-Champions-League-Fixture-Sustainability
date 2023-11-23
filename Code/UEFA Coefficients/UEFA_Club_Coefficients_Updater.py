import requests
import json
import pandas as pd

url = 'https://comp.uefa.com/v2/coefficients?coefficientType=MEN_CLUB&coefficientRange=OVERALL&seasonYear=2024&page=1&pagesize=500&language=EN'

# User-Agent header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
except requests.RequestException as e:
    print(f'Could not Update UEFA Co-efficients as an error occurred: {e}')
    exit()  # Exit the script if an error occurs

data = response.json()

with open('../../Teams/UEFA Coefficients/UEFA_club_coefficients.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

df = pd.read_csv('../../Teams/UEFA Coefficients/all_potential_teams.csv')

with open('../../Teams/UEFA Coefficients/UEFA_club_coefficients.json', 'r', encoding='utf-8') as f:
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

df.to_csv('../../Teams/UEFA Coefficients/all_potential_teams.csv', index=False)
