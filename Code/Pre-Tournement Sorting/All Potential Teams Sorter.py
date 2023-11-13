import pandas as pd

# Define the path to your file
file_path = '../../Teams/UEFA Coefficients/all_potential_teams.csv'

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Convert the 'uefa_coefficient' column to numeric type (float), just in case it's not
df['uefa_coefficient'] = pd.to_numeric(df['uefa_coefficient'], errors='coerce')

# Sort the DataFrame based on 'uefa_coefficient' column, in descending order
df_sorted = df.sort_values(by='uefa_coefficient', ascending=False)

# Drop the index column by resetting it before saving to CSV
df_sorted.reset_index(drop=True, inplace=True)

# Save the sorted DataFrame back to a CSV file, in the same directory as the original
sorted_file_path = '../../Teams/UEFA Coefficients/all_potential_teams.csv'
df_sorted.to_csv(sorted_file_path, index=False)
