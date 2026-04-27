import sqlite3
import os

# Path to the SQLite database file
DB_PATH = "data/expenses.db"

def connect_db():
    """
    Establishes a connection to the SQLite database.
    Creates the 'data' directory if it doesn't exist.
    
    Returns:
        sqlite3.Connection: A connection object to the database.
    """
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def create_table():
    """
    Creates the 'expenses' table in the database if it does not already exist.
    The table stores transaction details including amount, category, description, and date.
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Execute SQL to create the table structure
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
    """
    Inserts a new expense record into the database.
    
    Args:
        amount (float): The cost of the expense.
        category (str): The classification of the expense (e.g., Food, Travel).
        description (str): A brief note about the expense.
        date (str): The date of the expense in YYYY-MM-DD format.
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Insert data into the expenses table
    cursor.execute("""
        INSERT INTO expenses
        (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    """, (amount, category, description, date))

    conn.commit()
    conn.close()

def fetch_expenses():
    """
    Retrieves all expense records from the database.
    
    Returns:
        list: A list of tuples, where each tuple represents an expense record.
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch all records from the expenses table
    cursor.execute("SELECT * FROM expenses")
    data = cursor.fetchall()

    conn.close()

    return data

def delete_expense(expense_id):
    """
    Deletes a specific expense record from the database using its unique ID.
    
    Args:
        expense_id (int): The ID of the record to delete.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

    conn.commit()
    conn.close()

def clear_all_expenses():
    """
    Deletes all records from the expenses table.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses")

    conn.commit()
    conn.close()