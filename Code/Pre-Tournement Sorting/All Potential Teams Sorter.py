import pandas as pd
# creates a pandas dataframe (df)
df = pd.read_csv('../../Teams/UEFA Coefficients/all_potential_teams.csv')

# turns uefa_coefficent into a float
df['uefa_coefficient'] = pd.to_numeric(df['uefa_coefficient'], errors='coerce')

# sorts uefa_coefficent into a ranked order
df_sorted = df.sort_values(by='uefa_coefficient', ascending=False)

# drops the index column before saving
df_sorted.reset_index(drop=True, inplace=True)

# saves the csv back to the original file
df_sorted.to_csv('../../Teams/UEFA Coefficients/all_potential_teams.csv', index=False)
