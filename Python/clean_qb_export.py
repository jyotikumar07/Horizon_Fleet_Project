import pandas as pd

# 1. Load the QuickBooks Excel export
# Skip the first few header rows so Python reads the actual column names
df = pd.read_excel("qb_export.xlsx", skiprows=4, nrows=25)

# 2. Clean up column names (remove any accidental spaces)
df.columns = df.columns.str.strip()

# 3. Clean up data types
df['Transaction date'] = pd.to_datetime(df['Transaction date'], errors='coerce').dt.strftime('%Y-%m-%d')
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

# 6. Save the flat, raw data table for Power BI
df.to_csv("horizon_powerbi_ready.csv", index=False)

print("🚀 Success! All sub-totals removed. 'horizon_powerbi_ready.csv' is ready for Power BI.")