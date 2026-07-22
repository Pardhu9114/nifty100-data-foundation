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

def pro_rule_01(fr):

    latest_row = latest(fr)

    if latest_row is None:
        return None

    if latest_row["return_on_equity_pct"] >= 15:
        return {
            "type": "pro",
            "rule_id": "FR_PRO_01",
            "text": "Return on Equity is above 15%, indicating efficient use of shareholder capital.",
            "confidence_pct": 95,
        }

    return None


def pro_rule_02(fr):

    latest_row = latest(fr)

    if latest_row is None:
        return None

    if latest_row["debt_to_equity"] <= 1:
        return {
            "type": "pro",
            "rule_id": "FR_PRO_02",
            "text": "Debt-to-equity ratio is below 1, indicating a healthy capital structure.",
            "confidence_pct": 93,
        }

    return None


def pro_rule_03(fr):

    latest_row = latest(fr)

    if latest_row is None:
        return None

    if latest_row["interest_coverage"] >= 3:
        return {
            "type": "pro",
            "rule_id": "FR_PRO_03",
            "text": "Interest coverage is comfortably above 3, suggesting strong debt servicing ability.",
            "confidence_pct": 92,
        }

    return None

# =====================================================
# CON RULES
# =====================================================

def con_rule_01(fr):

    latest_row = latest(fr)

    if latest_row is None:
        return None

    if latest_row["return_on_equity_pct"] < 10:
        return {
            "type": "con",
            "rule_id": "FR_CON_01",
            "text": (
                "Return on Equity is below 10%, indicating weaker "
                "returns for shareholders."
            ),
            "confidence_pct": 95,
        }

    return None


def con_rule_02(fr):

    latest_row = latest(fr)

    if latest_row is None:
        return None

    if latest_row["debt_to_equity"] > 2:
        return {
            "type": "con",
            "rule_id": "FR_CON_02",
            "text": (
                "Debt-to-equity ratio is above 2, indicating "
                "high financial leverage."
            ),
            "confidence_pct": 93,
        }

    return None


def con_rule_03(fr):

    latest_row = latest(fr)

    if latest_row is None:
        return None

    if latest_row["interest_coverage"] < 1.5:
        return {
            "type": "con",
            "rule_id": "FR_CON_03",
            "text": (
                "Interest coverage is below 1.5, indicating "
                "difficulty servicing debt."
            ),
            "confidence_pct": 92,
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