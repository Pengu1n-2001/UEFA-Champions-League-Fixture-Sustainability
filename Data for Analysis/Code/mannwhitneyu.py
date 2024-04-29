import pandas as pd
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the Excel file
file_path = '../Excel Documents/Extremities test.xlsx'  # Ensure the file path matches where you've stored the file locally
data = pd.read_excel(file_path, sheet_name='Tests')

# Define the columns for the Random group and comparison groups
random_data = data['Unnamed: 4'].dropna()  # Assuming 'Unnamed: 4' contains the numeric data for the Random group
comparison_columns = {
    '': 'Unnamed: 9',
    'O': 'Unnamed: 14',
    'T': 'Unnamed: 19',
    'Y': 'Unnamed: 24',
    'AD': 'Unnamed: 29',
    'AI': 'Unnamed: 34',
    'AN': 'Unnamed: 39'
}

# Perform Mann-Whitney U Test for each comparison group and store results
results = {}
for col_letter, actual_col in comparison_columns.items():
    group_data = data[actual_col].dropna()
    if not group_data.empty:
        stat, p_value = mannwhitneyu(random_data, group_data, alternative='two-sided')
        results[col_letter] = (stat, p_value)
        print(f'Comparison between Random (Column E) and Column {col_letter}: U Statistic: {stat}, P-value: {p_value}')

# Setting up the figure for the box plot
plt.figure(figsize=(12, 8))
sns.set(style="whitegrid")

# Data preparation for the box plot
boxplot_data = [random_data]  # Start with the Random group data
labels = ['Random','Fitness-Proportionate', 'Greedy','Greedy-ε 0.1','Greedy-ε 0.25','Greedy-ε 0.5','Greedy-ε 0.75','Greedy-ε 0.9']  # Start with the Random group label

# Append other groups' data for the box plot
for label, col in comparison_columns.items():
    boxplot_data.append(data[col].dropna())

# Create and display the box plot
sns.boxplot(data=boxplot_data)
plt.xticks(range(len(labels)), labels)  # Set the group labels on the x-axis
plt.title('Distribution of Distances for varying optimisation algorithms')
plt.xlabel('Sorting Algorithm')
plt.ylabel('Total Travelled Distance by all teams in the League Stage')

plt.show()
