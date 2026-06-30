import sqlite3

DB = "db/nifty100.db"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

log = open("output/ratio_edge_cases.log", "w")

log.write("=" * 70 + "\n")
log.write("RATIO EDGE CASE REPORT\n")
log.write("=" * 70 + "\n\n")

query = """
SELECT
    c.id,
    c.company_name,
    c.roce_percentage,
    c.roe_percentage,
    AVG(fr.return_on_equity_pct) AS computed_roe
FROM companies c
LEFT JOIN financial_ratios fr
ON c.id = fr.company_id
GROUP BY
    c.id,
    c.company_name,
    c.roce_percentage,
    c.roe_percentage
"""

rows = cursor.execute(query).fetchall()

count = 0

for row in rows:

    company = row[1]
    source_roce = row[2]
    source_roe = row[3]
    computed_roe = row[4]

    if source_roe is None or computed_roe is None:
        continue

    diff = abs(source_roe - computed_roe)

    if diff > 5:

        count += 1

        if diff > 100:
            category = "Data Source Issue"
        elif diff > 20:
            category = "Version Difference"
        else:
            category = "Formula Discrepancy"

        log.write(f"Company : {company}\n")
        log.write(f"Source ROE : {source_roe}\n")
        log.write(f"Computed ROE : {computed_roe:.2f}\n")
        log.write(f"Difference : {diff:.2f}%\n")
        log.write(f"Category : {category}\n")
        log.write("-" * 60 + "\n")

# Write summary only once
log.write("\n")
log.write("=" * 70 + "\n")
log.write(f"Total anomalies : {count}\n")
log.write("=" * 70 + "\n")

log.close()
conn.close()

print("ratio_edge_cases.log generated")
print("Total anomalies:", count)