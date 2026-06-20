import pandas as pd
import sqlite3
from pathlib import Path

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

LOAD_ORDER = [
    "companies",
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

MISSING_COMPANIES = [
    "AGTL",
    "ULTRACEMCO",
    "UNIONBANK",
    "UNITDSPR",
    "VBL",
    "VEDL",
    "WIPRO",
    "ZOMATO",
    "ZYDUSLIFE"
]

audit_rows = []

Path("output").mkdir(exist_ok=True)

conn = sqlite3.connect(DB_FILE)
conn.execute("PRAGMA foreign_keys = ON")

for table in LOAD_ORDER:

    conn.execute(f"DELETE FROM {table}")

    file_path = f"data/raw/{table}.xlsx"

    df = pd.read_excel(
        file_path,
        header=HEADER_MAP[table]
    )

    df.to_sql(
        table,
        conn,
        if_exists="append",
        index=False
    )

    if table == "companies":

        for company in MISSING_COMPANIES:
            conn.execute("""
                INSERT OR IGNORE INTO companies
                (id, company_name)
                VALUES (?, ?)
            """, (company, company))

    audit_rows.append({
        "table_name": table,
        "rows_loaded": len(df)
    })

    print(f"Loaded {table}: {len(df)} rows")

conn.commit()
conn.close()

audit_df = pd.DataFrame(audit_rows)

audit_df.to_csv(
    "output/load_audit.csv",
    index=False
)

print("\nPipeline completed successfully")