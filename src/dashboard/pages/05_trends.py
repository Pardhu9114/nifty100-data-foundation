import streamlit as st
import pandas as pd

from src.dashboard.utils.db import (
    search_companies,
    get_pl,
    get_bs,
    get_cf,
    get_stock_prices,
)

st.set_page_config(
    page_title="Trend Analysis",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Trend Analysis")

# ----------------------------------------------------
# Company Selection
# ----------------------------------------------------

companies = search_companies("")

selected = st.selectbox(
    "Select Company",
    (
        companies["company_name"] +
        " (" +
        companies["id"] +
        ")"
    ).tolist()
)

company_id = selected.split("(")[-1].replace(")", "").strip()

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------

pl = get_pl(company_id)
bs = get_bs(company_id)
cf = get_cf(company_id)
prices = get_stock_prices(company_id)

# ----------------------------------------------------
# Profit & Loss
# ----------------------------------------------------

st.header("📊 Profit & Loss Trends")

if not pl.empty:

    chart = (
        pl.sort_values("year")
        .set_index("year")
    )

    st.subheader("Revenue")

    st.line_chart(chart["sales"])

    st.subheader("Net Profit")

    st.line_chart(chart["net_profit"])

else:
   st.info("No Profit & Loss data is available for the selected company.")

st.divider()

# ----------------------------------------------------
# Balance Sheet
# ----------------------------------------------------

st.header("🏦 Balance Sheet Trends")

if not bs.empty:

    chart = (
        bs.sort_values("year")
        .set_index("year")
    )

    if "total_assets" in chart.columns:
        st.subheader("Total Assets")
        st.line_chart(chart["total_assets"])

    if "borrowings" in chart.columns:
        st.subheader("Borrowings")
        st.line_chart(chart["borrowings"])

else:
    st.info("No Balance Sheet data is available for the selected company.")

st.divider()

# ----------------------------------------------------
# Cash Flow
# ----------------------------------------------------

st.header("💰 Cash Flow Trends")

if not cf.empty:

    chart = (
        cf.sort_values("year")
        .set_index("year")
    )

    if "operating_activity" in chart.columns:
        st.subheader("Operating Cash Flow")
        st.line_chart(chart["operating_activity"])

    if "investing_activity" in chart.columns:
        st.subheader("Investing Cash Flow")
        st.line_chart(chart["investing_activity"])

    if "financing_activity" in chart.columns:
        st.subheader("Financing Cash Flow")
        st.line_chart(chart["financing_activity"])

else:
    st.info("No Cash Flow data is available for the selected company.")

st.divider()

# ----------------------------------------------------
# Stock Price
# ----------------------------------------------------

st.header("📉 Stock Price Trend")

if not prices.empty:

    prices = prices.copy()

    prices["date"] = pd.to_datetime(prices["date"])

    prices = prices.sort_values("date")

    st.line_chart(
        prices.set_index("date")["close_price"]
    )

else:
    st.info("No stock price history is available for the selected company.")

with st.sidebar:
    st.title("📈 Nifty100 Dashboard")
    st.caption("Sprint 1 - Data Foundation")