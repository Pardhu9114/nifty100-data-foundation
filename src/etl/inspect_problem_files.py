import pandas as pd

problem_files = [
    "financial_ratios.xlsx",
    "sectors.xlsx",
    "peer_groups.xlsx",
    "stock_prices.xlsx",
    "market_cap.xlsx"
]

for file in problem_files:
    print("\n" + "=" * 80)
    print(file)

    df = pd.read_excel(
        f"data/raw/{file}",
        header=None
    )

    print(df.head(5))