import sqlite3
import pandas as pd
import yaml

DB = "db/nifty100.db"
CONFIG = "config/screener_config.yaml"


# ---------------------------------------------------
# Load Screener Configuration
# ---------------------------------------------------
def load_config():
    with open(CONFIG, "r") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------
# Load Data (Latest Year Only)
# ---------------------------------------------------
def load_data():

    conn = sqlite3.connect(DB)

    query = """
    SELECT
        fr.company_id,
        fr.year,

        c.company_name,

        s.broad_sector,

        fr.return_on_equity_pct,
        fr.net_profit_margin_pct,
        fr.operating_profit_margin_pct,
        fr.debt_to_equity,
        fr.interest_coverage,
        fr.asset_turnover,
        fr.free_cash_flow_cr,
        fr.capex_cr,
        fr.earnings_per_share,
        fr.book_value_per_share,
        fr.dividend_payout_ratio_pct,
        fr.total_debt_cr,
        fr.cash_from_operations_cr,

        pg.peer_group_name,
        pg.is_benchmark

    FROM financial_ratios fr

    LEFT JOIN companies c
        ON fr.company_id = c.id

    LEFT JOIN sectors s
        ON fr.company_id = s.company_id

    LEFT JOIN peer_groups pg
        ON fr.company_id = pg.company_id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    # Keep only latest year for each company
    df = (
        df.sort_values("year")
          .groupby("company_id", as_index=False)
          .last()
    )

    return df


# ---------------------------------------------------
# Composite Score (temporary version)
# Day 17 will replace this
# ---------------------------------------------------
def compute_composite_score(df):

    score = pd.Series(0.0, index=df.index)

    if "return_on_equity_pct" in df.columns:
        score += (
            df["return_on_equity_pct"]
            .fillna(0)
            .clip(0, 30)
            * (35 / 30)
        )

    if "net_profit_margin_pct" in df.columns:
        score += (
            df["net_profit_margin_pct"]
            .fillna(0)
            .clip(0, 25)
            * (20 / 25)
        )

    if "free_cash_flow_cr" in df.columns:

        score += (
            (df["free_cash_flow_cr"] > 0)
            .astype(int)
            * 15
        )

    if "interest_coverage" in df.columns:

        score += (
            df["interest_coverage"]
            .fillna(0)
            .clip(0, 10)
            * 1.5
        )

    if "asset_turnover" in df.columns:

        score += (
            df["asset_turnover"]
            .fillna(0)
            .clip(0, 2)
            * 7.5
        )

    score = score.clip(0, 100)

    return score.round(2)

# ---------------------------------------------------
# Generic Filter Engine
# ---------------------------------------------------
def apply_filters(df, filters):

    result = df.copy()

    for rule, value in filters.items():

        column = (
            rule.replace("_min", "")
                .replace("_max", "")
        )

        mapping = {

            "roe": "return_on_equity_pct",

            "opm": "operating_profit_margin_pct",

            "fcf": "free_cash_flow_cr",

            "sales": "cash_from_operations_cr",

            "debt_to_equity": "debt_to_equity",

            "icr": "interest_coverage"
        }

        column = mapping.get(column, column)

        if column not in result.columns:
            continue

        # -----------------------------
        # Minimum filters
        # -----------------------------
        if rule.endswith("_min"):

            if column == "interest_coverage":

                # Debt Free always passes
                mask = (
                    (result[column] >= value)
                    |
                    (result[column].isna())
                )

                result = result[mask]

            else:

                result = result[
                    result[column] >= value
                ]

        # -----------------------------
        # Maximum filters
        # -----------------------------
        elif rule.endswith("_max"):

            if column == "debt_to_equity":

                financials = (
                    result["broad_sector"]
                    == "Financials"
                )

                normal = (
                    result[column] <= value
                )

                result = result[
                    financials | normal
                ]

            else:

                result = result[
                    result[column] <= value
                ]

    result["composite_quality_score"] = (
        compute_composite_score(result)
    )

    result = result.sort_values(
        "composite_quality_score",
        ascending=False
    )

    return result


# ---------------------------------------------------
# Run Preset
# ---------------------------------------------------
def run_preset(name):

    config = load_config()

    if name not in config:
        raise ValueError(
            f"Unknown preset: {name}"
        )

    data = load_data()

    screened = apply_filters(
        data,
        config[name]
    )

    return screened


def main():

    print("=" * 60)
    print("NIFTY100 SCREENER")
    print("=" * 60)

    df = load_data()

    print()

    print("Companies Loaded :", len(df))

    print()

    print(df.head())

    print()

    print("Peer Groups :", df["peer_group_name"].nunique())