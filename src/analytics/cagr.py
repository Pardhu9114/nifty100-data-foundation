import pandas as pd


def calculate_cagr(start_value, end_value, years):
    """
    Calculate CAGR.

    Returns
    -------
    (value, flag)

    value : float | None
    flag  : str | None
    """

    if years <= 0:
        return None, "INSUFFICIENT"

    if start_value is None or end_value is None:
        return None, "INSUFFICIENT"

    if pd.isna(start_value) or pd.isna(end_value):
        return None, "INSUFFICIENT"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    try:
        value = (
            ((end_value / start_value) ** (1 / years) - 1)
            * 100
        )

        return round(value, 2), None

    except (ZeroDivisionError, ValueError, OverflowError):
        return None, "INSUFFICIENT"


def revenue_cagr(start_value, end_value, years):
    return calculate_cagr(start_value, end_value, years)


def pat_cagr(start_value, end_value, years):
    return calculate_cagr(start_value, end_value, years)


def eps_cagr(start_value, end_value, years):
    return calculate_cagr(start_value, end_value, years)


def company_cagr(df, company_id, metric, years):
    """
    Compute CAGR for a company's financial metric.
    """

    if years <= 0:
        return None, "INSUFFICIENT"

    company = (
        df[
            (df["company_id"] == company_id)
            & (df["year"] != "TTM")
        ]
        .copy()
    )

    if company.empty:
        return None, "INSUFFICIENT"

    company["sort_year"] = (
        company["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    company = company.dropna(subset=["sort_year"])

    if company.empty:
        return None, "INSUFFICIENT"

    company["sort_year"] = company["sort_year"].astype(int)

    company = company.sort_values("sort_year").reset_index(drop=True)

    if len(company) <= years:
        return None, "INSUFFICIENT"

    if metric not in company.columns:
        return None, "INSUFFICIENT"

    start_value = company.iloc[-(years + 1)][metric]
    end_value = company.iloc[-1][metric]

    return calculate_cagr(start_value, end_value, years)
    # -------------------------------------------------------
# Backward compatibility aliases
# -------------------------------------------------------

def sales_cagr(start_value, end_value, years):
    """Alias for revenue CAGR."""
    return revenue_cagr(start_value, end_value, years)


def profit_cagr(start_value, end_value, years):
    """Alias for PAT CAGR."""
    return pat_cagr(start_value, end_value, years)


def stock_price_cagr(start_value, end_value, years):
    """
    Alias for CAGR calculation on stock prices.
    Uses the generic CAGR formula.
    """
    return calculate_cagr(start_value, end_value, years)