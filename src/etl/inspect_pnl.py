import pandas as pd

df = pd.read_excel(
    "data/raw/profitandloss.xlsx",
    header=1
)

print("Columns:")
print(df.columns.tolist())

print("\nShape:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())    