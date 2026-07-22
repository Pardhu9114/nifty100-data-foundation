import sqlite3

DB = "db/nifty100.db"


def create_indexes():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_analysis_company
        ON analysis_metrics(company_id);
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_analysis_metric
        ON analysis_metrics(metric_type);
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_analysis_period
        ON analysis_metrics(period_years);
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_analysis_lookup
        ON analysis_metrics(company_id, metric_type, period_years);
    """)

    conn.commit()
    conn.close()

    print("Analysis indexes created successfully.")


if __name__ == "__main__":
    create_indexes()