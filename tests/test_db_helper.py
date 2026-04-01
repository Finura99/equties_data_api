import sqlite3
from pathlib import Path

# Get absolute path to DB
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "prices.db"


def get_price_from_db(symbol: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT symbol, price, prev_price FROM prices WHERE symbol = ?",
        (symbol,) ##heart of evaluating whether the clients request matches the data in the database...
    )

    row = cursor.fetchone()
    conn.close() ##end of sql session with python

    if row is None:
        return None

    return {
        "symbol": row[0],
        "price": row[1],
        "prev_price": row[2],
    } #structure it into a dict as sql query returns it as a tuple like structure 


# Quick test runs
print(get_price_from_db("AAPL"))
print(get_price_from_db("MSFT"))
print(get_price_from_db("GOOGL"))