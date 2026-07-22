import sqlite3

DB = "db/nifty100.db"


def create_table():
    conn = sqlite3.connect(DB)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS analysis_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id TEXT NOT NULL,
            metric_type TEXT NOT NULL,
            period_years INTEGER NOT NULL,
            value_pct REAL NOT NULL
        );
    """)

    conn.commit()
    conn.close()

    print("analysis_metrics table is ready.")


if __name__ == "__main__":
    create_table()