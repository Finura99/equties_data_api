from src.main import get_prices_from_df
import pandas as pd
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent ##root directory
PRICES_PATH = BASE_DIR / "data" / "prices.csv"

def test_get_prices_from_df_returns_aapl():

    df = pd.read_csv(PRICES_PATH) #load csv

    result = get_prices_from_df(df, "AAPL") #test function here

    assert result is not None #expect result not to be none
    assert result["symbol"] == "AAPL"
    assert "price" in result
    assert "prev_price" in result

    ##symbol does not exist test below

def test_get_prices_from_df_returns_none():

    df = pd.DataFrame({
        "symbol" : ["AAPL", "MSFT"],
        "price" : [200.2, 300.1],
        "prev_price" : [198.0, 295.1],
    })

    result = get_prices_from_df(df, "GOOGL")

    assert result is None

def test_get_prices_from_df_returns_data():

    df = pd.DataFrame({
        "symbol" : ["AAPL", "MSFT"],
        "price" : [200.2, 300.1],
        "prev_price": [198.0, 295.1]
    })

    result = get_prices_from_df(df, "MSFT")

    assert result is not None
    assert result["price"] == 300.1
    assert result["prev_price"] == 295.1
    

