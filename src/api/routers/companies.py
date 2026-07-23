from pathlib import Path

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

from src.api.database import get_connection

router = APIRouter()


def fetch_history(table: str, ticker: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"""
        SELECT *
        FROM {table}
        WHERE company_id=?
        ORDER BY year
        """,
        (ticker.upper(),),
    )

    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


@router.get("/companies")
def get_companies():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            company_name,
            roce_percentage,
            roe_percentage
        FROM companies
        ORDER BY company_name
        """
    )

    data = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return data


@router.get("/companies/{ticker}")
def get_company(ticker: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM companies WHERE id=?",
        (ticker.upper(),),
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    return dict(row)


@router.get("/companies/{ticker}/pl")
def profit_loss(
    ticker: str,
    from_year: str | None = Query(default=None),
    to_year: str | None = Query(default=None),
):

    rows = fetch_history("profitandloss", ticker)

    if from_year:
        rows = [r for r in rows if r["year"] >= from_year]

    if to_year:
        rows = [r for r in rows if r["year"] <= to_year]

    return rows


@router.get("/companies/{ticker}/bs")
def balance_sheet(
    ticker: str,
):

    return fetch_history("balancesheet", ticker)


@router.get("/companies/{ticker}/cashflow")
def cash_flow(
    ticker: str,
):

    return fetch_history("cashflow", ticker)


@router.get("/companies/{ticker}/ratios")
def ratios(
    ticker: str,
    year: str | None = None,
):

    conn = get_connection()
    cursor = conn.cursor()

    if year:

        cursor.execute(
            """
            SELECT *
            FROM financial_ratios
            WHERE company_id=?
            AND year=?
            """,
            (ticker.upper(), year),
        )

    else:

        cursor.execute(
            """
            SELECT *
            FROM financial_ratios
            WHERE company_id=?
            ORDER BY year
            """,
            (ticker.upper(),),
        )

    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return rows


@router.get("/companies/{ticker}/tearsheet")
def tearsheet(ticker: str):

    pdf = (
        Path("reports")
        / "tearsheets"
        / f"{ticker.upper()}.pdf"
    )

    if not pdf.exists():

        raise HTTPException(
            status_code=404,
            detail="Tearsheet not found",
        )

    return FileResponse(
        pdf,
        media_type="application/pdf",
        filename=pdf.name,
    )