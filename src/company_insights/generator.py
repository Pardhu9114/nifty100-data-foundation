from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parents[2]

OUTPUT = BASE / "output"

FILES = {
    "cashflow": OUTPUT / "cashflow_insights.csv",
    "balancesheet": OUTPUT / "balancesheet_insights.csv",
    "profitloss": OUTPUT / "profitloss_insights.csv",
    "financial_ratios": OUTPUT / "financial_ratios_insights.csv",
}

FINAL = OUTPUT / "company_insights.csv"


def load_file(source, path):

    df = pd.read_csv(path)

    df["source"] = source

    return df


def generate():

    dfs = []

    for source, path in FILES.items():

        dfs.append(load_file(source, path))

    report = pd.concat(
        dfs,
        ignore_index=True,
    )

    report = report[
        [
            "company_id",
            "source",
            "type",
            "rule_id",
            "text",
            "confidence_pct",
        ]
    ]

    report.to_csv(
        FINAL,
        index=False,
    )

    print("=" * 60)
    print("Company Insights Generated")
    print("=" * 60)

    print(f"Rows : {len(report)}")
    print(f"Companies : {report['company_id'].nunique()}")

    print()
    print("Saved :")
    print(FINAL)

    return report


if __name__ == "__main__":
    generate()