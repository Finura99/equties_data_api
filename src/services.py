from fastapi import HTTPException
from pathlib import Path
import sqlite3

###logic layer / validation and database 

def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()

    if not symbol.isalpha():
        raise HTTPException(status_code = 400, detail = "Invalid symbol format")
    
    return symbol


# Get path to DB
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "prices.db"


def get_price_from_db(symbol: str) -> dict:
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


def get_top_movers_from_db(limit: int) -> list:
    conn = sqlite3.connect(DB_PATH) #connect to database
    cursor = conn.cursor() # initialise tools 

    cursor.execute(
        """
        SELECT 
            symbol,
            price,
            prev_price,
            ((price - prev_price) / prev_price) * 100 AS change_pct
        FROM prices 
        WHERE prev_price > 0
        ORDER BY change_pct DESC 
        LIMIT ?
        """,  
        (limit,)
        ) # run query
    
    rows = cursor.fetchall() #fetch results
    conn.close() 

    result = [] #our cupboard

    for row in rows:
        result.append({
            "symbol": row[0],
            "price": row[1],
            "prev_price": row[2],
            "change_pct" : row[3],
        }) # add in the rows in our cupboard
    
    return result
