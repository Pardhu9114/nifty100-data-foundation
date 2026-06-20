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

    if "sales_cr" not in df.columns:
        return {"passed": True, "violations": pd.DataFrame()}

    invalid = df[df["sales_cr"] <= 0]

    return {
        "passed": invalid.empty,
        "violations": invalid
    }