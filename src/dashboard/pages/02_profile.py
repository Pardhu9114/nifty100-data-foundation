
import streamlit as st
import pandas as pd

from src.dashboard.utils.db import (
    search_companies,
    get_company,
    get_company_ratios,
    get_company_analysis,
    get_market_cap,
    get_pl,
    get_bs,
    get_cf,
    get_stock_prices,
    get_company_pros_cons,
)

st.set_page_config(
    page_title="Company Profile",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Company Profile")

# ---------------------------------------------------
# Search
# ---------------------------------------------------

search_text = st.text_input(
    "🔍 Search Company",
    placeholder="Example: TCS, Infosys, Reliance..."
)

companies = search_companies(search_text)

if companies.empty:
    st.warning("No matching company found.")
    st.stop()

company_display = (
    companies["company_name"].astype(str).str.strip()
    + " ("
    + companies["id"].astype(str).str.strip()
    + ")"
)

options = (
    companies["company_name"].astype(str)
    + " ("
    + companies["id"].astype(str)
    + ")"
).tolist()

default_index = 0

for i, option in enumerate(options):
    if "(ABB)" in option:
        default_index = i
        break

selected = st.selectbox(
    "Select Company",
    options,
    index=default_index,
)

company_id = selected.split("(")[-1].replace(")", "").strip()





# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

company = get_company(company_id)
ratios = get_company_ratios(company_id)
analysis = get_company_analysis(company_id)
valuation = get_market_cap(company_id)
pl = get_pl(company_id)
prices = get_stock_prices(company_id)
bs = get_bs(company_id)
cf = get_cf(company_id)

pros_cons = get_company_pros_cons(company_id)

if company.empty:
    st.error("Company data not available.")
    st.stop()

company = company.iloc[0]

latest_ratio = (
    ratios.sort_values("year", ascending=False).iloc[0]
    if not ratios.empty
    else None
)

latest_analysis = (
    analysis.iloc[0]
    if not analysis.empty
    else None
)

latest_valuation = (
    valuation.sort_values("year", ascending=False).iloc[0]
    if not valuation.empty
    else None
)

# ---------------------------------------------------
# Company Card
# ---------------------------------------------------

st.markdown("---")

left, right = st.columns([1, 3])

with left:

    if pd.notna(company["company_logo"]):
        st.image(company["company_logo"], width=120)

with right:

    st.subheader(company["company_name"])

    st.caption(company_id)

    if pd.notna(company["website"]):
        st.markdown(f"🌐 {company['website']}")

    if pd.notna(company["about_company"]):
        st.write(company["about_company"])

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------

st.markdown("---")

k1, k2, k3 = st.columns(3)

k4, k5, k6 = st.columns(3)

with k1:

    roe = (
        latest_ratio["return_on_equity_pct"]
        if latest_ratio is not None
        else None
    )

    st.metric(
        "ROE",
        f"{roe:.2f}%"
        if pd.notna(roe)
        else "N/A"
    )

with k2:

    roce = company["roce_percentage"]

    st.metric(
        "ROCE",
        f"{roce:.2f}%"
        if pd.notna(roce)
        else "N/A"
    )

with k3:

    pe = (
        latest_valuation["pe_ratio"]
        if latest_valuation is not None
        else None
    )

    st.metric(
        "P/E Ratio",
        f"{pe:.2f}"
        if pd.notna(pe)
        else "N/A"
    )

with k4:

    pb = (
        latest_valuation["pb_ratio"]
        if latest_valuation is not None
        else None
    )

    st.metric(
        "P/B Ratio",
        f"{pb:.2f}"
        if pd.notna(pb)
        else "N/A"
    )

with k5:

    market_cap = (
        latest_valuation["market_cap_crore"]
        if latest_valuation is not None
        else None
    )

    st.metric(
        "Market Cap (Cr)",
        f"{market_cap:,.0f}"
        if pd.notna(market_cap)
        else "N/A"
    )

with k6:

    sales_growth = (
        latest_analysis["compounded_sales_growth"]
        if latest_analysis is not None
        else "N/A"
    )

    st.metric(
        "Sales CAGR",
        str(sales_growth)
    )

st.markdown("---")

# ---------------------------------------------------
# Revenue & Net Profit
# ---------------------------------------------------

st.subheader("📈 Revenue vs Net Profit")

if not pl.empty:

    chart_df = (
        pl.sort_values("year")
        .set_index("year")[["sales", "net_profit"]]
    )

    st.line_chart(chart_df)

else:
    st.info("No Profit & Loss data is available for the selected company.")

st.markdown("---")
# ---------------------------------------------------
# ROE vs ROCE
# ---------------------------------------------------

st.subheader("📊 ROE vs ROCE Trend")

if not ratios.empty:

    ratio_chart = ratios.sort_values("year").copy()

    ratio_chart["ROCE"] = company["roce_percentage"]

    ratio_chart = ratio_chart.set_index("year")[
        [
            "return_on_equity_pct",
            "ROCE",
        ]
    ]

    ratio_chart.columns = [
        "ROE",
        "ROCE",
    ]

    st.line_chart(ratio_chart)

else:
    st.info("No historical ratio data is available for the selected company.")

st.markdown("---")
# ---------------------------------------------------
# Stock Price
# ---------------------------------------------------

st.subheader("📉 Stock Price History")

if not prices.empty:

    prices = prices.copy()

    prices["date"] = pd.to_datetime(prices["date"])

    prices = prices.sort_values("date")

    chart = prices.set_index("date")[
        "close_price"
    ]

    st.line_chart(chart)

else:
    st.info("No stock price history is available for the selected company.")

st.markdown("---")

# ---------------------------------------------------
# Pros & Cons
# ---------------------------------------------------

st.subheader("✅ Pros & Cons")

left, right = st.columns(2)

if not pros_cons.empty:

    row = pros_cons.iloc[0]

    with left:
        st.success("Pros")

        pros = str(row["pros"]).split("\n")

        for p in pros:
            if p.strip():
                st.write("✔", p.strip())

    with right:
        st.error("Cons")

        cons = str(row["cons"]).split("\n")

        for c in cons:
            if c.strip():
                st.write("✖", c.strip())

else:

    st.info("Pros & Cons not available.")

st.markdown("---")

st.subheader("📑 Financial Statements")

tab1, tab2, tab3 = st.tabs(
    [
        "Profit & Loss",
        "Balance Sheet",
        "Cash Flow"
    ]
)

with tab1:

    if pl.empty:

        st.info("No Profit & Loss data.")

    else:

        display = pl.sort_values(
            "year",
            ascending=False
        ).copy()

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )

with tab2:

    if bs.empty:

        st.info("No Balance Sheet data.")

    else:

        display = bs.sort_values(
            "year",
            ascending=False
        ).copy()

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )

with tab3:

    if cf.empty:

        st.info("No Cash Flow data.")

    else:

        display = cf.sort_values(
            "year",
            ascending=False
        ).copy()

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )

st.markdown("---")

st.caption(
    "Financial data sourced from the SQLite database."
)


with st.sidebar:
    st.title("📈 Nifty100 Dashboard")
    st.caption("Sprint 1 - Data Foundation")
