import pandas as pd


def calculate_cagr(start_value, end_value, years):
    """
    Calculate CAGR (%)

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
    except Exception:
        return None


def company_cagr(df, company_id, metric, years):
    """
    Compute CAGR for one company.

    Parameters
    ----------
    df : DataFrame
        Profit & Loss dataframe

    company_id : str
        Company identifier

    metric : str
        "sales" or "net_profit"

    years : int
        CAGR period (3, 5, 10 ...)
    """

    # CAGR is not defined for 0-year periods
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

    # Extract numeric year (e.g. "Mar 2024" -> 2024)
    company["sort_year"] = (
        company["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    company = company.dropna(subset=["sort_year"])

    company["sort_year"] = company["sort_year"].astype(int)

    company = company.sort_values("sort_year").reset_index(drop=True)

    # Need at least (years + 1) annual records
    if len(company) <= years:
        return None

    start = company.iloc[-(years + 1)][metric]
    end = company.iloc[-1][metric]

    return calculate_cagr(start, end, years)

if status == "PASS":
    remarks = "Within ±5% tolerance"
elif status == "FAIL":
    remarks = "Computed CAGR differs from parsed value by more than 5%"
else:
    remarks = "Metric cannot be validated from available financial data"
"remarks": remarks,