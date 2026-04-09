import sqlite3
from pathlib import Path
from src.services import get_price_from_db, get_top_movers_from_db, get_price_stats_from_db

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "prices.db"



def test_get_price_from_db_returns_data():
    result = get_price_from_db("AAPL")

    assert result is not None
    assert result["symbol"] == "AAPL"
    assert "price" in result
    assert "prev_price" in result


def test_get_price_from_db_returns_none():
    result = get_price_from_db("GOOGL")

    assert result is None

def test_get_top_movers_from_db():
    result = get_top_movers_from_db(1,0)

    assert isinstance(result, list)
    assert len(result) == 1
    
    item = result[0] #accessing the 1st row of our key from the service layer fucntion.

    assert "symbol" in item
    assert "change_pct" in item

def test_get_price_stats_from_db():
    result = get_price_stats_from_db()

    assert result is not None
    assert "total_rows" in result
    assert "average_price" in result