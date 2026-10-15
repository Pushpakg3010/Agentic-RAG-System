
import sqlite3

conn = sqlite3.connect("data/order.db")
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cur.fetchall())

try:
    cur.execute("SELECT * FROM orders;")
    print("Orders:", cur.fetchall())
except Exception as e:
    print("Error:", e)

conn.close()