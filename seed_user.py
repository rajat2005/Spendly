import sqlite3
import random
from datetime import datetime
from werkzeug.security import generate_password_hash

DATABASE = 'spendly.db'

# Common Indian first names (mixed gender)
FIRST_NAMES = [
    'Aarav', 'Vivaan', 'Aditya', 'Vihaan', 'Arjun', 'Reyansh', 'Ayan', 'Krishna',
    'Ishaan', 'Shaurya', 'Pranav', 'Rohan', 'Aryan', 'Karan', 'Rahul', 'Vikram',
    'Priya', 'Ananya', 'Diya', 'Saanvi', 'Aadhya', 'Pari', 'Meera', 'Kavya',
    'Riya', 'Neha', 'Sneha', 'Anjali', 'Divya', 'Pooja', 'Shruti', 'Nisha'
]

# Common Indian surnames across regions
LAST_NAMES = [
    'Sharma', 'Verma', 'Gupta', 'Agarwal', 'Singh', 'Kumar', 'Patel', 'Desai',
    'Reddy', 'Rao', 'Nair', 'Menon', 'Iyer', 'Iyengar', 'Chatterjee', 'Banerjee',
    'Mukherjee', 'Ganguly', 'Das', 'Bose', 'Shah', 'Jain', 'Mehta', 'Kapoor',
    'Malhotra', 'Khanna', 'Sethi', 'Bhat', 'Hegde', 'Kamath'
]

def get_db():
    """Returns a SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def email_from_name(first, last, num):
    """Generate email from name with random number suffix."""
    return f"{first.lower()}.{last.lower()}{num}@gmail.com"

def generate_unique_user():
    """Generate a unique Indian user that doesn't exist in DB."""
    conn = get_db()
    cursor = conn.cursor()

    max_attempts = 50
    for _ in range(max_attempts):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        num_suffix = random.randint(10, 999)
        email = email_from_name(first_name, last_name, num_suffix)

        # Check if email exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone() is None:
            conn.close()
            return first_name, last_name, email

    conn.close()
    raise Exception("Could not generate unique email after multiple attempts")

def seed_user():
    """Generate and insert a random Indian user into the database."""
    first_name, last_name, email = generate_unique_user()
    full_name = f"{first_name} {last_name}"
    password_hash = generate_password_hash("password123")
    created_at = datetime.now().isoformat()

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO users (name, email, password_hash, created_at)
        VALUES (?, ?, ?, ?)
    ''', (full_name, email, password_hash, created_at))

    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    print(f"User created successfully!")
    print(f"  id: {user_id}")
    print(f"  name: {full_name}")
    print(f"  email: {email}")

if __name__ == '__main__':
    seed_user()
