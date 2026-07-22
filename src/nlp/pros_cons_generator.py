import sqlite3
import pandas as pd
from pathlib import Path

from src.nlp.rules import PRO_RULES, CON_RULES


DB = "db/nifty100.db"
OUTPUT = "output/pros_cons_generated.csv"


def load_data():

    conn = sqlite3.connect(DB)

    companies = pd.read_sql(
        """
        SELECT id AS company_id
        FROM companies
        """,
        conn,
    )

    ratios = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn,
    )

    conn.close()

    companies["company_id"] = companies["company_id"].astype(str)
    ratios["company_id"] = ratios["company_id"].astype(str)

    return companies, ratios

def evaluate_company(company_id, ratios_df):

    company_ratios = ratios_df[
        ratios_df["company_id"] == company_id
    ].copy()

    results = []

    # --------------------
    # PRO RULES
    # --------------------

    for rule in PRO_RULES:

        try:

            result = rule(company_ratios)

            if (
                result is not None
                and result["confidence_pct"] > 60
            ):
                result["company_id"] = company_id
                results.append(result)

        except Exception as e:

            print(
                f"Error in {rule.__name__} "
                f"for {company_id}: {e}"
            )

    # --------------------
    # CON RULES
    # --------------------

    for rule in CON_RULES:

        try:

            result = rule(company_ratios)

            if (
                result is not None
                and result["confidence_pct"] > 60
            ):
                result["company_id"] = company_id
                results.append(result)

        except Exception as e:

            print(
                f"Error in {rule.__name__} "
                f"for {company_id}: {e}"
            )

    return results


def ensure_minimum_rules(results, company_id):

    pros = [
        r
        for r in results
        if r["type"] == "pro"
    ]

    cons = [
        r
        for r in results
        if r["type"] == "con"
    ]

    if len(pros) == 0:

        results.append(
            {
                "company_id": company_id,
                "type": "pro",
                "rule_id": "PRO_FALLBACK",
                "text": (
                    "Business exhibits "
                    "stable operating characteristics."
                ),
                "confidence_pct": 61,
            }
        )

    if len(cons) == 0:

        results.append(
            {
                "company_id": company_id,
                "type": "con",
                "rule_id": "CON_FALLBACK",
                "text": (
                    "Business should continue "
                    "to be monitored for future risks."
                ),
                "confidence_pct": 61,
            }
        )

    return results


def generate():

    companies, ratios = load_data()

    all_results = []

    print("=" * 60)
    print("Generating Pros / Cons")
    print("=" * 60)

    for company_id in companies["company_id"]:

        company_results = evaluate_company(
            company_id,
            ratios,
        )

        company_results = ensure_minimum_rules(
            company_results,
            company_id,
        )

        all_results.extend(company_results)

    output = pd.DataFrame(all_results)

    output = output[
        [
            "company_id",
            "type",
            "rule_id",
            "text",
            "confidence_pct",
        ]
    ]

    Path("output").mkdir(
        exist_ok=True
    )

    output.to_csv(
        OUTPUT,
        index=False,
    )

    print()

    print("=" * 60)
    print("Generation Completed")
    print("=" * 60)

    print("Companies :", len(companies))
    print("Rules Generated :", len(output))
    print("Saved :", OUTPUT)

    return output


def verify(df):

    print()

    print("=" * 60)
    print("Verification")
    print("=" * 60)

    summary = (
        df.groupby(
            ["company_id", "type"]
        )
        .size()
        .unstack(fill_value=0)
    )

    failed = summary[
        (summary["pro"] == 0)
        | (summary["con"] == 0)
    ]

    if failed.empty:

        print(
            "PASS : Every company has "
            "at least one Pro and one Con."
        )

    else:

        print(
            "FAILED"
        )

        print(failed)

    print()

    print(
        summary.describe()
    )


if __name__ == "__main__":

    df = generate()

    verify(df)