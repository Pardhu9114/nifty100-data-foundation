import pandas as pd
import plotly.express as px
import streamlit as st


from src.dashboard.utils.db import (
    get_companies,
    get_latest_ratios,
    get_latest_ratios_with_company,
    get_market_summary,
    get_top_market_cap,
    get_connection,
)

st.set_page_config(page_title="Home", layout="wide")

st.title("📊 NIFTY100 Data Foundation Dashboard")
st.markdown("---")

# ==================================================
# Load Data
# ==================================================

companies = get_companies()
ratios = get_latest_ratios()
latest_table = get_latest_ratios_with_company()
market = get_market_summary()
top_market = get_top_market_cap()

conn = get_connection()

sector = pd.read_sql("""
SELECT
    broad_sector,
    COUNT(*) AS companies
FROM sectors
GROUP BY broad_sector
ORDER BY companies DESC
""", conn)

conn.close()

# ==================================================
# Clean ROE (Remove Extreme Outliers)
# ==================================================

clean_roe = ratios[
    ratios["return_on_equity_pct"].between(-50, 100)
]

avg_roe = clean_roe["return_on_equity_pct"].mean()

# ==================================================
# KPI Cards
# ==================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Companies",
        f"{len(companies)}"
    )

with col2:
    st.metric(
        "Average ROE",
        f"{avg_roe:.2f}%"
    )

with col3:
    st.metric(
        "Average P/E",
        f"{market.iloc[0]['avg_pe']:.2f}×"
    )

with col4:
    st.metric(
        "Dividend Yield",
        f"{market.iloc[0]['avg_dividend']:.2f}%"
    )

st.markdown("---")

# ==================================================
# Charts
# ==================================================

left, right = st.columns(2)

with left:

    fig = px.pie(
        sector,
        names="broad_sector",
        values="companies",
        hole=0.55,
        title="Sector Distribution"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.bar(
        top_market,
        x="market_cap",
        y="company_name",
        orientation="h",
        title="Top 10 Companies by Market Capitalization",
        labels={
            "market_cap": "Market Cap (₹ Crore)",
            "company_name": "Company"
        },
        text="market_cap"
    )

    fig.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        xaxis_tickformat=","
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# ==================================================
# Latest Financial Ratios
# ==================================================

st.subheader("📑 Latest Financial Ratios")

display_table = latest_table.copy()

display_table = display_table.rename(
    columns={
        "company_name": "Company",
        "year": "Year",
        "return_on_equity_pct": "ROE (%)",
        "debt_to_equity": "Debt / Equity",
        "net_profit_margin_pct": "Net Profit Margin (%)",
        "earnings_per_share": "EPS",
    }
)

numeric_cols = [
    "ROE (%)",
    "Debt / Equity",
    "Net Profit Margin (%)",
    "EPS",
]

display_table[numeric_cols] = display_table[numeric_cols].round(2)

st.dataframe(
    display_table,
    use_container_width=True,
    hide_index=True
)
with st.sidebar:
    st.title("📈 Nifty100 Dashboard")
    st.caption("Sprint 1 - Data Foundation")

st.divider()

st.caption(
    "Developed by CH Venkata Sai Pardhu | Sprint 1 - Data Foundation"
)