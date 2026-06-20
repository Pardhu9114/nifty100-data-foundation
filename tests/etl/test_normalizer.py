import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.normaliser import (
    normalize_year,
    normalize_ticker
)

def test_year():
    assert normalize_year("FY23") == 2023

def test_ticker():
    assert normalize_ticker(" tcs ") == "TCS"