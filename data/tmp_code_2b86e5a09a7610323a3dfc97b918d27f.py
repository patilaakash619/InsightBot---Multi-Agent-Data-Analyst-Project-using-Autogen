import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('uploads/sales.csv')

# Convert the date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Filter the data to only include rows where the date falls within January, February, and March
df_filtered = df[(df['date'].dt.month == 1) | (df['date'].dt.month == 2) | (df['date'].dt.month == 3)]

# Group the data by month and calculate the total revenue for each month
df_grouped = df_filtered.groupby(df_filtered['date'].dt.month)['revenue'].sum().reset_index()

# Rename the columns for clarity
df_grouped.columns = ['month', 'revenue']

# Map month numbers to names
month_map = {1: 'January', 2: 'February', 3: 'March'}
df_grouped['month'] = df_grouped['month'].map(month_map)

# Calculate the month-over-month percentage change in revenue
df_grouped['percentage_change'] = df_grouped['revenue'].pct_change() * 100

# Print the key numeric findings
print("Total Revenue by Month:")
print(df_grouped)
print("\nMonth-over-Month Percentage Change in Revenue:")
print(df_grouped['percentage_change'])

# Plot a line graph to visualize the trend in revenue over the three months
plt.figure(figsize=(10,6))
plt.plot(df_grouped['month'], df_grouped['revenue'], marker='o')
plt.title('Revenue Trend Over Three Months')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.grid(True)
plt.savefig('outputs/revenue_trend.png')

# Plot a line graph to visualize the month-over-month percentage change in revenue
plt.figure(figsize=(10,6))
plt.plot(df_grouped['month'], df_grouped['percentage_change'], marker='o')
plt.title('Month-over-Month Percentage Change in Revenue')
plt.xlabel('Month')
plt.ylabel('Percentage Change')
plt.grid(True)
plt.savefig('outputs/percentage_change.png')