import streamlit as st
import pandas as pd

from src.dashboard.utils.db import (
    search_companies,
    get_company_reports,
)

st.set_page_config(
    page_title="Annual Reports",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Annual Reports")

# ---------------------------------------------------
# Company Selection
# ---------------------------------------------------

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

# ---------------------------------------------------
# Load Reports
# ---------------------------------------------------

reports = get_company_reports(company_id)

if reports.empty:
    st.warning("No annual reports are available for the selected company.")
    st.stop()

# ---------------------------------------------------
# Summary
# ---------------------------------------------------

c1, c2 = st.columns(2)

c1.metric(
    "Reports Available",
    len(reports)
)

c2.metric(
    "Latest Year",
    reports.iloc[0]["year"]
)

st.divider()

# ---------------------------------------------------
# Reports Table
# ---------------------------------------------------

st.subheader("Available Reports")

for _, row in reports.iterrows():

    with st.container():

        col1, col2 = st.columns([1, 5])

        col1.markdown(f"### {row['year']}")

        report = str(row["annual_report"])

        if report and report.lower() != "nan":

            if report.startswith("http://") or report.startswith("https://"):

                col2.link_button(
                    "📄 Open Annual Report",
                    report,
                    use_container_width=True,
                )

            else:
                col2.code(report)

        else:
            col2.write("Report not available")

        st.divider()

# ---------------------------------------------------
# Download CSV
# ---------------------------------------------------

st.download_button(
    "⬇ Download Report List",
    reports.to_csv(index=False),
    file_name=f"{company_id}_reports.csv",
    mime="text/csv",
)

# ---------------------------------------------------
# Raw Data
# ---------------------------------------------------

with st.expander("View Raw Data"):

    st.dataframe(
        reports,
        use_container_width=True,
        hide_index=True,
    )
with st.sidebar:
    st.title("📈 Nifty100 Dashboard")
    st.caption("Sprint 1 - Data Foundation")