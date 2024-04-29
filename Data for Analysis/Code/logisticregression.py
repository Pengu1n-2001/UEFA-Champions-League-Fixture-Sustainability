import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats import norm
import matplotlib.pyplot as plt

# Load data from a CSV file
file_path = '../Excel Documents/Sustainable Fixtures.csv'
data = pd.read_csv(file_path, encoding='latin1')

# Clean and prepare the data
data = data.drop(columns=['Unnamed: 3', 'Unnamed: 4', 'Run']).dropna()
real_data = data[['Team', 'UEFA Coefficient', 'Qualified']]
simulated_data = data[['Team (Simulated)', 'UEFA Coefficient (Simulated)', 'Qualified(Simulated)']].rename(
    columns={'Team (Simulated)': 'Team', 'UEFA Coefficient (Simulated)': 'UEFA Coefficient', 'Qualified(Simulated)': 'Qualified'})

# Adding intercept for logistic regression
real_data['Intercept'] = 1
simulated_data['Intercept'] = 1

# Logistic regression for real data
logit_model_real = sm.Logit(real_data['Qualified'], real_data[['Intercept', 'UEFA Coefficient']])
result_real = logit_model_real.fit(disp=0)

# Logistic regression for simulated data
logit_model_simulated = sm.Logit(simulated_data['Qualified'], simulated_data[['Intercept', 'UEFA Coefficient']])
result_simulated = logit_model_simulated.fit(disp=0)

# Extracting coefficients and standard errors
coef_real, se_real = result_real.params['UEFA Coefficient'], result_real.bse['UEFA Coefficient']
coef_simulated, se_simulated = result_simulated.params['UEFA Coefficient'], result_simulated.bse['UEFA Coefficient']

# Calculating the z-statistic for comparing the coefficients
z = (coef_real - coef_simulated) / np.sqrt(se_real**2 + se_simulated**2)
p_value = 2 * (1 - norm.cdf(np.abs(z)))  # two-tailed test

# Define a range of UEFA coefficient values for plotting
x_range = np.linspace(data['UEFA Coefficient'].min(), data['UEFA Coefficient'].max(), 500)

# Calculate the predicted probabilities for real and simulated data
prob_real = 1 / (1 + np.exp(-(result_real.params['Intercept'] + result_real.params['UEFA Coefficient'] * x_range)))
prob_simulated = 1 / (1 + np.exp(-(result_simulated.params['Intercept'] + result_simulated.params['UEFA Coefficient'] * x_range)))

# Plotting the logistic regression curves
plt.figure(figsize=(10, 6))
plt.plot(x_range, prob_real, label='Real Data', color='blue')
plt.plot(x_range, prob_simulated, label='Simulated Data', color='red')
plt.scatter(real_data['UEFA Coefficient'], real_data['Qualified'], color='blue', alpha=0.5, marker='o', label='Real Data Points')
plt.scatter(simulated_data['UEFA Coefficient'], simulated_data['Qualified'], color='red', alpha=0.5, marker='x', label='Simulated Data Points')
plt.title('Logistic Regression Analysis of UEFA Coefficients')
plt.xlabel('UEFA Coefficient')
plt.ylabel('Probability of Qualification')
plt.legend()
plt.grid(True)
plt.show()

print(f"Z-statistic: {z}")
print(f"P-value: {p_value}")
