import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('uploads/sales.csv')

# Convert date to datetime and extract quarter
df['date'] = pd.to_datetime(df['date'])
df['quarter'] = df['date'].dt.to_period('Q')

# Filter the data by quarter to compare sales trends
q1_df = df[df['quarter'] == '2025Q1']
q2_df = df[df['quarter'] == '2025Q2']

# Group the data by product and calculate total units sold and revenue for each quarter
q1_product_sales = q1_df.groupby('product')[['units', 'revenue']].sum().reset_index()
q2_product_sales = q2_df.groupby('product')[['units', 'revenue']].sum().reset_index()

# Calculate the percentage change in units sold and revenue for each product between quarters
product_momentum = pd.merge(q1_product_sales, q2_product_sales, on='product', suffixes=('_q1', '_q2'))
product_momentum['units_change'] = ((product_momentum['units_q2'] - product_momentum['units_q1']) / product_momentum['units_q1']) * 100
product_momentum['revenue_change'] = ((product_momentum['revenue_q2'] - product_momentum['revenue_q1']) / product_momentum['revenue_q1']) * 100

# Analyze the results to identify which products are gaining or losing momentum over the quarter
gaining_momentum = product_momentum[product_momentum['units_change'] > 0]
losing_momentum = product_momentum[product_momentum['units_change'] < 0]

# Print key numeric findings
print("Products gaining momentum:")
print(gaining_momentum)
print("\nProducts losing momentum:")
print(losing_momentum)

# Save charts to 'outputs/<name>.png'
plt.figure(figsize=(10,6))
plt.bar(gaining_momentum['product'], gaining_momentum['units_change'], label='Gaining Momentum')
plt.bar(losing_momentum['product'], losing_momentum['units_change'], label='Losing Momentum')
plt.xlabel('Product')
plt.ylabel('Percentage Change in Units Sold')
plt.title('Product Momentum')
plt.legend()
plt.savefig('outputs/product_momentum.png')

plt.figure(figsize=(10,6))
plt.bar(gaining_momentum['product'], gaining_momentum['revenue_change'], label='Gaining Momentum')
plt.bar(losing_momentum['product'], losing_momentum['revenue_change'], label='Losing Momentum')
plt.xlabel('Product')
plt.ylabel('Percentage Change in Revenue')
plt.title('Product Revenue Momentum')
plt.legend()
plt.savefig('outputs/product_revenue_momentum.png')