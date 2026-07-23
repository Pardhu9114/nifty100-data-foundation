"""
Sprint 6 - Day 36

KMeans Company Clustering
"""

import sqlite3

import pandas as pd


DB_PATH = "db/nifty100.db"


def load_features():
    """Load clustering features from SQLite."""

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        fr.company_id,
        s.broad_sector,
        fr.year,
        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.operating_profit_margin_pct,

        MAX(CASE
            WHEN am.metric_type='compounded_sales_growth'
             AND am.period_years=5
            THEN am.value_pct
        END) AS revenue_cagr_5yr,

        MAX(CASE
            WHEN am.metric_type='compounded_profit_growth'
             AND am.period_years=5
            THEN am.value_pct
        END) AS profit_cagr_5yr

    FROM financial_ratios fr

    LEFT JOIN sectors s
        ON fr.company_id=s.company_id

    LEFT JOIN analysis_metrics am
        ON fr.company_id=am.company_id

    GROUP BY
        fr.company_id,
        s.broad_sector,
        fr.year,
        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.operating_profit_margin_pct
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def main():
    df = load_features()

    print(df.head())
    print()
    print(df.columns)
    print()
    print(df.shape)


if __name__ == "__main__":
    main()