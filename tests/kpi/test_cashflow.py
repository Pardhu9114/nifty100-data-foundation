import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate
)


def test_free_cash_flow():
    assert free_cash_flow(
        500,
        -100
    ) == 400


def test_cfo_quality_high():
    assert (
        cfo_quality_score(
            200,
            100
        )
        == "High Quality"
    )


def test_cfo_quality_moderate():
    assert (
        cfo_quality_score(
            75,
            100
        )
        == "Moderate"
    )


def test_cfo_quality_low():
    assert (
        cfo_quality_score(
            30,
            100
        )
        == "Accrual Risk"
    )


def test_cfo_quality_zero_pat():
    assert (
        cfo_quality_score(
            100,
            0
        )
        is None
    )


def test_capex_asset_light():
    assert (
        capex_intensity(
            -20,
            1000
        )
        == "Asset Light"
    )


def test_capex_moderate():
    assert (
        capex_intensity(
            -50,
            1000
        )
        == "Moderate"
    )


def test_capex_capital_intensive():
    assert (
        capex_intensity(
            -150,
            1000
        )
        == "Capital Intensive"
    )


def test_fcf_conversion():
    assert round(
        fcf_conversion_rate(
            400,
            500
        ),
        2
    ) == 80.00


def test_fcf_conversion_zero():
    assert (
        fcf_conversion_rate(
            100,
            0
        )
        is None
    )
from src.analytics.cashflow_kpis import capital_allocation_pattern


def test_pattern_reinvestor():
    assert (
        capital_allocation_pattern(
            100,
            -50,
            -20
        )
        == "Reinvestor"
    )


def test_pattern_shareholder_returns():
    assert (
        capital_allocation_pattern(
            100,
            -50,
            -20,
            "High Quality"
        )
        == "Shareholder Returns"
    )


def test_pattern_mixed():
    assert (
        capital_allocation_pattern(
            100,
            -50,
            20
        )
        == "Mixed"
    )


def test_pattern_cash_accumulator():
    assert (
        capital_allocation_pattern(
            100,
            20,
            10
        )
        == "Cash Accumulator"
    )


def test_pattern_distress():
    assert (
        capital_allocation_pattern(
            -100,
            50,
            30
        )
        == "Distress Signal"
    )


def test_pattern_growth_debt():
    assert (
        capital_allocation_pattern(
            -100,
            -20,
            40
        )
        == "Growth Funded by Debt"
    )


def test_pattern_pre_revenue():
    assert (
        capital_allocation_pattern(
            -100,
            -50,
            -30
        )
        == "Pre-Revenue"
    )