import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📈 Nifty 100 Analytics Dashboard")

st.markdown("""
Welcome to the **Nifty 100 Analytics Dashboard**.

### Sprint 4 Dashboard Modules

- 🏠 Home
- 🏢 Company Profile
- 🔍 Screener
- 👥 Peer Comparison
- 📊 Trend Analysis
- 🏭 Sector Analysis
- 💰 Capital Allocation
- 📄 Annual Reports

Use the **sidebar** to navigate between pages.
""")

st.success("Dashboard initialized successfully.")