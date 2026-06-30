import sqlite3

from src.analytics.ratio_engine import (
    load_ratio_dataframe,
    compute_ratios,
)

DB = "db/nifty100.db"

conn = sqlite3.connect(DB)

print("Loading source data...")

merged = load_ratio_dataframe()

print("Computing ratios...")

ratios = compute_ratios(merged)

print("Rows:", len(ratios))

cursor = conn.cursor()

updated = 0

for _, r in ratios.iterrows():

    cursor.execute(
        """
        UPDATE financial_ratios
        SET
            net_profit_margin_pct=?,
            operating_profit_margin_pct=?,
            return_on_equity_pct=?,
            debt_to_equity=?,
            interest_coverage=?,
            asset_turnover=?,
            free_cash_flow_cr=?,
            capex_cr=?,
            total_debt_cr=?,
            cash_from_operations_cr=?
        WHERE
            company_id=?
            AND year=?
        """,
        (
            r["net_profit_margin_pct"],
            r["operating_profit_margin_pct"],
            r["return_on_equity_pct"],
            r["debt_to_equity"],
            r["interest_coverage"],
            r["asset_turnover"],
            r["free_cash_flow_cr"],
            r["capex_intensity"],
            r["net_debt"],
            r["free_cash_flow_cr"],
            r["company_id"],
            r["year"],
        ),
    )

    updated += cursor.rowcount

conn.commit()

print(f"Updated {updated} rows")

conn.close()