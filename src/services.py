from fastapi import HTTPException
from pathlib import Path

import sqlite3
import psycopg2
from psycopg2 import IntegrityError
###logic layer / validation and database

def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()

    if not symbol.isalpha(): # if not alphabet then return 400 - incorrect format...
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


def get_top_movers_from_db(limit: int, offset: int) -> list:
    conn = sqlite3.connect(DB_PATH) #connect to database
    cursor = conn.cursor() # initialise tools 

    cursor.execute(
        """
        SELECT 
            symbol,
            price,
            prev_price,
            (price - prev_price) / prev_price * 100 AS change_pct
        FROM prices
        WHERE prev_price > 0
        ORDER BY change_pct DESC
        LIMIT ? OFFSET ?;
        """,
        (limit, offset)
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

def get_price_stats_from_db() -> dict:
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor = cursor.execute(
        """
        SELECT COUNT(*) FROM prices
        """
        )
    total_rows = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT AVG(price) FROM prices
        """
        )
    average_price = cursor.fetchone()[0] # the zero indicates unwrapping of the tuple sql returns

    conn.close()

    return {
        "total_rows" : total_rows,
        "average_price" : average_price,
    }

def get_price_with_company_from_db(symbol: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            prices.symbol,
            prices.price,
            companies.company_name,
            companies.sector
        FROM prices
        JOIN companies
        ON prices.symbol = companies.symbol
        WHERE prices.symbol = ?
        """, (symbol,)
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None
    
    return {
        "symbol" : row[0],
        "price" : row[1],
        "prev_price" : row[2],
        "company_name" : row[3],
        "sector" : row[4],
    }

def get_price_from_postgres(symbol:str):
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="admin",
        password="admin",
        database="equities",
    )

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM prices WHERE symbol = %s
        """,(symbol,))
    
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None
    
    return {
        "symbol": row[0],
        "price" : row[1],
        "prev_price": row[2],
    }

def create_price_in_postgres(symbol:str, price:float, prev_price:float):
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="admin",
        password="admin",
        database="equities",
    )

    cursor = conn.cursor()


    try:
        cursor.execute(
            """
            INSERT INTO prices (symbol, price, prev_price)
            VALUES (%s, %s, %s)
            RETURNING symbol, price, prev_price
            """, (symbol, price, prev_price)
            )
    
        row = cursor.fetchone()
        conn.commit()
        conn.close()

        return {
            "symbol" : row[0],
            "price" : row[1],
            "prev_price": row[2],
    }

    except IntegrityError:
        conn.rollback() #if insert fails , it resets transaction
        raise HTTPException(status_code=409, detail="Symbol already exists")
    
    finally:
        cursor.close()
        conn.close()