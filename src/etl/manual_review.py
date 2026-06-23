import sqlite3

companies = [
    "ABB",
    "ADANIENT",
    "HDFCBANK",
    "RELIANCE",
    "TCS"
]

conn = sqlite3.connect("db/nifty100.db")

for company in companies:

    print("\n" + "=" * 60)
    print(company)

    pnl = conn.execute("""
        SELECT COUNT(*)
        FROM profitandloss
        WHERE company_id = ?
    """, (company,)).fetchone()[0]

    bs = conn.execute("""
        SELECT COUNT(*)
        FROM balancesheet
        WHERE company_id = ?
    """, (company,)).fetchone()[0]

    cf = conn.execute("""
        SELECT COUNT(*)
        FROM cashflow
        WHERE company_id = ?
    """, (company,)).fetchone()[0]

    docs = conn.execute("""
        SELECT COUNT(*)
        FROM documents
        WHERE company_id = ?
    """, (company,)).fetchone()[0]

    print("P&L Records      :", pnl)
    print("Balance Records  :", bs)
    print("Cashflow Records :", cf)
    print("Documents        :", docs)

conn.close()