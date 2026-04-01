import sqlite3
from pathlib import Path
from src.services import get_price_from_db

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