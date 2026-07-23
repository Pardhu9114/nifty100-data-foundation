import sqlite3
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Load scaled features
df = pd.read_csv("output/scaled_features.csv")

# Keep identifiers
company_info = df[["company_id", "broad_sector"]]

# ML features
X = df.drop(columns=["company_id", "broad_sector"])

# Train KMeans
kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

clusters = kmeans.fit_predict(X)

# Attach cluster labels
result = company_info.copy()
result["cluster"] = clusters

# Save CSV
result.to_csv(
    "output/company_clusters.csv",
    index=False
)

# Calculate Silhouette Score
score = silhouette_score(X, clusters)

print(f"\nSilhouette Score: {score:.4f}")

print("\nCompanies per Cluster:")
print(result["cluster"].value_counts().sort_index())

print("\nFirst 10 Companies:")
print(result.head(10))

# Save to SQLite
conn = sqlite3.connect("db/nifty100.db")

result.to_sql(
    "company_clusters",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("\nCluster assignments saved to:")
print(" - output/company_clusters.csv")
print(" - SQLite table: company_clusters")


df = pd.read_csv("output/scaled_features.csv")
X = df.drop(columns=["company_id", "broad_sector"])

print("K\tSilhouette Score")

for k in range(2, 11):
    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(X)
    score = silhouette_score(X, labels)

    print(f"{k}\t{score:.4f}")