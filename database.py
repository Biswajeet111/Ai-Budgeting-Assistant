import sqlite3
import os

DB_PATH = "data/expenses.db"

def connect_db():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def create_table():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            description TEXT,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()

def add_expense(amount, category, description, date):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    """, (amount, category, description, date))

    conn.commit()
    conn.close()

def fetch_expenses():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")

    data = cursor.fetchall()

    conn.close()

    return data