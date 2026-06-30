"""
Financial Ratio Engine
Sprint 2 - Day 08
"""


def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin (%)
    """

    if sales in (0, None):
        return None

    return (net_profit / sales) * 100


def operating_profit_margin(operating_profit, sales):
    """
    Operating Profit Margin (%)
    """

    if sales in (0, None):
        return None

    return (operating_profit / sales) * 100


def return_on_equity(net_profit, equity_capital, reserves):
    """
    Return on Equity (%)
    """

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return (net_profit / equity) * 100


def return_on_capital_employed(
    operating_profit,
    equity_capital,
    reserves,
    borrowings
):
    """
    Return on Capital Employed (%)
    """

    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    return (operating_profit / capital) * 100


def return_on_assets(net_profit, total_assets):
    """
    Return on Assets (%)
    """

    if total_assets <= 0:
        return None

    return (net_profit / total_assets) * 100


def check_opm_difference(
    operating_profit,
    sales,
    stored_opm,
    tolerance=1.0
):
    """
    Returns True if computed OPM differs
    from stored OPM by more than tolerance.
    """

    calculated = operating_profit_margin(
        operating_profit,
        sales
    )

    if calculated is None or stored_opm is None:
        return False

    return abs(calculated - stored_opm) > tolerance
# ===============================
# Day 09 - Leverage & Efficiency
# ===============================

def debt_to_equity(borrowings, equity_capital, reserves):
    """
    Debt-to-Equity Ratio

    Returns:
        0 if borrowings == 0
        None if equity <= 0
    """

    equity = equity_capital + reserves

    if borrowings == 0:
        return 0

    if equity <= 0:
        return None

    return borrowings / equity


def high_leverage_flag(de_ratio, is_financial=False):
    """
    High leverage warning.
    Financial companies are excluded.
    """

    if is_financial:
        return False

    if de_ratio is None:
        return False

    return de_ratio > 5


def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest
):
    """
    Interest Coverage Ratio

    Returns None if interest is zero.
    """

    if interest == 0:
        return None

    return (operating_profit + other_income) / interest


def icr_label(icr):
    """
    Returns 'Debt Free' when ICR is None.
    """

    if icr is None:
        return "Debt Free"

    return None


def icr_warning(icr):
    """
    Warning if ICR < 1.5
    """

    if icr is None:
        return False

    return icr < 1.5


def net_debt(borrowings, investments):
    """
    Net Debt
    """

    return borrowings - investments


def asset_turnover(sales, total_assets):
    """
    Asset Turnover Ratio
    """

    if total_assets <= 0:
        return None

    return sales / total_assets