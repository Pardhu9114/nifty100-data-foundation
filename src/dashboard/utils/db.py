import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = BASE_DIR / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


@st.cache_data(ttl=600)
def get_companies():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM companies", conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_ratios(company_id=None, year=None):
    conn = get_connection()

    query = "SELECT * FROM financial_ratios WHERE 1=1"
    params = []

    if company_id:
        query += " AND company_id=?"
        params.append(company_id)

    if year:
        query += " AND year=?"
        params.append(year)

    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_pl(company_id):
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM profitandloss WHERE company_id=?",
        conn,
        params=[company_id]
    )
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_bs(company_id):
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM balancesheet WHERE company_id=?",
        conn,
        params=[company_id]
    )
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_cf(company_id):
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM cashflow WHERE company_id=?",
        conn,
        params=[company_id]
    )
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_sectors():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM sectors", conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_peers(peer_group):
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM peer_percentiles WHERE peer_group_name=?",
        conn,
        params=[peer_group]
    )
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_valuation():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM market_cap", conn)
    conn.close()
    return df



@st.cache_data(ttl=600)
def get_sector_summary():
    conn = get_connection()

    query = """
    SELECT broad_sector,
           COUNT(*) AS companies
    FROM sectors
    GROUP BY broad_sector
    ORDER BY companies DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

# ==========================================================
# COMPANY DETAILS
# ==========================================================

@st.cache_data(ttl=600)
def get_company(company_id):
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM companies
        WHERE id = ?
        """,
        conn,
        params=[company_id],
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def search_companies(search_text=""):
    conn = get_connection()

    query = """
    SELECT
        id,
        company_name
    FROM companies
    WHERE
        company_name LIKE ?
        OR id LIKE ?
    ORDER BY company_name
    """

    df = pd.read_sql(
        query,
        conn,
        params=[
            f"%{search_text}%",
            f"%{search_text}%"
        ],
    )

    conn.close()

    df["company_name"] = (
        df["company_name"]
        .str.replace("\n", "", regex=False)
        .str.strip()
    )

    return df


# ==========================================================
# COMPANY RATIOS
# ==========================================================

@st.cache_data(ttl=600)
def get_company_ratios(company_id):
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY year DESC
        """,
        conn,
        params=[company_id],
    )

    conn.close()

    return df


# ==========================================================
# ANALYSIS
# ==========================================================

@st.cache_data(ttl=600)
def get_company_analysis(company_id):
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM analysis
        WHERE company_id = ?
        """,
        conn,
        params=[company_id],
    )

    conn.close()

    return df


# ==========================================================
# MARKET CAP / VALUATION
# ==========================================================

@st.cache_data(ttl=600)
def get_market_cap(company_id):
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM market_cap
        WHERE company_id = ?
        ORDER BY year DESC
        """,
        conn,
        params=[company_id],
    )

    conn.close()

    return df


# ==========================================================
# PROS & CONS
# ==========================================================

@st.cache_data(ttl=600)
def get_company_pros_cons(company_id):
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM prosandcons
        WHERE company_id = ?
        """,
        conn,
        params=[company_id],
    )

    conn.close()

    return df


# ==========================================================
# STOCK PRICES
# ==========================================================

@st.cache_data(ttl=600)
def get_stock_prices(company_id):
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM stock_prices
        WHERE company_id = ?
        ORDER BY date
        """,
        conn,
        params=[company_id],
    )

    conn.close()

    return df


# ==========================================================
# SECTOR DATA
# ==========================================================

@st.cache_data(ttl=600)
def get_sector_companies(sector):
    conn = get_connection()

    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector,
        s.sub_sector
    FROM companies c
    JOIN sectors s
        ON c.id = s.company_id
    WHERE s.broad_sector = ?
    ORDER BY c.company_name
    """

    df = pd.read_sql(query, conn, params=[sector])

    conn.close()

    return df


# ==========================================================
# PEER GROUPS
# ==========================================================

