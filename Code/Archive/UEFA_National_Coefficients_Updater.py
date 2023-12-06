import requests
import pandas as pd

#This code is used to update UEFA National association Co-efficents.
#However this does not need to happen during the running of one season.
#This exists to allow use in following seasons of the UEFA Champions League.

url = 'https://comp.uefa.com/v2/coefficients?coefficientType=MEN_ASSOCIATION&coefficientRange=OVERALL&seasonYear=2024&page=1&pagesize=500&language=EN'
response = requests.get(url)
data = response.json()
excluded_associations_df = pd.read_csv('../../Teams/UEFA Coefficients/excluded_associations.csv')
excluded_association_codes = set(excluded_associations_df['association_code'])
csv_data = []
for rank, member in enumerate(data['data']['members'], start=1):
    association_name = member['member']['displayName']
    association_code = member['member']['displayTeamCode'][:3]
    coefficient = member['overallRanking']['totalValue']
    status = ''
    if association_code[:3] in excluded_association_codes:
        status = 'excluded'
    csv_data.append([rank, association_name, association_code, coefficient, status])
output_df = pd.DataFrame(csv_data, columns=['rank', 'association_name', 'association_code', 'coefficient', 'status'])
output_df.to_csv('../Teams/UEFA Coefficients/UEFA_national_coefficient_ranking.csv', index=False)
