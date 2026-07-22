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

def pro_rule_01(cashflow):

    data = last_n(cashflow, 3)

    if len(data) < 3:
        return None

    if (data["operating_activity"] > 0).all():
        return {
            "type": "pro",
            "rule_id": "CF_PRO_01",
            "text": (
                "Operating cash flow has remained positive for "
                "the last three years, indicating healthy "
                "core business operations."
            ),
            "confidence_pct": 94,
        }

    return None


def pro_rule_02(cashflow):

    data = last_n(cashflow, 3)

    if len(data) < 3:
        return None

    if increasing(list(data["operating_activity"])):
        return {
            "type": "pro",
            "rule_id": "CF_PRO_02",
            "text": (
                "Operating cash flow has improved consistently "
                "over the last three years."
            ),
            "confidence_pct": 90,
        }

    return None


def pro_rule_03(cashflow):

    row = latest(cashflow)

    if row is None:
        return None

    if row["net_cash_flow"] > 0:
        return {
            "type": "pro",
            "rule_id": "CF_PRO_03",
            "text": (
                "Latest year's net cash flow is positive, "
                "reflecting healthy cash generation."
            ),
            "confidence_pct": 88,
        }

    return None

# =====================================================
# CON RULES
# =====================================================

def con_rule_01(cashflow):

    row = latest(cashflow)

    if row is None:
        return None

    if row["operating_activity"] < 0:
        return {
            "type": "con",
            "rule_id": "CF_CON_01",
            "text": (
                "Latest operating cash flow is negative, "
                "which may indicate weakness in core operations."
            ),
            "confidence_pct": 94,
        }

    return None


def con_rule_02(cashflow):

    data = last_n(cashflow, 3)

    if len(data) < 3:
        return None

    if (data["net_cash_flow"] < 0).all():
        return {
            "type": "con",
            "rule_id": "CF_CON_02",
            "text": (
                "Net cash flow has remained negative for three "
                "consecutive years."
            ),
            "confidence_pct": 92,
        }

    return None


def con_rule_03(cashflow):

    data = last_n(cashflow, 3)

    if len(data) < 3:
        return None

    if (data["financing_activity"] > 0).all():
        return {
            "type": "con",
            "rule_id": "CF_CON_03",
            "text": (
                "Consistently positive financing cash flow may "
                "indicate dependence on external funding."
            ),
            "confidence_pct": 87,
        }

    return None

# =====================================================
# Rule Registry
# =====================================================

PRO_RULES = [
    pro_rule_01,
    pro_rule_02,
    pro_rule_03,
]

CON_RULES = [
    con_rule_01,
    con_rule_02,
    con_rule_03,
]