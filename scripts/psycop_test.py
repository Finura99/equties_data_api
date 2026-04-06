import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="equities",
    user="admin",
    password="admin",
    port=5432,
)

print("Connected!")

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        symbol TEXT PRIMARY KEY,
        price REAL,
        prev_price REAL
)
""")

cursor.execute("""
    INSERT INTO PRICES (symbol, price, prev_price)
    VALUES 
        ('AAPL', 200.2, 198.0),
        ('MSFT', 300.1, 295.1),
        ('TSLA', 400.2, 200.2)
    ON CONFLICT (symbol) DO NOTHING
""")
conn.commit()

cursor.execute("SELECT * FROM prices")
rows = cursor.fetchall() # returns a list of tuples back from 

cursor.close()
conn.close()

# this is the network conencted to the postgres docker container 