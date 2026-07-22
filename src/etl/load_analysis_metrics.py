import sqlite3
import pandas as pd

DB = "db/nifty100.db"

CSV = "output/analysis_parsed.csv"


def load_analysis_metrics():

    df = pd.read_csv(CSV)

    conn = sqlite3.connect(DB)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM analysis_metrics")

    conn.commit()

    df.to_sql(
        "analysis_metrics",
        conn,
        if_exists="append",
        index=False,
    )

    conn.commit()

    print("=" * 60)
    print("Analysis Metrics Loaded")
    print("=" * 60)
    print("Rows inserted:", len(df))

    conn.close()


if __name__ == "__main__":
    load_analysis_metrics()