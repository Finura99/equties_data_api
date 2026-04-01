import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "price.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS prices (
    symbol TEXT,
    price REAL,
    prev_price REAL
)
""")

cursor.execute("DELETE FROM prices")

cursor.execute("INSERT INTO prices VALUES (?, ?, ?)", ("AAPL", 200.2, 198.0))
cursor.execute("INSERT INTO prices VALUES (?, ?, ?)", ("MSFT", 300.1, 295.1))

conn.commit()
conn.close()

print("Database seeded successfully.")