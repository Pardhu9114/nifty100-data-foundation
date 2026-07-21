import streamlit as st
import pandas as pd

from src.dashboard.utils.db import (
    search_companies,
    get_bs,
    get_cf,
)

st.set_page_config(
    page_title="Capital Allocation",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Capital Allocation")

# --------------------------------------------------
# Company Selection
# --------------------------------------------------

companies = search_companies("")

selected = st.selectbox(
    "Select Company",
    (
        companies["company_name"]
        + " ("
        + companies["id"]
        + ")"
    ).tolist()
)

company_id = selected.split("(")[-1].replace(")", "").strip()

# --------------------------------------------------
# Load Data
# --------------------------------------------------

bs = get_bs(company_id)
cf = get_cf(company_id)

if bs.empty and cf.empty:
    st.warning("No capital allocation data available.")
    st.stop()

# --------------------------------------------------
# Balance Sheet Trends
# --------------------------------------------------

st.header("🏦 Balance Sheet")

if not bs.empty:

    chart = bs.sort_values("year").set_index("year")

    cols = st.columns(2)

    if "borrowings" in chart.columns:
        with cols[0]:
            st.subheader("Borrowings")
            st.line_chart(chart["borrowings"])

    if "total_assets" in chart.columns:
        with cols[1]:
            st.subheader("Total Assets")
            st.line_chart(chart["total_assets"])

else:
    st.info("No Balance Sheet data is available for the selected company.")

st.divider()

# --------------------------------------------------
# Cash Flow Trends
# --------------------------------------------------

st.header("💵 Cash Flow Analysis")

if not cf.empty:

    chart = cf.sort_values("year").set_index("year")

    cols = st.columns(3)

    if "operating_activity" in chart.columns:
        with cols[0]:
            st.subheader("Operating")
            st.line_chart(chart["operating_activity"])

    if "investing_activity" in chart.columns:
        with cols[1]:
            st.subheader("Investing")
            st.line_chart(chart["investing_activity"])

    if "financing_activity" in chart.columns:
        with cols[2]:
            st.subheader("Financing")
            st.line_chart(chart["financing_activity"])

    st.divider()

    if "net_cash_flow" in chart.columns:
        st.subheader("Net Cash Flow")
        st.line_chart(chart["net_cash_flow"])

else:
    st.info("No Cash Flow data is available for the selected company.")

# --------------------------------------------------
# Tables
# --------------------------------------------------

st.header("📋 Financial Tables")

tab1, tab2 = st.tabs(
    [
        "Balance Sheet",
        "Cash Flow"
    ]
)

with tab1:

    if not bs.empty:
        st.dataframe(
            bs.sort_values(
                "year",
                ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )

with tab2:

    if not cf.empty:
        st.dataframe(
            cf.sort_values(
                "year",
                ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )

# --------------------------------------------------
# Download
# --------------------------------------------------

st.divider()

if not bs.empty:

    st.download_button(
        "⬇ Download Balance Sheet",
        bs.to_csv(index=False),
        file_name=f"{company_id}_balance_sheet.csv",
        mime="text/csv",
    )

if not cf.empty:

    st.download_button(
        "⬇ Download Cash Flow",
        cf.to_csv(index=False),
        file_name=f"{company_id}_cash_flow.csv",
        mime="text/csv",
    )

with st.sidebar:
    st.title("📈 Nifty100 Dashboard")
    st.caption("Sprint 1 - Data Foundation")