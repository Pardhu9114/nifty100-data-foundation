def format_currency(value):
    if value is None:
        return "N/A"

    if value >= 100000:
        return f"₹{value/100000:.2f} L Cr"

    if value >= 100:
        return f"₹{value:,.2f} Cr"

    return f"₹{value:.2f}"


def format_percent(value):
    if value is None:
        return "N/A"

    return f"{value:.2f}%"

st.metric(
    "Market Cap",
    format_currency(value)
)