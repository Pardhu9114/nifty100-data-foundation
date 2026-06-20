import sqlite3

conn = sqlite3.connect("db/nifty100.db")

tables = [
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

print("\nTABLE COUNTS")
print("=" * 40)

for table in tables:
    count = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(f"{table:20s} {count}")

print("\nFK CHECK")
print("=" * 40)

fk = conn.execute(
    "PRAGMA foreign_key_check"
).fetchall()

print("Violations:", len(fk))

for row in fk[:20]:
    print(row)