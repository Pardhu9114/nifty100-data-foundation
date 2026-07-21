import streamlit as st
import pandas as pd

from src.dashboard.utils.db import (
    get_peer_groups,
    get_peer_comparison,
)

st.set_page_config(
    page_title="Peer Comparison",
    page_icon="👥",
    layout="wide",
)

st.title("👥 Peer Comparison")

# --------------------------------------------------
# Load Peer Groups
# --------------------------------------------------

peer_groups = get_peer_groups()

if peer_groups.empty:
    st.error("No peer groups available.")
    st.stop()

peer_group = st.selectbox(
    "Select Peer Group",
    peer_groups["peer_group_name"].tolist()
)

# --------------------------------------------------
# Load Comparison Data
# --------------------------------------------------

df = get_peer_comparison(peer_group)

if df.empty:
    st.warning("No companies found in this peer group.")
    st.stop()

# --------------------------------------------------
# Summary
# --------------------------------------------------

st.subheader("📊 Peer Group Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Companies", len(df))

avg_roe = df["return_on_equity_pct"].mean()
avg_pe = df["pe_ratio"].mean()
avg_margin = df["net_profit_margin_pct"].mean()

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
    "Average Margin",
    f"{avg_margin:.2f}%"
    if pd.notna(avg_margin)
    else "N/A"
)

st.markdown("---")

# --------------------------------------------------
# Comparison Table
# --------------------------------------------------

st.subheader("📋 Comparison Table")

display = df.copy()

display.columns = [
    "ID",
    "Company",
    "Benchmark",
    "ROE (%)",
    "Debt/Equity",
    "Net Margin (%)",
    "Operating Margin (%)",
    "EPS",
    "Market Cap (Cr)",
    "P/E",
    "P/B",
    "Dividend Yield (%)",
]

display["Market Cap (Cr)"] = display["Market Cap (Cr)"].apply(
    lambda x: f"{x:,.0f}" if pd.notna(x) else ""
)

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True,
)

# --------------------------------------------------
# Charts
# --------------------------------------------------

st.markdown("---")

st.subheader("📈 ROE Comparison")

roe_chart = df.set_index("company_name")[
    "return_on_equity_pct"
]

st.bar_chart(roe_chart)

st.subheader("💰 Market Cap Comparison")

market_chart = df.set_index("company_name")[
    "market_cap_crore"
]

st.bar_chart(market_chart)

st.subheader("📊 P/E Ratio Comparison")

pe_chart = df.set_index("company_name")[
    "pe_ratio"
]

st.bar_chart(pe_chart)

st.subheader("📉 Net Profit Margin Comparison")

margin_chart = df.set_index("company_name")[
    "net_profit_margin_pct"
]

st.bar_chart(margin_chart)

# --------------------------------------------------
# Download
# --------------------------------------------------

csv = display.to_csv(index=False)

st.download_button(
    label="⬇ Download Peer Comparison",
    data=csv,
    file_name="peer_comparison.csv",
    mime="text/csv",
)

with st.sidebar:
    st.title("📈 Nifty100 Dashboard")
    st.caption("Sprint 1 - Data Foundation")

