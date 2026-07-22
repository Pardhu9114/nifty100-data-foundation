from pathlib import Path
import sqlite3

import pandas as pd

from src.analytics.cagr import company_cagr


BASE = Path(__file__).resolve().parents[2]

DB = BASE / "db" / "nifty100.db"
PARSED = BASE / "output" / "analysis_parsed.csv"
OUTPUT = BASE / "output" / "cagr_validation_report.csv"


def load_profit_data():
    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            sales,
            net_profit
        FROM profitandloss
        """,
        conn,
    )

    conn.close()

    return df


def validate():

    parsed = pd.read_csv(PARSED)

    pnl = load_profit_data()

    rows = []

    for _, r in parsed.iterrows():

        company = r.company_id
        metric = r.metric_type
        years = int(r.period_years)

        computed = None
        difference = None
        status = "NOT_SUPPORTED"

        if metric == "compounded_sales_growth":

            computed = company_cagr(
                pnl,
                company,
                "sales",
                years,
            )

        elif metric == "compounded_profit_growth":

            computed = company_cagr(
                pnl,
                company,
                "net_profit",
                years,
            )

        if computed is not None:

            difference = round(
                abs(r.value_pct - computed),
                2,
            )

            if difference <= 5:
                status = "PASS"
            else:
                status = "FAIL"

        if status == "PASS":
            remarks = "Within ±5% tolerance"

        elif status == "FAIL":
            remarks = (
                "Computed CAGR differs from parsed value "
                "by more than 5%"
            )

        else:
            remarks = (
                "Metric cannot be validated from "
                "available financial data"
            )

        rows.append(
            {
                "company_id": company,
                "metric_type": metric,
                "period_years": years,
                "parsed_value_pct": r.value_pct,
                "computed_value_pct": computed,
                "difference_pct": difference,
                "status": status,
                "remarks": remarks,
            }
        )

    report = pd.DataFrame(rows)

    report.to_csv(
        OUTPUT,
        index=False,
    )

    print("=" * 60)
    print("CAGR Validation Complete")
    print("=" * 60)
    print(f"Rows : {len(report)}")
    print()

    print(report["status"].value_counts())
    print()

    print("Saved to")
    print(OUTPUT)


if __name__ == "__main__":
    print("Starting CAGR validator...")
    validate()
    print("CAGR validator finished.")