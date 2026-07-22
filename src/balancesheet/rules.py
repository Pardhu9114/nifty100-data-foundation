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

def pro_rule_01(bs):

    data = last_n(bs, 3)

    if len(data) < 3:
        return None

    if decreasing(list(data["borrowings"])):
        return {
            "type": "pro",
            "rule_id": "BS_PRO_01",
            "text": (
                "Borrowings have reduced consistently over the "
                "last three years, improving financial strength."
            ),
            "confidence_pct": 92,
        }

    return None


def pro_rule_02(bs):

    data = last_n(bs, 3)

    if len(data) < 3:
        return None

    if increasing(list(data["reserves"])):
        return {
            "type": "pro",
            "rule_id": "BS_PRO_02",
            "text": (
                "Reserves have grown consistently over the "
                "last three years."
            ),
            "confidence_pct": 90,
        }

    return None


def pro_rule_03(bs):

    data = last_n(bs, 3)

    if len(data) < 3:
        return None

    if increasing(list(data["total_assets"])):
        return {
            "type": "pro",
            "rule_id": "BS_PRO_03",
            "text": (
                "Total assets have increased steadily over the "
                "last three years."
            ),
            "confidence_pct": 88,
        }

    return None

# =====================================================
# CON RULES
# =====================================================

def con_rule_01(bs):

    data = last_n(bs, 3)

    if len(data) < 3:
        return None

    if increasing(list(data["borrowings"])):
        return {
            "type": "con",
            "rule_id": "BS_CON_01",
            "text": (
                "Borrowings have increased consistently over the "
                "last three years, increasing financial leverage."
            ),
            "confidence_pct": 92,
        }

    return None


def con_rule_02(bs):

    data = last_n(bs, 3)

    if len(data) < 3:
        return None

    if decreasing(list(data["reserves"])):
        return {
            "type": "con",
            "rule_id": "BS_CON_02",
            "text": (
                "Reserves have declined over the last three years."
            ),
            "confidence_pct": 90,
        }

    return None


def con_rule_03(bs):

    data = last_n(bs, 3)

    if len(data) < 3:
        return None

    if increasing(list(data["other_liabilities"])):
        return {
            "type": "con",
            "rule_id": "BS_CON_03",
            "text": (
                "Other liabilities have increased steadily over "
                "the last three years."
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