from fastapi import APIRouter, HTTPException
import pandas as pd
import json

from src.screener.engine import (
    load_data,
    apply_filters,
    run_preset,
)

router = APIRouter()


@router.get("/screener")
def screener(
    preset: str | None = None,
    min_roe: float | None = None,
    max_de: float | None = None,
    min_fcf: float | None = None,
):
    """
    Stock screener endpoint.
    """

    try:

        # -----------------------------
        # Load Data
        # -----------------------------
        if preset:

            df = run_preset(preset)

        else:

            df = load_data()

            filters = {}

            if min_roe is not None:
                filters["roe_min"] = min_roe

            if max_de is not None:
                filters["debt_to_equity_max"] = max_de

            if min_fcf is not None:
                filters["fcf_min"] = min_fcf

            df = apply_filters(df, filters)

        # -----------------------------
        # Replace NaN with None
        # -----------------------------
        df = df.where(pd.notnull(df), None)

        # -----------------------------
        # Convert safely to JSON
        # -----------------------------
        records = json.loads(df.to_json(orient="records"))

        return records

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )