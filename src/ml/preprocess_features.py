import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# Load feature matrix
df = pd.read_csv("output/feature_matrix.csv")

print("Original Shape:", df.shape)

# -----------------------------
# Fill missing sector values
# -----------------------------
df["broad_sector"] = df["broad_sector"].fillna("Unknown")

# -----------------------------
# Numerical columns
# -----------------------------
numeric_cols = [
    "return_on_equity_pct",
    "debt_to_equity",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "asset_turnover",
    "free_cash_flow_cr"
]

# Fill missing numerical values with median
imputer = SimpleImputer(strategy="median")
df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

# -----------------------------
# Feature Scaling
# -----------------------------
scaler = StandardScaler()

scaled = scaler.fit_transform(df[numeric_cols])

scaled_df = pd.DataFrame(
    scaled,
    columns=numeric_cols
)

# Add company details back
scaled_df.insert(0, "company_id", df["company_id"])
scaled_df.insert(1, "broad_sector", df["broad_sector"])

print("\nScaled Dataset")
print(scaled_df.head())

print("\nShape:", scaled_df.shape)

scaled_df.to_csv(
    "output/scaled_features.csv",
    index=False
)

print("\nSaved: output/scaled_features.csv")