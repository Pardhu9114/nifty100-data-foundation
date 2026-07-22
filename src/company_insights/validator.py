from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[2]

INPUT = BASE / "output" / "company_insights.csv"


def validate():

    report = pd.read_csv(INPUT)

    print("=" * 60)
    print("Company Insights Validation")
    print("=" * 60)

    print(f"Rows : {len(report)}")
    print()

    print("Source Distribution")
    print(report["source"].value_counts())
    print()

    print("Insight Types")
    print(report["type"].value_counts())
    print()

    duplicates = report.duplicated(
        subset=["company_id", "source", "rule_id"]
    ).sum()

    print(f"Duplicate Rules : {duplicates}")

    invalid = report[
        ~report["confidence_pct"].between(0, 100)
    ]

    print(f"Invalid Confidence : {len(invalid)}")

    companies = report["company_id"].nunique()

    print(f"Companies Covered : {companies}")


if __name__ == "__main__":
    validate()