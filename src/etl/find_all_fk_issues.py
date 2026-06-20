import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "financial_ratios",
    "sectors",
    "peer_groups",
    "stock_prices",
    "market_cap"
]

for table in tables:
    try:
        query = f"""
        SELECT DISTINCT company_id
        FROM {table}
        WHERE company_id NOT IN (
            SELECT id FROM companies
        )
        ORDER BY company_id
        """

        df = pd.read_sql_query(query, conn)

        if len(df) > 0:
            print("\n" + "=" * 60)
            print(table)
            print(df)
            print("Missing:", len(df))

    except Exception as e:
        print(table, e)

conn.close()