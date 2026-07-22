import pandas as pd


def calculate_cagr(start_value, end_value, years):
    """
    Calculate Compound Annual Growth Rate (CAGR).

    CAGR = ((End / Start) ** (1 / Years) - 1) * 100
    """

    if (
        start_value is None
        or end_value is None
        or years <= 0
        or pd.isna(start_value)
        or pd.isna(end_value)
        or start_value <= 0
        or end_value <= 0
    ):
        return None

    try:
        return round(
            ((end_value / start_value) ** (1 / years) - 1) * 100,
            2,
        )
    except (ZeroDivisionError, ValueError, OverflowError):
        return None


def company_cagr(df, company_id, metric, years):
    """
    Compute CAGR for a company's financial metric.

    Parameters
    ----------
    df : pandas.DataFrame
        Profit & Loss dataframe.

    company_id : str
        Company identifier.

    metric : str
        Financial metric column name (e.g. 'sales', 'net_profit').

    years : int
        CAGR period (3, 5, 10 ...).

    Returns
    -------
    float | None
        CAGR percentage if computable, otherwise None.
    """

    if years <= 0:
        return None

    company = (
        df[
            (df["company_id"] == company_id)
            & (df["year"] != "TTM")
        ]
        .copy()
    )

    if company.empty:
        return None

    company["sort_year"] = (
        company["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    company = company.dropna(subset=["sort_year"])

    if company.empty:
        return None

    company["sort_year"] = company["sort_year"].astype(int)

    company = (
        company
        .sort_values("sort_year")
        .reset_index(drop=True)
    )

    if len(company) <= years:
        return None

    if metric not in company.columns:
        return None

    start_value = company.iloc[-(years + 1)][metric]
    end_value = company.iloc[-1][metric]

    return calculate_cagr(start_value, end_value, years)