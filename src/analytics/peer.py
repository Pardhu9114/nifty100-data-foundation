import sqlite3
import pandas as pd

DB = "db/nifty100.db"


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
        fr.debt_to_equity,
        fr.interest_coverage,
        fr.asset_turnover,
        fr.free_cash_flow_cr,

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

    # Keep latest record for every company
    df = (
        df.sort_values("year")
          .groupby("company_id", as_index=False)
          .last()
    )

    # Companies without peer groups
    df["peer_group_name"] = (
        df["peer_group_name"]
        .fillna("No peer group assigned")
    )

    df["is_benchmark"] = (
        df["is_benchmark"]
        .fillna(0)
        .astype(int)
    )

    return df

def compute_percentiles(df):

    metrics = [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr"
    ]

    rows = []

    for peer_group in df["peer_group_name"].unique():

        if peer_group == "No peer group assigned":
            continue

        group = df[df["peer_group_name"] == peer_group].copy()

        if len(group) <= 1:
            continue

        for metric in metrics:

            if metric not in group.columns:
                continue

            valid = group[metric].notna()
            
            ranking = group.loc[valid, metric].rank(pct=True)

            # Lower D/E is better
            if metric == "debt_to_equity":
                ranking = 1 - ranking

            for i in ranking.index:

                rows.append({
                    "company_id": group.loc[i, "company_id"],
                    "peer_group_name": peer_group,
                    "metric": metric,
                    "value": group.loc[i, metric],
                    "percentile_rank": round(float(ranking.loc[i]), 4),
                    "year": group.loc[i, "year"]
                })

    return pd.DataFrame(rows)

def save_percentiles(df):

    conn = sqlite3.connect(DB)

    conn.execute("DELETE FROM peer_percentiles")

    df.to_sql(
        "peer_percentiles",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()


def main():

    print("=" * 60)
    print("PEER ENGINE")
    print("=" * 60)

    df = load_data()

    print("Companies Loaded :", len(df))

    percentile_df = compute_percentiles(df)

    save_percentiles(percentile_df)

    print()

    print("Percentile rows created :", len(percentile_df))

    print()

    print(percentile_df.head())


if __name__ == "__main__":
    main()