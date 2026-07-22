import re
from pathlib import Path

import pandas as pd

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "raw" / "analysis.xlsx"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

PARSED_FILE = OUTPUT_DIR / "analysis_parsed.csv"
FAILURE_FILE = OUTPUT_DIR / "parse_failures.csv"

# -------------------------------------------------------
# Read Excel
# -------------------------------------------------------

df = pd.read_excel(
    INPUT_FILE,
    header=1
)

# -------------------------------------------------------
# Regex Pattern
# -------------------------------------------------------

pattern = re.compile(
    r"(TTM|Last\s+Year|(\d+)\s*Years?|1\s*Year)\s*:?\s*([-+]?\d+(?:\.\d+)?)\s*%",
    re.IGNORECASE,
)

# -------------------------------------------------------
# Columns to Parse
# -------------------------------------------------------

metrics = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]

parsed_rows = []
failed_rows = []

# -------------------------------------------------------
# Parse
# -------------------------------------------------------

for _, row in df.iterrows():

    company_id = row["company_id"]

    for metric in metrics:

        value = row.get(metric)

        if pd.isna(value):
            continue

        text = str(value).strip()

        match = pattern.search(text)

        if match:

            label = match.group(1).lower()

            if label == "ttm":
                period = 0
            elif label == "last year":
                period = 1
            elif label == "1 year":
                period = 1
            else:
                period = int(match.group(2))

            parsed_rows.append(
                {
                    "company_id": company_id,
                    "metric_type": metric,
                    "period_years": period,
                    "value_pct": float(match.group(3)),
                }
            )

        else:

            failed_rows.append(
                {
                    "company_id": company_id,
                    "metric_type": metric,
                    "original_text": text,
                }
            )

# -------------------------------------------------------
# Save Outputs
# -------------------------------------------------------

parsed_df = pd.DataFrame(parsed_rows)

failed_df = pd.DataFrame(
    failed_rows,
    columns=[
        "company_id",
        "metric_type",
        "original_text",
    ],
)

parsed_df.to_csv(PARSED_FILE, index=False)
failed_df.to_csv(FAILURE_FILE, index=False)

# -------------------------------------------------------
# Summary
# -------------------------------------------------------

print("=" * 60)
print("Analysis Parser Completed")
print("=" * 60)

print(f"Rows Parsed      : {len(parsed_df)}")
print(f"Parse Failures   : {len(failed_df)}")

print("\nSaved:")
print(PARSED_FILE)
print(FAILURE_FILE)