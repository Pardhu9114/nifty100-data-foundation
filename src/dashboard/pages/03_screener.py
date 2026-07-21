import streamlit as st
import pandas as pd

from src.dashboard.utils.db import get_latest_ratios_with_company

st.set_page_config(
    page_title="Stock Screener",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 Nifty 100 Stock Screener")

# -----------------------------------------------------
# Load Data
# -----------------------------------------------------

df = get_latest_ratios_with_company()

if df.empty:
    st.error("No screening data available.")
    st.stop()

# -----------------------------------------------------
# Convert Numeric Columns
# -----------------------------------------------------

numeric_cols = [
    "return_on_equity_pct",
    "pe_ratio",
    "pb_ratio",
    "debt_to_equity",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "earnings_per_share",
    "market_cap_crore",
    "dividend_yield_pct",
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# -----------------------------------------------------
# Sidebar Filters
# -----------------------------------------------------

st.sidebar.header("📌 Filters")

search = st.sidebar.text_input("Search Company")

min_roe = st.sidebar.slider(
    "Minimum ROE (%)",
    min_value=0,
    max_value=100,
    value=0,
)

max_pe = st.sidebar.slider(
    "Maximum P/E Ratio",
    min_value=0,
    max_value=150,
    value=150,
)

max_de = st.sidebar.slider(
    "Maximum Debt / Equity",
    min_value=0.0,
    max_value=5.0,
    value=5.0,
    step=0.1,
)

min_margin = st.sidebar.slider(
    "Minimum Net Profit Margin (%)",
    min_value=0,
    max_value=100,
    value=0,
)

# -----------------------------------------------------
# Apply Filters
# -----------------------------------------------------

filtered = df.copy()

if search:
    filtered = filtered[
        filtered["company_name"].str.contains(
            search,
            case=False,
            na=False,
        )
    ]

filtered = filtered[
    filtered["return_on_equity_pct"].fillna(0) >= min_roe
]

filtered = filtered[
    filtered["pe_ratio"].isna()
    | (filtered["pe_ratio"] <= max_pe)
]

filtered = filtered[
    filtered["debt_to_equity"].isna()
    | (filtered["debt_to_equity"] <= max_de)
]

filtered = filtered[
    filtered["net_profit_margin_pct"].fillna(0) >= min_margin
]

# -----------------------------------------------------
# Summary
# -----------------------------------------------------

st.subheader("📊 Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Companies", len(filtered))

avg_roe = filtered["return_on_equity_pct"].mean()
avg_pe = filtered["pe_ratio"].mean()
avg_margin = filtered["net_profit_margin_pct"].mean()

c2.metric(
    "Average ROE",
    f"{avg_roe:.2f}%"
    if pd.notna(avg_roe)
    else "N/A",
)

c3.metric(
    "Average P/E",
    f"{avg_pe:.2f}"
    if pd.notna(avg_pe)
    else "N/A",
)

c4.metric(
    "Average Margin",
    f"{avg_margin:.2f}%"
    if pd.notna(avg_margin)
    else "N/A",
)

st.divider()

# -----------------------------------------------------
# Results
# -----------------------------------------------------

st.subheader("📋 Matching Companies")

display = filtered[
    [
        "company_name",
        "return_on_equity_pct",
        "pe_ratio",
        "pb_ratio",
        "debt_to_equity",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "earnings_per_share",
        "market_cap_crore",
        "dividend_yield_pct",
    ]
].copy()

display.columns = [
    "Company",
    "ROE (%)",
    "P/E",
    "P/B",
    "Debt/Equity",
    "Net Margin (%)",
    "Operating Margin (%)",
    "EPS",
    "Market Cap (Cr)",
    "Dividend Yield (%)",
]

display = display.sort_values(
    by="ROE (%)",
    ascending=False,
    na_position="last",
)

display["Market Cap (Cr)"] = display["Market Cap (Cr)"].apply(
    lambda x: f"{x:,.0f}" if pd.notna(x) else ""
)
display = display.round({
    "ROE (%)": 2,
    "P/E": 2,
    "P/B": 2,
    "Debt/Equity": 2,
    "Net Margin (%)": 2,
    "Operating Margin (%)": 2,
    "EPS": 2,
    "Dividend Yield (%)": 2,
})

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True,
)

st.caption(f"Showing {len(display)} companies")

# -----------------------------------------------------
# Download
# -----------------------------------------------------

st.download_button(
    label="⬇ Download CSV",
    data=display.to_csv(index=False),
    file_name="stock_screener.csv",
    mime="text/csv",
)

with st.sidebar:
    st.title("📈 Nifty100 Dashboard")
    st.caption("Sprint 1 - Data Foundation")