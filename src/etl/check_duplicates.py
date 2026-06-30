import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow"
]

for table in tables:

    print("\n" + "=" * 50)
    print(table)

    df = pd.read_sql(f"""
        SELECT
            company_id,
            year,
            COUNT(*) AS cnt
        FROM {table}
        GROUP BY company_id, year
        HAVING COUNT(*) > 1
    """, conn)

    print("Duplicate keys:", len(df))

    if not df.empty:
        print(df.head(20))

conn.close()