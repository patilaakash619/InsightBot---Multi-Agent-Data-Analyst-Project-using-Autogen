import pandas as pd
import matplotlib.pyplot as plt

# Ensure necessary libraries are installed
try:
    import seaborn as sns
except ImportError:
    print("Seaborn is not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "seaborn"])
    import seaborn as sns

# Load the data
df = pd.read_csv('uploads/sales.csv')

# Step 1: Data Cleaning
# Convert 'date' column to datetime format and set it as the index
df['date'] = pd.to_datetime(df['date'])
# df.set_index('date', inplace=True)  # Uncomment if you want to set 'date' as the index

# Verify that 'region' and 'product' columns are categorical
df['region'] = df['region'].astype('category')
df['product'] = df['product'].astype('category')

# Step 2: Calculate Revenue per Unit
df['revenue_per_unit'] = df['revenue'] / df['units']

# Step 3: Group by Region and Product
average_revenue_per_unit = df.groupby(['region', 'product'])['revenue_per_unit'].mean().reset_index()

# Step 4: Visualize the Results
plt.figure(figsize=(10, 6))
pivot_table = pd.pivot_table(df, values='revenue_per_unit', index='product', columns='region', aggfunc='mean')
pivot_table.plot(kind='bar')
plt.title('Average Revenue per Unit by Product and Region')
plt.xlabel('Product')
plt.ylabel('Average Revenue per Unit')
plt.legend(title='Region')
plt.savefig('outputs/average_revenue_per_unit.png')

# Print the key numeric findings
print(average_revenue_per_unit)