from pathlib import Path
import sqlite3

import pandas as pd

from src.balancesheet.rules import (
    PRO_RULES,
    CON_RULES,
)

BASE = Path(__file__).resolve().parents[2]

DB = BASE / "db" / "nifty100.db"

OUTPUT = BASE / "output" / "balancesheet_insights.csv"


def load_balancesheet():

    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            equity_capital,
            reserves,
            borrowings,
            other_liabilities,
            total_liabilities,
            fixed_assets,
            cwip,
            investments,
            other_asset,
            total_assets
        FROM balancesheet
        """,
        conn,
    )

    conn.close()

    return df


def generate():

    balancesheet = load_balancesheet()

    rows = []

    for company_id, df in balancesheet.groupby("company_id"):

        matched = False

        # PRO rules
        for rule in PRO_RULES:

            result = rule(df)

            if result is not None:

                matched = True

                rows.append(
                    {
                        "company_id": company_id,
                        **result,
                    }
                )

        # CON rules
        for rule in CON_RULES:

            result = rule(df)

            if result is not None:

                matched = True

                rows.append(
                    {
                        "company_id": company_id,
                        **result,
                    }
                )

        # Fallback
        if not matched:

            rows.append(
                {
                    "company_id": company_id,
                    "type": "info",
                    "rule_id": "BS_FALLBACK",
                    "text": (
                        "Balance sheet information is available, "
                        "but no predefined rule was triggered."
                    ),
                    "confidence_pct": 50,
                }
            )

    report = pd.DataFrame(rows)

    report.to_csv(
        OUTPUT,
        index=False,
    )

    print("=" * 60)
    print("Balance Sheet Intelligence Generated")
    print("=" * 60)
    print(f"Companies : {balancesheet['company_id'].nunique()}")
    print(f"Insights  : {len(report)}")
    print()
    print("Saved :")
    print(OUTPUT)

    return report


if __name__ == "__main__":
    generate()