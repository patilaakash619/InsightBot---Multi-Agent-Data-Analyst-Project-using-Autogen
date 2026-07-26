import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('uploads/sales.csv')

# Calculate revenue per unit for each row
df['revenue_per_unit'] = df['revenue'] / df['units']

# Group the data by product and calculate the average revenue per unit for each product
avg_revenue_per_unit = df.groupby('product')['revenue_per_unit'].mean().reset_index()

# Sort the products by their average revenue per unit in descending order
avg_revenue_per_unit = avg_revenue_per_unit.sort_values(by='revenue_per_unit', ascending=False)

# Print the product with the highest revenue per unit
print("The product with the highest revenue per unit is:", avg_revenue_per_unit.iloc[0]['product'])
print("The average revenue per unit for this product is:", avg_revenue_per_unit.iloc[0]['revenue_per_unit'])

# Plot a bar chart with the products on the x-axis and their average revenue per unit on the y-axis
plt.figure(figsize=(10,6))
plt.bar(avg_revenue_per_unit['product'], avg_revenue_per_unit['revenue_per_unit'])
plt.xlabel('Product')
plt.ylabel('Average Revenue per Unit')
plt.title('Average Revenue per Unit by Product')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('outputs/average_revenue_per_unit.png')

# Print key numeric findings
print("Average revenue per unit for all products:")
print(avg_revenue_per_unit['revenue_per_unit'])