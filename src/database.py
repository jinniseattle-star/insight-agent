import sqlite3
import pandas as pd

def init_mock_db():
    """Initializes a local SQLite database representing an e-commerce platform."""
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    
    # Create Tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        plan_type TEXT,
        signup_date TEXT
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        amount REAL,
        order_date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")
    
    # Populate Mock Data
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM orders")
    
    users = [
        (1, 'Alice Smith', 'Premium', '2025-01-15'),
        (2, 'Bob Jones', 'Free', '2025-02-20'),
        (3, 'Charlie Brown', 'Premium', '2025-03-05'),
        (4, 'Diana Prince', 'Premium', '2025-03-22')
    ]
    orders = [
        (101, 1, 150.00, '2025-04-01'),
        (102, 1, 200.00, '2025-05-10'),
        (103, 2, 15.50, '2025-04-15'),
        (104, 3, 300.00, '2025-05-12'),
        (105, 4, 125.75, '2025-05-19'),
        (106, 1, 95.00, '2025-05-22')
    ]
    
    cursor.executemany("INSERT INTO users VALUES (?,?,?,?)", users)
    cursor.executemany("INSERT INTO orders VALUES (?,?,?,?)", orders)
    conn.commit()
    conn.close()

def run_read_only_query(sql_query: str) -> pd.DataFrame:
    """Executes SQL queries strictly ensuring safety constraints."""
    forbidden_keywords = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "GRANT"]
    if any(keyword in sql_query.upper() for keyword in forbidden_keywords):
        raise ValueError("Security Violation: Destructive or mutating operations are strictly forbidden.")
    
    conn = sqlite3.connect("ecommerce.db")
    try:
        df = pd.read_sql_query(sql_query, conn)
        return df
    finally:
        conn.close()

def get_schema_string() -> str:
    """Returns a string representation of the schema for the LLM's context."""
    return """
    Table: users
    - user_id (INTEGER, PRIMARY KEY)
    - name (TEXT)
    - plan_type (TEXT, values: 'Premium', 'Free')
    - signup_date (TEXT, YYYY-MM-DD)
    
    Table: orders
    - order_id (INTEGER, PRIMARY KEY)
    - user_id (INTEGER, FOREIGN KEY references users.user_id)
    - amount (REAL)
    - order_date (TEXT, YYYY-MM-DD)
    """

if __name__ == "__main__":
    init_mock_db()
    print("Database successfully initialized!")
