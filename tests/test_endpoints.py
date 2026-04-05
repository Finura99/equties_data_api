import pandas as pd
from pathlib import Path
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)

BASE_DIR = Path(__file__).resolve().parent.parent ##root directory
PRICES_PATH = BASE_DIR / "data" / "prices.csv"
"""
def test_get_price_from_df_returns_aapl():

    df = pd.read_csv(PRICES_PATH) #load csv

    result = get_price_from_df(df, "AAPL") #test function here

    assert result is not None #expect result not to be none
    assert result["symbol"] == "AAPL"
    assert "price" in result
    assert "prev_price" in result

    ##symbol does not exist test below


def test_get_price_from_df_returns_none():

    df = pd.DataFrame({
        "symbol" : ["AAPL", "MSFT"],
        "price" : [200.2, 300.1],
        "prev_price" : [198.0, 295.1],
    })

    result = get_price_from_df(df, "GOOGL")

    assert result is None

def test_get_price_from_df_returns_data():

    df = pd.DataFrame({
        "symbol" : ["AAPL", "MSFT"],
        "price" : [200.2, 300.1],
        "prev_price": [198.0, 295.1]
    })

    result = get_price_from_df(df, "MSFT")

    assert result is not None
    assert result["price"] == 300.1
    assert result["prev_price"] == 295.1
"""
#legacy learning tests for testing a dataframe helper logic

########API testing


app.state.prices_df = pd.DataFrame({
        "symbol" : ["AAPL", "MSFT"],
        "price" : [189.2, 353.2],
        "prev_price" : [182.7, 345.25],
    })


##test valid symbol
def test_get_price_success():
    
    response = client.get("/prices/AAPL")

    assert response.status_code == 200
    data = response.json()

    assert data["symbol"] == "AAPL"
    assert "price" in data

def test_get_price_invalid_format():

    response = client.get("/prices/123")

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid symbol format"

##test invalid symbol
def test_get_price_not_found():

    response = client.get("/prices/INVALID")

    assert response.status_code == 404
    assert response.json()["detail"] == "Symbol not found"


def test_get_top_movers():

    response = client.get("/top-movers")

    data = response.json() #taking json as input and parsing it to produce a js object which is a list on the next line.

    assert isinstance(data, list)
    assert len(data) > 0

    item = data[0]

    assert "symbol" in item
    assert "change_pct" in item

def test_get_price_stats():

    response = client.get("/stats")

    assert response.status_code == 200

    data = response.json() #destructure into a json

    assert "total_rows" in data
    assert "average_price" in data



