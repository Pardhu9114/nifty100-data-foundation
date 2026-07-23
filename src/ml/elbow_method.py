import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Load scaled features
df = pd.read_csv("output/scaled_features.csv")

# Keep only numerical columns
X = df.drop(columns=["company_id", "broad_sector"])

inertia = []

k_values = range(2, 11)

for k in k_values:
    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X)
    inertia.append(model.inertia_)

# Plot Elbow Curve
plt.figure(figsize=(8, 5))
plt.plot(k_values, inertia, marker="o")
plt.title("Elbow Method")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")
plt.grid(True)

plt.savefig("output/elbow_curve.png", dpi=300)
plt.show()

print("\nElbow curve saved to output/elbow_curve.png")