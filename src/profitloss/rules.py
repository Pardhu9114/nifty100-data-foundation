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

def pro_rule_01(pl):

    data = last_n(pl, 3)

    if len(data) < 3:
        return None

    if increasing(list(data["sales"])):
        return {
            "type": "pro",
            "rule_id": "PL_PRO_01",
            "text": "Sales have grown consistently over the last three years.",
            "confidence_pct": 92,
        }

    return None


def pro_rule_02(pl):

    data = last_n(pl, 3)

    if len(data) < 3:
        return None

    if increasing(list(data["net_profit"])):
        return {
            "type": "pro",
            "rule_id": "PL_PRO_02",
            "text": "Net profit has increased consistently over the last three years.",
            "confidence_pct": 94,
        }

    return None


def pro_rule_03(pl):

    data = last_n(pl, 3)

    if len(data) < 3:
        return None

    if increasing(list(data["operating_profit"])):
        return {
            "type": "pro",
            "rule_id": "PL_PRO_03",
            "text": "Operating profit has improved steadily over the last three years.",
            "confidence_pct": 91,
        }

    return None

# =====================================================
# CON RULES
# =====================================================

def con_rule_01(pl):

    data = last_n(pl, 3)

    if len(data) < 3:
        return None

    if decreasing(list(data["sales"])):
        return {
            "type": "con",
            "rule_id": "PL_CON_01",
            "text": "Sales have declined consistently over the last three years.",
            "confidence_pct": 92,
        }

    return None


def con_rule_02(pl):

    data = last_n(pl, 3)

    if len(data) < 3:
        return None

    if decreasing(list(data["net_profit"])):
        return {
            "type": "con",
            "rule_id": "PL_CON_02",
            "text": "Net profit has declined consistently over the last three years.",
            "confidence_pct": 94,
        }

    return None


def con_rule_03(pl):

    data = last_n(pl, 3)

    if len(data) < 3:
        return None

    if decreasing(list(data["operating_profit"])):
        return {
            "type": "con",
            "rule_id": "PL_CON_03",
            "text": "Operating profit has weakened steadily over the last three years.",
            "confidence_pct": 91,
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