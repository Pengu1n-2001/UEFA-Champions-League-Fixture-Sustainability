import pandas as pd

# Read the Excel file
excel_file = "../Excel Documents/FYP Analysis.xlsx"
dfs = pd.read_excel(excel_file, sheet_name=None)

# Initialize a dictionary to store the results
results = {}

# Loop through each sheet (excluding the first one)
for sheet_name, df in dfs.items():
    if sheet_name == "Sheet1":  # Skip the first sheet
        continue

    # Extract the part that indicates 'save_state_2' from 'Source.Name' column
    df['save_state'] = df['Source.Name'].str.extract(r'(save_state_2)')

    # Filter the data to include only save_state_2 for each algorithm
    df_save_state_2 = df[df['save_state'] == 'save_state_2']

    # Group by replicate number
    grouped = df_save_state_2.groupby('replicate_number')

    # Initialize a list to store the unique matchups for each replicate
    unique_matchups = []

    # Iterate over each replicate
    for replicate, group_df in grouped:
        # Count unique matchups
        unique_matchups.append(group_df[['home_team', 'away_team']].apply(frozenset, axis=1).unique())

    # Calculate the percentage of common matchups across the 10 replicates
    common_matchups_count = len(set.intersection(*map(set, unique_matchups)))
    total_unique_matchups_count = len(set.union(*map(set, unique_matchups)))
    common_matchups_percent = (common_matchups_count / total_unique_matchups_count) * 100

    # Store the results
    results[sheet_name] = common_matchups_percent

# Print the results
for algorithm, percent in results.items():
    print(f"{algorithm}: {percent:.2f}% common matchups across 10 replicates")