@st.cache_data(ttl=600)
def get_peer_groups():
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT DISTINCT peer_group_name
        FROM peer_groups
        ORDER BY peer_group_name
        """,
        conn,
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_peer_companies(peer_group):
    conn = get_connection()

    query = """
    SELECT
        pg.company_id,
        c.company_name,
        pg.is_benchmark
    FROM peer_groups pg
    JOIN companies c
        ON pg.company_id = c.id
    WHERE pg.peer_group_name = ?
    ORDER BY c.company_name
    """

    df = pd.read_sql(query, conn, params=[peer_group])

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_peer_percentiles(peer_group):
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM peer_percentiles
        WHERE peer_group_name = ?
        """,
        conn,
        params=[peer_group],
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_market_summary():
    conn = get_connection()

    query = """
    SELECT
        AVG(pe_ratio) AS avg_pe,
        AVG(pb_ratio) AS avg_pb,
        AVG(dividend_yield_pct) AS avg_dividend,
        AVG(ev_ebitda) AS avg_ev_ebitda
    FROM market_cap
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_top_market_cap(limit=10):
    conn = get_connection()

    query = """
    SELECT
        c.company_name,
        MAX(m.market_cap_crore) AS market_cap
    FROM market_cap m
    JOIN companies c
      ON c.id = m.company_id
    GROUP BY c.company_name
    ORDER BY market_cap DESC
    LIMIT ?
    """

    df = pd.read_sql(query, conn, params=[limit])

    conn.close()

    # Clean company names
    df["company_name"] = (
        df["company_name"]
        .str.replace("\n", "", regex=False)
        .str.strip()
    )

    return df

@st.cache_data(ttl=600)
def get_latest_ratios_with_company():
    conn = get_connection()

    query = """
    SELECT
    c.id,
    c.company_name,
    fr.year,
    fr.return_on_equity_pct,
    fr.debt_to_equity,
    fr.net_profit_margin_pct,
    fr.operating_profit_margin_pct,
    fr.earnings_per_share,
    mc.market_cap_crore,
    mc.pe_ratio,
    mc.pb_ratio,
    mc.dividend_yield_pct
FROM financial_ratios fr

JOIN companies c
ON fr.company_id = c.id

LEFT JOIN market_cap mc
ON fr.company_id = mc.company_id
AND fr.year = mc.year

