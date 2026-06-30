"""
Sprint 2 - Day 11
Cash Flow KPI Engine
"""


def free_cash_flow(
    operating_activity,
    investing_activity
):
    """
    Free Cash Flow

    FCF = CFO + CFI
    """

    return operating_activity + investing_activity


def cfo_quality_score(
    operating_cashflow,
    net_profit
):
    """
    CFO / PAT Classification
    """

    if net_profit == 0:
        return None

    score = operating_cashflow / net_profit

    if score > 1:
        return "High Quality"

    if score >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def capex_intensity(
    investing_activity,
    sales
):
    """
    CapEx Intensity
    """

    if sales == 0:
        return None

    pct = abs(investing_activity) / sales * 100

    if pct < 3:
        return "Asset Light"

    if pct <= 8:
        return "Moderate"

    return "Capital Intensive"


def fcf_conversion_rate(
    free_cash_flow_value,
    operating_profit
):
    """
    FCF Conversion %

    FCF / Operating Profit
    """

    if operating_profit == 0:
        return None

    return (
        free_cash_flow_value
        / operating_profit
    ) * 100
def capital_allocation_pattern(
    operating_activity,
    investing_activity,
    financing_activity,
    cfo_quality=None
):
    """
    Classify cash flow pattern based on
    CFO, CFI and CFF signs.
    """

    cfo = "+" if operating_activity >= 0 else "-"
    cfi = "+" if investing_activity >= 0 else "-"
    cff = "+" if financing_activity >= 0 else "-"

    # Special case
    if (cfo, cfi, cff) == ("+", "-", "-"):
        if cfo_quality == "High Quality":
            return "Shareholder Returns"
        return "Reinvestor"

    patterns = {
        ("+", "-", "+"): "Mixed",
        ("+", "+", "+"): "Cash Accumulator",
        ("+", "+", "-"): "Liquidating Assets",
        ("-", "+", "+"): "Distress Signal",
        ("-", "-", "+"): "Growth Funded by Debt",
        ("-", "-", "-"): "Pre-Revenue",
    }

    return patterns.get((cfo, cfi, cff), "Unknown")