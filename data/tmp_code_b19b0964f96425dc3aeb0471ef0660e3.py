import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('uploads/sales.csv')

# Group the data by 'region' and calculate the total revenue for each region
region_revenue = df.groupby('region')['revenue'].sum().reset_index()

# Sort the regions by total revenue in descending order
region_revenue = region_revenue.sort_values(by='revenue', ascending=False)

# Identify the region with the most total revenue and the region with the least total revenue
most_revenue_region = region_revenue.iloc[0]['region']
least_revenue_region = region_revenue.iloc[-1]['region']

# Print the key numeric findings
print(f"Region with the most total revenue: {most_revenue_region}")
print(f"Region with the least total revenue: {least_revenue_region}")

# Plot a bar chart to visualize the total revenue by region
plt.figure(figsize=(10,6))
plt.bar(region_revenue['region'], region_revenue['revenue'])
plt.xlabel('Region')
plt.ylabel('Total Revenue')
plt.title('Total Revenue by Region')
plt.savefig('outputs/region_revenue.png')

# Plot a pie chart to visualize the proportion of total revenue by region
plt.figure(figsize=(10,6))
plt.pie(region_revenue['revenue'], labels=region_revenue['region'], autopct='%1.1f%%')
plt.title('Proportion of Total Revenue by Region')
plt.savefig('outputs/region_revenue_pie.png')