JOIN (
    SELECT company_id, MAX(year) latest_year
    FROM financial_ratios
    GROUP BY company_id
) latest
ON fr.company_id = latest.company_id
AND fr.year = latest.latest_year
    """

    df = pd.read_sql(query, conn)

    conn.close()

    # Clean company names
    df["company_name"] = (
        df["company_name"]
        .str.replace("\n", "", regex=False)
        .str.strip()
    )

    # Remove duplicate companies
    df = df.drop_duplicates(subset="company_name", keep="first")

    return df

@st.cache_data(ttl=600)
def get_latest_ratios():
    conn = get_connection()

    query = """
    SELECT fr.*
    FROM financial_ratios fr
    JOIN (
        SELECT company_id, MAX(year) AS latest_year
        FROM financial_ratios
        GROUP BY company_id
    ) latest
      ON fr.company_id = latest.company_id
     AND fr.year = latest.latest_year
    """

    df = pd.read_sql(query, conn)

    conn.close()

    # Remove duplicate latest records
    df = df.drop_duplicates(subset="company_id", keep="first")

    return df

@st.cache_data(ttl=600)
def search_companies(search_text=""):
    conn = get_connection()

    query = """
    SELECT
        id,
        company_name
    FROM companies
    WHERE
        company_name LIKE ?
        OR id LIKE ?
    ORDER BY company_name
    """

    df = pd.read_sql(
        query,
        conn,
        params=[
            f"%{search_text}%",
            f"%{search_text}%"
        ]
    )

    conn.close()

    df["company_name"] = (
        df["company_name"]
        .str.replace("\n", "", regex=False)
        .str.strip()
    )

    return df

@st.cache_data(ttl=600)
def get_latest_company_ratio(company_id):
    df = get_company_ratios(company_id)

    if df.empty:
        return None

    return df.sort_values("year", ascending=False).iloc[0]


@st.cache_data(ttl=600)
def get_latest_market_cap(company_id):
    df = get_market_cap(company_id)

    if df.empty:
        return None

    return df.sort_values("year", ascending=False).iloc[0]

import re


def _extract_percent(text):
    if text is None:
        return None

    match = re.search(r"(-?\d+(\.\d+)?)\s*%", str(text))

    if match:
        return float(match.group(1))

    return None

@st.cache_data(ttl=600)
def get_company_growth_metrics(company_id):
    df = get_company_analysis(company_id)

    metrics = {
        "sales_cagr": None,
        "profit_cagr": None,
        "stock_cagr": None,
        "roe": None,
    }

    if df.empty:
        return metrics

    for _, row in df.iterrows():

        sales = _extract_percent(row["compounded_sales_growth"])
        profit = _extract_percent(row["compounded_profit_growth"])
        stock = _extract_percent(row["stock_price_cagr"])
        roe = _extract_percent(row["roe"])

        if sales is not None:
            metrics["sales_cagr"] = sales

        if profit is not None:
            metrics["profit_cagr"] = profit

        if stock is not None:
            metrics["stock_cagr"] = stock

        if roe is not None:
            metrics["roe"] = roe

    return metrics

def fmt_number(value, digits=2):

    if value is None or pd.isna(value):
        return "N/A"

    return f"{value:.{digits}f}"


def fmt_percent(value, digits=2):

    if value is None or pd.isna(value):
        return "N/A"

    return f"{value:.{digits}f}%"


def fmt_currency(value):

    if value is None or pd.isna(value):
        return "N/A"

    return f"{value:,.0f}"

@st.cache_data(ttl=600)
def get_peer_comparison(peer_group):
    conn = get_connection()

    query = """
    SELECT
        c.id,
        c.company_name,
        pg.is_benchmark,
        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.net_profit_margin_pct,
        fr.operating_profit_margin_pct,
        fr.earnings_per_share,
        mc.market_cap_crore,
        mc.pe_ratio,
        mc.pb_ratio,
        mc.dividend_yield_pct
    FROM peer_groups pg

    JOIN companies c
        ON pg.company_id = c.id

    LEFT JOIN (
        SELECT *
        FROM financial_ratios fr
        WHERE year = (
            SELECT MAX(fr2.year)
            FROM financial_ratios fr2
            WHERE fr2.company_id = fr.company_id
        )
    ) fr
        ON pg.company_id = fr.company_id

    LEFT JOIN (
        SELECT *
        FROM market_cap mc
        WHERE year = (
            SELECT MAX(mc2.year)
            FROM market_cap mc2
            WHERE mc2.company_id = mc.company_id
        )
    ) mc
        ON pg.company_id = mc.company_id

    WHERE pg.peer_group_name = ?

    ORDER BY c.company_name
    """

    df = pd.read_sql(query, conn, params=[peer_group])

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_sectors():
    conn = get_connection()

    query = """
    SELECT DISTINCT broad_sector
    FROM sectors
    ORDER BY broad_sector
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_sector_companies(broad_sector):
    conn = get_connection()

    query = """
    SELECT
        s.company_id,
        c.company_name,
        s.sub_sector,
        s.index_weight_pct,
        s.market_cap_category
    FROM sectors s
    JOIN companies c
        ON s.company_id = c.id
    WHERE s.broad_sector = ?
    ORDER BY c.company_name
    """

    df = pd.read_sql(query, conn, params=[broad_sector])

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_sector_summary(broad_sector):
    conn = get_connection()

    query = """
    SELECT
        c.company_name,
        s.sub_sector,
        s.index_weight_pct,
        s.market_cap_category,
        fr.return_on_equity_pct,
        fr.net_profit_margin_pct,
        mc.market_cap_crore,
        mc.pe_ratio,
        mc.pb_ratio
    FROM sectors s

    JOIN companies c
        ON s.company_id = c.id

    LEFT JOIN (
        SELECT *
        FROM financial_ratios fr
        WHERE year = (
            SELECT MAX(fr2.year)
            FROM financial_ratios fr2
            WHERE fr2.company_id = fr.company_id
        )
    ) fr
        ON s.company_id = fr.company_id

    LEFT JOIN (
        SELECT *
        FROM market_cap mc
        WHERE year = (
            SELECT MAX(mc2.year)
            FROM market_cap mc2
            WHERE mc2.company_id = mc.company_id
        )
    ) mc
        ON s.company_id = mc.company_id

    WHERE s.broad_sector = ?

    ORDER BY mc.market_cap_crore DESC
    """

    df = pd.read_sql(query, conn, params=[broad_sector])

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_company_reports(company_id):
    conn = get_connection()

    query = """
    SELECT
        year,
        annual_report
    FROM documents
    WHERE company_id = ?
    ORDER BY year DESC
    """

    df = pd.read_sql(query, conn, params=[company_id])

    conn.close()

    return df