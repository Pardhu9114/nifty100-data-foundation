from pathlib import Path
import sqlite3

import pandas as pd

from src.financial_ratios.rules import (
    PRO_RULES,
    CON_RULES,
)

BASE = Path(__file__).resolve().parents[2]

DB = BASE / "db" / "nifty100.db"

OUTPUT = BASE / "output" / "financial_ratios_insights.csv"


def load_financial_ratios():

    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            net_profit_margin_pct,
            operating_profit_margin_pct,
            return_on_equity_pct,
            debt_to_equity,
            interest_coverage,
            asset_turnover,
            free_cash_flow_cr,
            capex_cr,
            earnings_per_share,
            book_value_per_share,
            dividend_payout_ratio_pct,
            total_debt_cr,
            cash_from_operations_cr
        FROM financial_ratios
        """,
        conn,
    )

    conn.close()

    return df


def generate():

    ratios = load_financial_ratios()

    rows = []

    for company_id, df in ratios.groupby("company_id"):

        matched = False

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

        if not matched:
            rows.append(
                {
                    "company_id": company_id,
                    "type": "info",
                    "rule_id": "FR_FALLBACK",
                    "text": (
                        "Financial ratio information is available, "
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
    print("Financial Ratios Intelligence Generated")
    print("=" * 60)
    print(f"Companies : {ratios['company_id'].nunique()}")
    print(f"Insights  : {len(report)}")
    print()
    print("Saved :")
    print(OUTPUT)

    return report


if __name__ == "__main__":
    generate()