import pandas as pd

file_path = "data/raw/financial_ratios.xlsx"

df = pd.read_excel(file_path)

print("\nCOLUMNS:")
print(df.columns.tolist())

print("\nSHAPE:")
print(df.shape)

print("\nFIRST 5 ROWS:")
print(df.head().to_string())