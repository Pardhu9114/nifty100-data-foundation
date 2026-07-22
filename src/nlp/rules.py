import pandas as pd


# =====================================================
# Utility Functions
# =====================================================

def latest(df):
    """Return latest annual row excluding TTM."""

    temp = df[df["year"] != "TTM"].copy()

    if temp.empty:
        return None

    temp["sort_year"] = (
        temp["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    temp = temp.dropna(subset=["sort_year"])

    if temp.empty:
        return None

    temp["sort_year"] = temp["sort_year"].astype(int)

    temp = temp.sort_values("sort_year")

    return temp.iloc[-1]


def last_n(df, n):
    """Return last n annual rows."""

    temp = df[df["year"] != "TTM"].copy()

    if temp.empty:
        return pd.DataFrame()

    temp["sort_year"] = (
        temp["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    temp = temp.dropna(subset=["sort_year"])

    if temp.empty:
        return pd.DataFrame()

    temp["sort_year"] = temp["sort_year"].astype(int)

    temp = temp.sort_values("sort_year")

    return temp.tail(n)


def increasing(series):
    return all(x < y for x, y in zip(series[:-1], series[1:]))


def decreasing(series):
    return all(x > y for x, y in zip(series[:-1], series[1:]))


# =====================================================
# PRO RULES
# =====================================================

def pro_rule_01(ratios):

    data = last_n(ratios, 3)

    if len(data) < 3:
        return None

    if (data["return_on_equity_pct"] > 20).all():
        return {
            "type": "pro",
            "rule_id": "PRO_01",
            "text": (
                "Consistently high return on equity above 20% "
                "demonstrates exceptional capital efficiency."
            ),
            "confidence_pct": 95,
        }

    return None


def pro_rule_02(ratios):

    data = last_n(ratios, 5)

    if len(data) < 5:
        return None

    if (data["free_cash_flow_cr"] > 0).all():
        return {
            "type": "pro",
            "rule_id": "PRO_02",
            "text": (
                "Strong free cash flow generation over five years "
                "signals healthy business fundamentals."
            ),
            "confidence_pct": 92,
        }

    return None


def pro_rule_03(ratios):

    row = latest(ratios)

    if row is None:
        return None

    if row["debt_to_equity"] == 0:
        return {
            "type": "pro",
            "rule_id": "PRO_03",
            "text": (
                "Debt-free balance sheet provides financial "
                "flexibility and eliminates interest burden."
            ),
            "confidence_pct": 94,
        }

    return None


def pro_rule_05(ratios):

    row = latest(ratios)

    if row is None:
        return None

    if row["operating_profit_margin_pct"] > 25:
        return {
            "type": "pro",
            "rule_id": "PRO_05",
            "text": (
                "Operating profit margin above 25% indicates "
                "strong pricing power and cost discipline."
            ),
            "confidence_pct": 88,
        }

    return None


def pro_rule_07(ratios):

    row = latest(ratios)

    if row is None:
        return None

    if row["interest_coverage"] > 10 or row["debt_to_equity"] == 0:
        return {
            "type": "pro",
            "rule_id": "PRO_07",
            "text": (
                "Very high interest coverage ratio reflects "
                "negligible financial stress from debt servicing."
            ),
            "confidence_pct": 90,
        }

    return None


def pro_rule_10(ratios):

    data = last_n(ratios, 3)

    if len(data) < 3:
        return None

    if increasing(list(data["return_on_equity_pct"])):
        return {
            "type": "pro",
            "rule_id": "PRO_10",
            "text": (
                "Return on equity improving for three consecutive "
                "years shows strengthening business quality."
            ),
            "confidence_pct": 86,
        }

    return None


# =====================================================
# CON RULES
# =====================================================

def con_rule_01(ratios):

    row = latest(ratios)

    if row is None:
        return None

    if row["debt_to_equity"] > 2:
        return {
            "type": "con",
            "rule_id": "CON_01",
            "text": (
                f"Debt-to-equity ratio of {row['debt_to_equity']:.2f} "
                "is elevated and warrants monitoring."
            ),
            "confidence_pct": 90,
        }

    return None


def con_rule_02(ratios):

    data = last_n(ratios, 3)

    if len(data) < 3:
        return None

    if (data["free_cash_flow_cr"] < 0).all():
        return {
            "type": "con",
            "rule_id": "CON_02",
            "text": (
                "Free cash flow negative for three consecutive years "
                "raises concern about cash generation quality."
            ),
            "confidence_pct": 93,
        }

    return None


def con_rule_03(ratios):

    data = last_n(ratios, 3)

    if len(data) < 3:
        return None

    if decreasing(list(data["operating_profit_margin_pct"])):
        return {
            "type": "con",
            "rule_id": "CON_03",
            "text": (
                "Operating margins declining for three consecutive "
                "years suggest pricing or cost pressure."
            ),
            "confidence_pct": 85,
        }

    return None


def con_rule_06(ratios):

    row = latest(ratios)

    if row is None:
        return None

    if row["interest_coverage"] < 1.5:
        return {
            "type": "con",
            "rule_id": "CON_06",
            "text": (
                "Interest coverage ratio below 1.5x indicates "
                "risk in meeting debt obligations."
            ),
            "confidence_pct": 94,
        }

    return None


# =====================================================
# Rule Registry
# =====================================================

PRO_RULES = [
    pro_rule_01,
    pro_rule_02,
    pro_rule_03,
    pro_rule_05,
    pro_rule_07,
    pro_rule_10,
]

CON_RULES = [
    con_rule_01,
    con_rule_02,
    con_rule_03,
    con_rule_06,
]