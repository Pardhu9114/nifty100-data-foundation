import streamlit as st
import pandas as pd

from src.dashboard.utils.db import (
    get_sectors,
    get_sector_summary,
    get_sector_details,
)

st.set_page_config(
    page_title="Sector Analysis",
    page_icon="🏭",
    layout="wide",
)

st.title("🏭 Sector Analysis")

# --------------------------------------------------
# Load Sectors
# --------------------------------------------------

sectors = get_sectors()

if sectors.empty:
    st.error("No sectors available.")
    st.stop()

selected_sector = st.selectbox(
    "Select Sector",
    sectors["broad_sector"].tolist()
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = get_sector_details(selected_sector)

if df.empty:
    st.warning("No companies found.")
    st.stop()

# --------------------------------------------------
# Summary
# --------------------------------------------------

st.subheader("📊 Sector Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Companies",
    len(df)
)

avg_roe = df["return_on_equity_pct"].mean()

avg_pe = df["pe_ratio"].mean()

market_cap = df["market_cap_crore"].sum()

c2.metric(
    "Average ROE",
    f"{avg_roe:.2f}%"
    if pd.notna(avg_roe)
    else "N/A"
)

c3.metric(
    "Average P/E",
    f"{avg_pe:.2f}"
    if pd.notna(avg_pe)
    else "N/A"
)

c4.metric(
    "Total Market Cap",
    f"{market_cap:,.0f} Cr"
    if pd.notna(market_cap)
    else "N/A"
)

st.markdown("---")

# --------------------------------------------------
# Market Cap Chart
# --------------------------------------------------

st.subheader("💰 Market Cap Comparison")

market = (
    df
    .set_index("company_name")["market_cap_crore"]
)

st.bar_chart(market)

# --------------------------------------------------
# ROE Chart
# --------------------------------------------------

st.subheader("📈 ROE Comparison")

roe = (
    df
    .set_index("company_name")["return_on_equity_pct"]
)

st.bar_chart(roe)

# --------------------------------------------------
# Net Profit Margin
# --------------------------------------------------

st.subheader("📊 Net Profit Margin")

margin = (
    df
    .set_index("company_name")["net_profit_margin_pct"]
)

st.bar_chart(margin)

# --------------------------------------------------
# Company Table
# --------------------------------------------------

st.subheader("📋 Companies")

display = df.copy()

display.columns = [
    "Company",
    "Sub Sector",
    "Index Weight %",
    "Market Cap Category",
    "ROE (%)",
    "Net Margin (%)",
    "Market Cap (Cr)",
    "P/E",
    "P/B"
]

display["Market Cap (Cr)"] = display["Market Cap (Cr)"].apply(
    lambda x: f"{x:,.0f}" if pd.notna(x) else ""
)

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True,
)

st.caption(f"Showing {len(display)} companies")

# --------------------------------------------------
# Download
# --------------------------------------------------

csv = display.to_csv(index=False)

st.download_button(
    "⬇ Download Sector Data",
    csv,
    file_name="sector_analysis.csv",
    mime="text/csv",
)

with st.sidebar:
    st.title("📈 Nifty100 Dashboard")
    st.caption("Sprint 1 - Data Foundation")