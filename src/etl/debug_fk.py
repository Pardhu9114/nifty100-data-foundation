import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

bad = pd.read_sql_query("""
SELECT DISTINCT company_id
FROM financial_ratios
WHERE company_id NOT IN (
    SELECT id FROM companies
)
ORDER BY company_id
""", conn)

print("Missing company IDs:")
print(bad)

print("\nCount:", len(bad))

conn.close()