import sqlite3
import pandas as pd

from src.analytics.cashflow_kpis import (
    capital_allocation_pattern,
    cfo_quality_score
)

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql("""
SELECT
    cf.company_id,
    cf.year,
    cf.operating_activity,
    cf.investing_activity,
    cf.financing_activity,
    pnl.net_profit
FROM cashflow cf
LEFT JOIN profitandloss pnl
ON cf.company_id = pnl.company_id
AND cf.year = pnl.year
""", conn)

rows = []

for _, row in df.iterrows():

    quality = cfo_quality_score(
        row["operating_activity"],
        row["net_profit"] if pd.notna(row["net_profit"]) else 0
    )

    pattern = capital_allocation_pattern(
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"],
        quality
    )

    rows.append({
        "company_id": row["company_id"],
        "year": row["year"],
        "cfo_sign": "+" if row["operating_activity"] >= 0 else "-",
        "cfi_sign": "+" if row["investing_activity"] >= 0 else "-",
        "cff_sign": "+" if row["financing_activity"] >= 0 else "-",
        "pattern_label": pattern
    })

pd.DataFrame(rows).to_csv(
    "output/capital_allocation.csv",
    index=False
)

print("capital_allocation.csv generated")