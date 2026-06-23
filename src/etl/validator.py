import pandas as pd


def validate_pk_uniqueness(df, pk_column="id"):
    """
    DQ-01: Primary Key uniqueness
    """
    duplicates = df[df.duplicated(subset=[pk_column], keep=False)]

    return {
        "passed": duplicates.empty,
        "violations": duplicates
    }


def validate_company_year_uniqueness(df):
    """
    DQ-02: (company_id, year) uniqueness
    """
    duplicates = df[
        df.duplicated(
            subset=["company_id", "year"],
            keep=False
        )
    ]

    return {
        "passed": duplicates.empty,
        "violations": duplicates
    }


def validate_fk_integrity(
    child_df,
    parent_df,
    fk_col="company_id",
    pk_col="id"
):
    """
    DQ-03: Foreign Key integrity
    """

    invalid = child_df[
        ~child_df[fk_col].isin(parent_df[pk_col])
    ]

    return {
        "passed": invalid.empty,
        "violations": invalid
    }


def validate_positive_sales(df):
    """
    DQ-06: Sales must be positive
    """

    if "sales" not in df.columns:
        return {
            "passed": True,
            "violations": pd.DataFrame()
        }

    invalid = df[df["sales"] <= 0]

    return {
        "passed": invalid.empty,
        "violations": invalid
    }
def validate_balance_sheet(df):
    """
    DQ-04:
    total_assets ~= total_liabilities
    tolerance = 1%
    """

    required = [
        "total_assets",
        "total_liabilities"
    ]

    if not all(col in df.columns for col in required):
        return {
            "passed": True,
            "violations": pd.DataFrame()
        }

    diff_pct = (
        abs(
            df["total_assets"] -
            df["total_liabilities"]
        )
        /
        df["total_assets"].replace(0, 1)
    )

    invalid = df[diff_pct > 0.01]

    return {
        "passed": invalid.empty,
        "violations": invalid
    }
def validate_opm_crosscheck(df):
    """
    DQ-05:
    operating_profit / sales ~= opm_percentage
    """

    required = [
        "sales",
        "operating_profit",
        "opm_percentage"
    ]

    if not all(col in df.columns for col in required):
        return {
            "passed": True,
            "violations": pd.DataFrame()
        }

    calc_opm = (
        df["operating_profit"]
        /
        df["sales"].replace(0, 1)
        * 100
    )

    diff = abs(
        calc_opm -
        df["opm_percentage"]
    )

    invalid = df[diff > 1]

    return {
        "passed": invalid.empty,
        "violations": invalid
    }