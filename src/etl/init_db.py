import sqlite3

DB_PATH = "db/nifty100.db"
SCHEMA_PATH = "db/schema.sql"

def main():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("PRAGMA foreign_keys = ON;")

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()

    print("Database ready")

if __name__ == "__main__":
    main()