import sqlite3
from pathlib import Path
from src.services import get_price_from_db

# Get absolute path to DB
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "prices.db"


def test_get_price_from_db():
    
    result = get_price_from_db("MSFT")

    assert result is not None