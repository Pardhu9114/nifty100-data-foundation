import pandas as pd

files = [
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx",
    "financial_ratios.xlsx",
    "sectors.xlsx",
    "peer_groups.xlsx",
    "stock_prices.xlsx",
    "market_cap.xlsx"
]

for file in files:
    print("\n" + "=" * 80)
    print(file)

    df = pd.read_excel(
        f"data/raw/{file}",
        header=1
    )

    print("Shape:", df.shape)
    print("Columns:")
    print(df.columns.tolist())