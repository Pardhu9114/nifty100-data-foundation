import sqlite3
import pandas as pd

DB = "db/nifty100.db"

conn = sqlite3.connect(DB)

query = """
WITH latest AS (
    SELECT
        company_id,
        MAX(year) AS latest_year
    FROM financial_ratios
    GROUP BY company_id
)

SELECT
    fr.company_id,
    s.broad_sector,

    fr.return_on_equity_pct,
    fr.debt_to_equity,
    fr.net_profit_margin_pct,
    fr.operating_profit_margin_pct,
    fr.asset_turnover,
    fr.free_cash_flow_cr

FROM financial_ratios fr

JOIN latest l
    ON fr.company_id = l.company_id
   AND fr.year = l.latest_year

LEFT JOIN sectors s
    ON fr.company_id = s.company_id

ORDER BY fr.company_id;
"""

df = pd.read_sql(query, conn)

conn.close()

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

df.to_csv(
    "output/feature_matrix.csv",
    index=False
)

print("\nFeature matrix saved to output/feature_matrix.csv")