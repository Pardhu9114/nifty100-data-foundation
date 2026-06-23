import sqlite3
import pandas as pd

from validator import (
    validate_pk_uniqueness,
    validate_company_year_uniqueness,
    validate_fk_integrity,
    validate_balance_sheet,
    validate_opm_crosscheck,
    validate_positive_sales
)

DB_FILE = "db/nifty100.db"

conn = sqlite3.connect(DB_FILE)

companies = pd.read_sql("SELECT * FROM companies", conn)
profitandloss = pd.read_sql("SELECT * FROM profitandloss", conn)
balancesheet = pd.read_sql("SELECT * FROM balancesheet", conn)
cashflow = pd.read_sql("SELECT * FROM cashflow", conn)
analysis = pd.read_sql("SELECT * FROM analysis", conn)
documents = pd.read_sql("SELECT * FROM documents", conn)
prosandcons = pd.read_sql("SELECT * FROM prosandcons", conn)
financial_ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)

failures = []

# DQ-01
result = validate_pk_uniqueness(companies)

if not result["passed"]:
    for _, row in result["violations"].iterrows():
        failures.append({
            "rule": "DQ-01",
            "severity": "CRITICAL",
            "table": "companies",
            "record_id": row["id"]
        })

# DQ-02
result = validate_company_year_uniqueness(profitandloss)

if not result["passed"]:
    for _, row in result["violations"].iterrows():
        failures.append({
            "rule": "DQ-02",
            "severity": "CRITICAL",
            "table": "profitandloss",
            "record_id": row["id"]
        })

# DQ-03
child_tables = {
    "profitandloss": profitandloss,
    "balancesheet": balancesheet,
    "cashflow": cashflow,
    "analysis": analysis,
    "documents": documents,
    "prosandcons": prosandcons,
    "financial_ratios": financial_ratios
}

for table_name, df in child_tables.items():

    result = validate_fk_integrity(
        df,
        companies
    )

    if not result["passed"]:

        for _, row in result["violations"].iterrows():
            failures.append({
                "rule": "DQ-03",
                "severity": "CRITICAL",
                "table": table_name,
                "record_id": row["id"]
            })

# DQ-04
result = validate_balance_sheet(balancesheet)

if not result["passed"]:

    for _, row in result["violations"].iterrows():
        failures.append({
            "rule": "DQ-04",
            "severity": "WARNING",
            "table": "balancesheet",
            "record_id": row["id"]
        })

# DQ-05
result = validate_opm_crosscheck(profitandloss)

if not result["passed"]:

    for _, row in result["violations"].iterrows():
        failures.append({
            "rule": "DQ-05",
            "severity": "WARNING",
            "table": "profitandloss",
            "record_id": row["id"]
        })

# DQ-06
result = validate_positive_sales(profitandloss)

if not result["passed"]:

    for _, row in result["violations"].iterrows():
        failures.append({
            "rule": "DQ-06",
            "severity": "CRITICAL",
            "table": "profitandloss",
            "record_id": row["id"]
        })

validation_df = pd.DataFrame(failures)

validation_df.to_csv(
    "output/validation_failures.csv",
    index=False
)

print("\nValidation complete")

print(
    "Total violations:",
    len(validation_df)
)

conn.close()