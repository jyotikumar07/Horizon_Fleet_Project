import pandas as pd
import numpy as np

# 1. Load the messy logistics dataset
df = pd.read_csv("horizon_raw_large.csv")

# 2. Drop exact duplicate rows (Fixes the double-counting issue)
df = df.drop_duplicates()

# 3. Clean up text columns: Strip ghost spaces and force UPPERCASE
df['Vendor/Description'] = df['Vendor/Description'].str.strip().str.upper()

df['Category_Raw'] = df['Category_Raw'].str.strip().str.upper()

# 4. Standardize the Date column to a single unified format (coercing bad entries to NaT)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')

# 5.Forward fill to handle NaT values
df['Date'] = df['Date'].ffill() 

# 6. Handle missing Transaction IDs systematically by replacing NaN with a manual tag
df['Transaction_ID'] = df['Transaction_ID'].fillna('TXN-MANUAL')

# Ensure every ID starts with 'TXN-' (if it doesn't already)
df['Transaction_ID'] = df['Transaction_ID'].apply(lambda x: f"TXN-{x}" if str(x).isdigit() else x)

# Check for fuel/oil keywords and force them to be negative expenses
fuel_keywords = ['GAS', 'FUEL', 'PETROL', 'DIESEL', 'GAS STATION', 'SHELL']

# Create a matching rule: if the category OR description contains any of our keywords
is_fuel = df['Category_Raw'].str.contains('|'.join(fuel_keywords)) | df['Vendor/Description'].str.contains('|'.join(fuel_keywords)) 

# Apply the negative sign to those rows
df.loc[is_fuel, 'Amount_USD'] = -df.loc[is_fuel, 'Amount_USD'].abs()

# 7. Create a Chart of Accounts (COA) Mapping Dictionary
coa_mapping = { 'UTILITIES': 'OPERATING EXPENSES',
                'SOFTWARE_EXP': 'OPERATING EXPENSES',
                'SUPPLIES': 'OPERATING EXPENSES',
                'INSURANCE': 'OPERATING EXPENSES',
                'MISC': 'OPERATING EXPENSES',
                'FUEL': 'COST OF GOODS SOLD',
                'MAINTENANCE': 'COST OF GOODS SOLD',
                'MAINT': 'COST OF GOODS SOLD',
                'REVENUE': 'INCOME',
                'SALES': 'INCOME',
                'INCOME': 'INCOME'
                }

# 8. Create a new column called 'Financial_Statement_Class' using the map
df['Finacial_Statement_Class'] = df['Category_Raw'].map(coa_mapping)

# 9. If any category didn't match our dictionary, label it as Uncategorized
df['Finacial_Statement_Class'] = df['Finacial_Statement_Class'].fillna('UNCATEGORIZED')


gas_stations = { ''


}
# 10. Save the clean dataset
df.to_csv("horizon_clean_ledger.csv", index = False)

print("Dataset cleaned successfully")
