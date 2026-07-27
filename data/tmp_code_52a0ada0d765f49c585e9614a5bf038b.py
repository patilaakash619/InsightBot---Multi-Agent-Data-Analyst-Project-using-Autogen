import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('uploads/sales.csv')

# Group the data by 'region' and 'product', and calculate the sum of 'units' and 'revenue' for each group
grouped_df = df.groupby(['region', 'product']).agg({'units': 'sum', 'revenue': 'sum'}).reset_index()

# Create a pivot table that shows the total 'units' and 'revenue' for each 'product' in each 'region'
pivot_units = grouped_df.pivot(index='region', columns='product', values='units')
pivot_revenue = grouped_df.pivot(index='region', columns='product', values='revenue')

# Calculate the percentage of total 'units' and 'revenue' for each 'product' in each 'region'
pivot_units_percent = pivot_units.div(pivot_units.sum(axis=1), axis=0) * 100
pivot_revenue_percent = pivot_revenue.div(pivot_revenue.sum(axis=1), axis=0) * 100

# Print the key numeric findings
print("Total Units by Region and Product:")
print(pivot_units)
print("\nTotal Revenue by Region and Product:")
print(pivot_revenue)
print("\nPercentage of Total Units by Region and Product:")
print(pivot_units_percent)
print("\nPercentage of Total Revenue by Region and Product:")
print(pivot_revenue_percent)

# Visualize the results using a heatmap
plt.figure(figsize=(10,6))
sns.heatmap(pivot_units_percent, annot=True, cmap='Blues')
plt.title('Percentage of Total Units by Region and Product')
plt.xlabel('Product')
plt.ylabel('Region')
plt.savefig('outputs/units_heatmap.png')

plt.figure(figsize=(10,6))
sns.heatmap(pivot_revenue_percent, annot=True, cmap='Blues')
plt.title('Percentage of Total Revenue by Region and Product')
plt.xlabel('Product')
plt.ylabel('Region')
plt.savefig('outputs/revenue_heatmap.png')

# Visualize the results using a bar chart
pivot_units_percent.plot(kind='bar', figsize=(10,6))
plt.title('Percentage of Total Units by Region and Product')
plt.xlabel('Region')
plt.ylabel('Percentage')
plt.legend(title='Product')
plt.savefig('outputs/units_bar_chart.png')

pivot_revenue_percent.plot(kind='bar', figsize=(10,6))
plt.title('Percentage of Total Revenue by Region and Product')
plt.xlabel('Region')
plt.ylabel('Percentage')
plt.legend(title='Product')
plt.savefig('outputs/revenue_bar_chart.png')