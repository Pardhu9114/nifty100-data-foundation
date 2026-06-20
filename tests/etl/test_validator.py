import pandas as pd

from src.etl.validator import (
    validate_pk_uniqueness,
    validate_company_year_uniqueness,
    validate_fk_integrity
)


def test_pk_uniqueness_pass():
    df = pd.DataFrame({
        "id": [1, 2, 3]
    })

    result = validate_pk_uniqueness(df)

    assert result["passed"] is True


def test_pk_uniqueness_fail():
    df = pd.DataFrame({
        "id": [1, 1, 2]
    })

    result = validate_pk_uniqueness(df)

    assert result["passed"] is False


def test_company_year_unique():
    df = pd.DataFrame({
        "company_id": [1, 1],
        "year": [2023, 2024]
    })

    result = validate_company_year_uniqueness(df)

    assert result["passed"] is True


def test_fk_integrity():
    companies = pd.DataFrame({
        "id": [1, 2]
    })

    pnl = pd.DataFrame({
        "company_id": [1, 2]
    })

    result = validate_fk_integrity(
        pnl,
        companies
    )

    assert result["passed"] is True