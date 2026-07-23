import sqlite3
import pandas as pd

DB = "db/nifty100.db"

conn = sqlite3.connect(DB)

company = input("Enter Company ID: ").strip().upper()

# Find company cluster
cluster_query = """
SELECT cluster
FROM company_clusters
WHERE company_id = ?
"""

cluster_df = pd.read_sql_query(
    cluster_query,
    conn,
    params=(company,)
)

if cluster_df.empty:
    print(f"\nCompany '{company}' not found.")
    conn.close()
    exit()

cluster = int(cluster_df.iloc[0]["cluster"])

print(f"\n{company} belongs to Cluster {cluster}")

# Get all companies in the same cluster
recommend_query = """
SELECT
    cc.company_id,
    cc.broad_sector
FROM company_clusters cc
WHERE cc.cluster = ?
AND cc.company_id != ?
ORDER BY cc.company_id;
"""

recommendations = pd.read_sql_query(
    recommend_query,
    conn,
    params=(cluster, company)
)

conn.close()

print(f"\nFound {len(recommendations)} similar companies:\n")

print(recommendations)

recommendations.to_csv(
    f"output/recommendations_{company}.csv",
    index=False
)

print(f"\nSaved to output/recommendations_{company}.csv")