import pandas as pd
import sqlite3

DB_FILE = "db/nifty100.db"
EXCEL_FILE = "data/raw/profitandloss.xlsx"


def main():
    df = pd.read_excel(
        EXCEL_FILE,
        header=1
    )

    print("Rows:", len(df))

    conn = sqlite3.connect(DB_FILE)

    df.to_sql(
        "profitandloss",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()
    conn.close()

    print(f"{len(df)} rows loaded")


if __name__ == "__main__":
    main()