import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.normaliser import (
    normalize_year,
    normalize_ticker
)

# -----------------------
# normalize_year tests
# -----------------------

def test_year_fy23():
    assert normalize_year("FY23") == 2023

def test_year_fy22():
    assert normalize_year("FY22") == 2022

def test_year_fy21():
    assert normalize_year("FY21") == 2021

def test_year_fy20():
    assert normalize_year("FY20") == 2020

def test_year_fy19():
    assert normalize_year("FY19") == 2019

def test_year_dec2012():
    assert normalize_year("Dec 2012") == 2012

def test_year_mar2014():
    assert normalize_year("Mar 2014") == 2014

def test_year_mar2015():
    assert normalize_year("Mar 2015") == 2015

def test_year_mar2016():
    assert normalize_year("Mar 2016") == 2016

def test_year_mar2017():
    assert normalize_year("Mar 2017") == 2017

def test_year_mar2018():
    assert normalize_year("Mar 2018") == 2018

def test_year_mar2019():
    assert normalize_year("Mar 2019") == 2019

def test_year_mar2020():
    assert normalize_year("Mar 2020") == 2020

def test_year_mar2021():
    assert normalize_year("Mar 2021") == 2021

def test_year_mar2022():
    assert normalize_year("Mar 2022") == 2022

def test_year_mar2023():
    assert normalize_year("Mar 2023") == 2023

def test_year_mar2024():
    assert normalize_year("Mar 2024") == 2024

def test_year_integer():
    assert normalize_year(2023) == 2023

def test_year_string():
    assert normalize_year("2023") == 2023

def test_year_whitespace():
    assert normalize_year(" 2023 ") == 2023


# -----------------------
# normalize_ticker tests
# -----------------------

def test_ticker_tcs():
    assert normalize_ticker(" tcs ") == "TCS"

def test_ticker_reliance():
    assert normalize_ticker("reliance") == "RELIANCE"

def test_ticker_hdfc():
    assert normalize_ticker("hdfcbank") == "HDFCBANK"

def test_ticker_infy():
    assert normalize_ticker("INFY") == "INFY"

def test_ticker_wipro():
    assert normalize_ticker(" wipro ") == "WIPRO"

def test_ticker_vedl():
    assert normalize_ticker("vedl") == "VEDL"

def test_ticker_zomato():
    assert normalize_ticker("zomato") == "ZOMATO"

def test_ticker_vbl():
    assert normalize_ticker("vbl") == "VBL"

def test_ticker_abb():
    assert normalize_ticker("abb") == "ABB"

def test_ticker_ultracemco():
    assert normalize_ticker("ultracemco") == "ULTRACEMCO"

def test_ticker_unionbank():
    assert normalize_ticker("unionbank") == "UNIONBANK"

def test_ticker_spaces():
    assert normalize_ticker("   TCS   ") == "TCS"

def test_ticker_mixedcase():
    assert normalize_ticker("TcS") == "TCS"

def test_ticker_adanient():
    assert normalize_ticker("adanient") == "ADANIENT"

def test_ticker_adaniports():
    assert normalize_ticker("adaniports") == "ADANIPORTS"