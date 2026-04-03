import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "prices.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()



cursor.execute("""
CREATE TABLE IF NOT EXISTS prices (
    symbol TEXT,
    price REAL,
    prev_price REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS companies (
    symbol TEXT,
    company_name TEXT,
    sector TEXT    
)
""")


cursor.execute("DELETE FROM prices")
cursor.execute("DELETE FROM companies")

cursor.execute("INSERT INTO prices VALUES (?, ?, ?)", ("AAPL", 200.2, 198.0))
cursor.execute("INSERT INTO prices VALUES (?, ?, ?)", ("MSFT", 300.1, 295.1))
cursor.execute("INSERT INTO prices VALUES (?, ?, ?)", ("TSLA", 203.2, 199.9))

cursor.execute("INSERT INTO companies VALUES (?, ?, ?)", ("AAPL", "Apple", "Technology"))
cursor.execute("INSERT INTO companies VALUES (?, ?, ?)", ("MSFT", "Microsoft", "Technology"))
cursor.execute("INSERT INTO companies VALUES (?, ?, ?)", ("TSLA", "Tesla", "Automative"))



print("Database seeded successfully.")

#1. Check compaies table
cursor.execute("SELECT * FROM companies")
rows = cursor.fetchall()

print("COMPANIES:")
for row in rows:
    print(row)


cursor.execute("""
    SELECT prices.symbol, prices.price, companies.company_name, companies.sector
    FROM prices
    JOIN companies
    ON prices.symbol = companies.symbol
    
""")

join_rows = cursor.fetchall()

print("\nJOIN RESULT:")
for row in join_rows:
    print(row)

conn.commit()
conn.close()







