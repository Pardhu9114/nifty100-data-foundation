import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    check_opm_difference
)


def test_net_profit_margin():
    assert round(net_profit_margin(100, 1000), 2) == 10.00


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_operating_profit_margin():
    assert round(operating_profit_margin(200, 1000), 2) == 20.00


def test_operating_profit_margin_zero_sales():
    assert operating_profit_margin(100, 0) is None


def test_return_on_equity():
    assert round(return_on_equity(100, 200, 300), 2) == 20.00


def test_return_on_equity_negative():
    assert return_on_equity(100, -200, 100) is None


def test_return_on_capital_employed():
    assert round(
        return_on_capital_employed(200, 200, 300, 500),
        2
    ) == 20.00


def test_return_on_assets():
    assert round(return_on_assets(100, 500), 2) == 20.00


def test_return_on_assets_zero():
    assert return_on_assets(100, 0) is None


def test_opm_difference_false():
    assert check_opm_difference(200, 1000, 20) is False


def test_opm_difference_true():
    assert check_opm_difference(200, 1000, 25) is True

from src.analytics.ratios import (
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning,
    net_debt,
    asset_turnover
)


def test_debt_to_equity():
    assert round(debt_to_equity(500, 200, 300), 2) == 1.00


def test_debt_to_equity_debt_free():
    assert debt_to_equity(0, 100, 100) == 0


def test_interest_coverage_ratio():
    assert round(
        interest_coverage_ratio(100, 20, 40),
        2
    ) == 3.00


def test_interest_coverage_zero():
    assert interest_coverage_ratio(100, 20, 0) is None


def test_icr_label():
    assert icr_label(None) == "Debt Free"


def test_icr_warning():
    assert icr_warning(1.2) is True


def test_net_debt():
    assert net_debt(500, 200) == 300


def test_asset_turnover():
    assert round(asset_turnover(1000, 500), 2) == 2.00


def test_asset_turnover_zero():
    assert asset_turnover(100, 0) is None


def test_high_leverage_flag():
    assert high_leverage_flag(6.0) is True


def test_high_leverage_financial():
    assert high_leverage_flag(6.0, True) is False