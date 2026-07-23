import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA

# Load scaled features
features = pd.read_csv("output/scaled_features.csv")

# Load cluster assignments
clusters = pd.read_csv("output/company_clusters.csv")

# Merge
df = features.merge(
    clusters[["company_id", "cluster"]],
    on="company_id"
)

# ML Features
X = df.drop(columns=["company_id", "broad_sector", "cluster"])

# PCA
pca = PCA(n_components=2, random_state=42)

components = pca.fit_transform(X)

plot_df = pd.DataFrame({
    "PC1": components[:, 0],
    "PC2": components[:, 1],
    "cluster": df["cluster"],
    "company_id": df["company_id"]
})

# Plot
plt.figure(figsize=(10, 7))

for cluster in sorted(plot_df["cluster"].unique()):
    subset = plot_df[plot_df["cluster"] == cluster]

    plt.scatter(
        subset["PC1"],
        subset["PC2"],
        label=f"Cluster {cluster}"
    )

# Label each company
for _, row in plot_df.iterrows():
    plt.text(
        row["PC1"],
        row["PC2"],
        row["company_id"],
        fontsize=6
    )

plt.title("Company Clusters (PCA)")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "output/company_clusters_pca.png",
    dpi=300
)

plt.show()

print("\nPCA visualization saved to output/company_clusters_pca.png")