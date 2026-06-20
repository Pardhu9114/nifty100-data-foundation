import pandas as pd
import sqlite3

DB_FILE = "db/nifty100.db"

HEADER_MAP = {
    "companies": 1,
    "profitandloss": 1,
    "balancesheet": 1,
    "cashflow": 1,
    "analysis": 1,
    "documents": 1,
    "prosandcons": 1,
    "financial_ratios": 0,
    "sectors": 0,
    "peer_groups": 0,
    "stock_prices": 0,
    "market_cap": 0
}

def load_table(table_name):
    file_path = f"data/raw/{table_name}.xlsx"

    df = pd.read_excel(
        file_path,
        header=HEADER_MAP[table_name]
    )

    conn = sqlite3.connect(DB_FILE)

    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()
    conn.close()

    print(f"{table_name}: {len(df)} rows loaded")