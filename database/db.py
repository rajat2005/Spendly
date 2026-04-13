import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = 'spendly.db'


def get_db():
    """Returns a SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    """Creates all tables using CREATE TABLE IF NOT EXISTS."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()


def seed_db():
    """Inserts sample data for development (idempotent)."""
    conn = get_db()
    cursor = conn.cursor()

    # Check if data already exists
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Create demo user
    from datetime import datetime
    password_hash = generate_password_hash('demo123')
    now = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO users (name, email, password_hash, created_at)
        VALUES (?, ?, ?, ?)
    ''', ('Demo User', 'demo@spendly.com', password_hash, now))

    user_id = cursor.lastrowid

    # 8 sample expenses across categories
    expenses = [
        (150.50, 'Food', '2026-04-01', 'Lunch at office cafe'),
        (45.00, 'Transport', '2026-04-02', 'Uber ride to airport'),
        (2500.00, 'Bills', '2026-04-03', 'Electricity bill'),
        (899.00, 'Health', '2026-04-05', 'Doctor consultation'),
        (350.00, 'Entertainment', '2026-04-06', 'Movie tickets and dinner'),
        (1200.00, 'Shopping', '2026-04-08', 'New shoes'),
        (75.00, 'Food', '2026-04-10', 'Grocery shopping'),
        (500.00, 'Other', '2026-04-12', 'Gift for friend'),
    ]

    cursor.executemany('''
        INSERT INTO expenses (user_id, amount, category, date, description, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', [(user_id, *exp, now) for exp in expenses])

    conn.commit()
    conn.close()
