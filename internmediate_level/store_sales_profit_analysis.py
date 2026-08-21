import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------
# 1. Load and inspect data
# ---------------------------
path = r'c:\Users\Lenovo\Desktop\my all\code\shadowfox\internmediate_level\Sample-Superstore.csv'
df = pd.read_csv(path, encoding='latin1')

df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

print('Dataset shape:', df.shape)
print('\nColumns:')
print(df.columns.tolist())
print('\nData types:')
print(df.dtypes)
print('\nMissing values:')
print(df.isna().sum())
print('\nDuplicate rows:', df.duplicated().sum())
print('\nFirst 5 rows:')
print(df.head().to_string(index=False))

# ---------------------------
# 2. Basic statistics
# ---------------------------
numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit']
print('\nSummary statistics:')
print(df[numeric_cols].describe().to_string())

# KPI calculations
sales_total = df['Sales'].sum()
profit_total = df['Profit'].sum()
margin = profit_total / sales_total
print(f'\nTotal Sales: ${sales_total:,.2f}')
print(f'Total Profit: ${profit_total:,.2f}')
print(f'Profit Margin: {margin:.2%}')
print(f'Number of profit-loss rows: {(df["Profit"] < 0).sum()}')

# ---------------------------
# 3. Sales and profit by region
# ---------------------------
region_sales = df.groupby('Region', as_index=False)['Sales'].sum().sort_values('Sales', ascending=False)
region_profit = df.groupby('Region', as_index=False)['Profit'].sum().sort_values('Profit', ascending=False)

print('\nRegion Sales:')
print(region_sales.to_string(index=False))
print('\nRegion Profit:')
print(region_profit.to_string(index=False))

# ---------------------------
# 4. Sales and profit by category
# ---------------------------
category_sales = df.groupby('Category', as_index=False)['Sales'].sum().sort_values('Sales', ascending=False)
category_profit = df.groupby('Category', as_index=False)['Profit'].sum().sort_values('Profit', ascending=False)

print('\nCategory Sales:')
print(category_sales.to_string(index=False))
print('\nCategory Profit:')
print(category_profit.to_string(index=False))

# ---------------------------
# 5. Sales and profit by segment
# ---------------------------
segment_sales = df.groupby('Segment', as_index=False)['Sales'].sum().sort_values('Sales', ascending=False)
segment_profit = df.groupby('Segment', as_index=False)['Profit'].sum().sort_values('Profit', ascending=False)

print('\nSegment Sales:')
print(segment_sales.to_string(index=False))
print('\nSegment Profit:')
print(segment_profit.to_string(index=False))

# ---------------------------
# 6. Best and worst subcategories
# ---------------------------
subcat_profit = df.groupby('Sub-Category', as_index=False)['Profit'].sum().sort_values('Profit', ascending=False)
print('\nTop 10 profit sub-categories:')
print(subcat_profit.head(10).to_string(index=False))

# ---------------------------
# 7. Monthly trend analysis
# ---------------------------
monthly = df.assign(Month=df['Order Date'].dt.to_period('M').astype(str)).groupby('Month').agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum')
).sort_index()

print('\nMonthly sales and profit:')
print(monthly.head(10).to_string())

# ---------------------------
# 8. Correlation and customer insights
# ---------------------------
print(f'\nCorrelation between Sales and Profit: {df["Sales"].corr(df["Profit"]):.4f}')

customer_sales = df.groupby('Customer Name', as_index=False)['Sales'].sum().sort_values('Sales', ascending=False)
print('\nTop 5 customers by sales:')
print(customer_sales.head(5).to_string(index=False))

# ---------------------------
# 9. Data visualization
# ---------------------------
plt.figure(figsize=(10, 6))
plt.bar(region_sales['Region'], region_sales['Sales'], color='steelblue')
plt.title('Sales by Region')
plt.xlabel('Region')
plt.ylabel('Sales')
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.bar(region_profit['Region'], region_profit['Profit'], color='darkgreen')
plt.title('Profit by Region')
plt.xlabel('Region')
plt.ylabel('Profit')
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.bar(category_profit['Category'], category_profit['Profit'], color='tomato')
plt.title('Profit by Category')
plt.xlabel('Category')
plt.ylabel('Profit')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
monthly.plot(kind='line', marker='o', figsize=(12, 6))
plt.title('Monthly Sales and Profit Trend')
plt.xlabel('Month')
plt.ylabel('Amount')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='Sales', y='Profit', alpha=0.6)
plt.title('Sales vs Profit')
plt.xlabel('Sales')
plt.ylabel('Profit')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
subcat_profit.head(10).plot.bar(x='Sub-Category', y='Profit', color='purple')
plt.title('Top 10 Sub-Categories by Profit')
plt.xlabel('Sub-Category')
plt.ylabel('Profit')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---------------------------
# 10. Final insight summary
# ---------------------------
print('\nFinal insights:')
print('- West and East regions generate the highest sales and profit.')
print('- Technology is the best-performing category by profit, followed by Office Supplies.')
print('- Consumer segment contributes the largest sales and profit.')
print('- The strongest profit sub-categories are Copiers, Phones, and Accessories.')
print('- There are 1,871 orders with negative profit, which indicates loss-making transactions that should be reviewed.')
print('- Sales and profit are positively correlated, but the relationship is moderate (r ≈ 0.479).')
