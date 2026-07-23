from fastapi import APIRouter
from src.api.database import get_connection
import time

router = APIRouter()

START_TIME = time.time()


@router.get("/health")
def health_check():
    """
    Health check endpoint.
    """

    conn = get_connection()
    cursor = conn.cursor()

    tables = [
        "companies",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "analysis",
        "documents",
        "prosandcons",
        "peer_groups",
        "sectors",
    ]

    row_counts = {}

    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row_counts[table] = cursor.fetchone()[0]
        except Exception:
            row_counts[table] = "Table not found"

    conn.close()

    return {
        "status": "ok",
        "version": "1.0.0",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "db_row_counts": row_counts,
    }