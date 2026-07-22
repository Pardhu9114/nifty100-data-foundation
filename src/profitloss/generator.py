from pathlib import Path
import sqlite3

import pandas as pd

from src.profitloss.rules import (
    PRO_RULES,
    CON_RULES,
)

BASE = Path(__file__).resolve().parents[2]

DB = BASE / "db" / "nifty100.db"

OUTPUT = BASE / "output" / "profitloss_insights.csv"


def load_profitloss():

    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            sales,
            expenses,
            operating_profit,
            opm_percentage,
            other_income,
            interest,
            depreciation,
            profit_before_tax,
            tax_percentage,
            net_profit,
            eps,
            dividend_payout
        FROM profitandloss
        """,
        conn,
    )

    conn.close()

    return df


def generate():

    profitloss = load_profitloss()

    rows = []

    for company_id, df in profitloss.groupby("company_id"):

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
                    "rule_id": "PL_FALLBACK",
                    "text": (
                        "Profit & Loss information is available, "
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
    print("Profit & Loss Intelligence Generated")
    print("=" * 60)
    print(f"Companies : {profitloss['company_id'].nunique()}")
    print(f"Insights  : {len(report)}")
    print()
    print("Saved :")
    print(OUTPUT)

    return report


if __name__ == "__main__":
    generate()