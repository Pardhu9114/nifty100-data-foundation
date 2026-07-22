from pathlib import Path
import sqlite3

import pandas as pd

from src.cashflow.rules import (
    PRO_RULES,
    CON_RULES,
)

BASE = Path(__file__).resolve().parents[2]

DB = BASE / "db" / "nifty100.db"

OUTPUT = (
    BASE
    / "output"
    / "cashflow_insights.csv"
)

def load_cashflow():

    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            operating_activity,
            investing_activity,
            financing_activity,
            net_cash_flow
        FROM cashflow
        """,
        conn,
    )

    conn.close()

    return df

if __name__ == "__main__":

    df = load_cashflow()

    print(df.head())

    print()

    print(df.columns.tolist())

    print()

    print(f"Rows : {len(df)}")

def generate():

    cashflow = load_cashflow()

    rows = []

    for company_id, df in cashflow.groupby("company_id"):

        matched = False

        # PRO Rules
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

        # CON Rules
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
                    "rule_id": "CF_FALLBACK",
                    "text": (
                        "Cash flow information is available, "
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
    print("Cashflow Intelligence Generated")
    print("=" * 60)
    print(f"Companies : {cashflow['company_id'].nunique()}")
    print(f"Insights  : {len(report)}")
    print()
    print("Saved :")
    print(OUTPUT)

    return report

if __name__ == "__main__":
    generate()