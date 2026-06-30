import sqlite3
import pandas as pd

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover,
    net_debt,
)

from src.analytics.cashflow_kpis import (
    free_cash_flow,
    capex_intensity,
    fcf_conversion_rate,
)

DB = "db/nifty100.db"


def load_ratio_dataframe():
    conn = sqlite3.connect(DB)

    pnl = (
        pd.read_sql(
            "SELECT * FROM profitandloss",
            conn
        )
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="first"
        )
    )

    bs = (
        pd.read_sql(
            "SELECT * FROM balancesheet",
            conn
        )
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="first"
        )
    )

    cf = (
        pd.read_sql(
            "SELECT * FROM cashflow",
            conn
        )
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="first"
        )
    )

    conn.close()

    df = (
        pnl.merge(
            bs,
            on=["company_id", "year"],
            how="left",
            suffixes=("_pnl", "_bs")
        )
        .merge(
            cf,
            on=["company_id", "year"],
            how="left"
        )
    )

    return df


def compute_ratios(df):

    rows = []

    for _, r in df.iterrows():

        fcf = free_cash_flow(
            r["operating_activity"],
            r["investing_activity"]
        )

        rows.append({

            "company_id": r["company_id"],
            "year": r["year"],

            "net_profit_margin_pct":
                net_profit_margin(
                    r["net_profit"],
                    r["sales"]
                ),

            "operating_profit_margin_pct":
                operating_profit_margin(
                    r["operating_profit"],
                    r["sales"]
                ),

            "return_on_equity_pct":
                return_on_equity(
                    r["net_profit"],
                    r["equity_capital"],
                    r["reserves"]
                ),

            "return_on_capital_employed_pct":
                return_on_capital_employed(
                    r["operating_profit"],
                    r["equity_capital"],
                    r["reserves"],
                    r["borrowings"]
                ),

            "return_on_assets_pct":
                return_on_assets(
                    r["net_profit"],
                    r["total_assets"]
                ),

            "debt_to_equity":
                debt_to_equity(
                    r["borrowings"],
                    r["equity_capital"],
                    r["reserves"]
                ),

            "interest_coverage":
                interest_coverage_ratio(
                    r["operating_profit"],
                    r["other_income"],
                    r["interest"]
                ),

            "asset_turnover":
                asset_turnover(
                    r["sales"],
                    r["total_assets"]
                ),

            "free_cash_flow_cr":
                fcf,

            "capex_intensity":
                capex_intensity(
                    r["investing_activity"],
                    r["sales"]
                ),

            "fcf_conversion_rate":
                fcf_conversion_rate(
                    fcf,
                    r["operating_profit"]
                ),

            "net_debt":
                net_debt(
                    r["borrowings"],
                    r["investments"]
                )

        })

    return pd.DataFrame(rows)


if __name__ == "__main__":

    merged = load_ratio_dataframe()

    ratios = compute_ratios(merged)

    print(ratios.head())

    print()

    print("Rows:", len(ratios))