import sqlite3
import random
from datetime import datetime, timedelta
from database.db import get_db, DATABASE

# Category configurations with Indian context
CATEGORIES = {
    'Food': {'min': 50, 'max': 800, 'weight': 25, 'descriptions': [
        'Lunch at local restaurant', 'Street food chaat', 'Groceries from market',
        'Dinner at family cafe', 'Morning breakfast', 'Office tiffin',
        'Weekend biryani order', 'South Indian thali', 'Chinese takeaway', 'Pizza delivery'
    ]},
    'Transport': {'min': 20, 'max': 500, 'weight': 15, 'descriptions': [
        'Auto rickshaw fare', 'Metro card recharge', 'Uber to airport',
        'Bus pass monthly', 'Petrol refill', 'Taxi to railway station',
        'Ola ride home', 'Bike service', 'Train ticket', 'Parking fee'
    ]},
    'Bills': {'min': 200, 'max': 3000, 'weight': 15, 'descriptions': [
        'Electricity bill', 'Mobile recharge', 'Internet broadband',
        'Water bill', 'Cooking gas cylinder', 'House maintenance',
        'Society charges', 'Cable TV subscription', 'Security fee', 'Property tax'
    ]},
    'Health': {'min': 100, 'max': 2000, 'weight': 8, 'descriptions': [
        'Doctor consultation', 'Medicine from pharmacy', 'Dental checkup',
        'Eye test glasses', 'Gym membership', 'Health supplements',
        'Physiotherapy session', 'Blood test lab', 'Yoga class', 'Massage therapy'
    ]},
    'Entertainment': {'min': 100, 'max': 1500, 'weight': 10, 'descriptions': [
        'Movie tickets', 'Netflix subscription', 'Concert entry',
        'Amusement park', 'Gaming zone', 'Cricket match tickets',
        'Comedy show', 'Museum visit', 'Boat ride', 'Theme park'
    ]},
    'Shopping': {'min': 200, 'max': 5000, 'weight': 17, 'descriptions': [
        'New kurta set', 'Festival clothes', 'Shoes from showroom',
        'Mobile phone case', 'Birthday gift', 'Jewelry purchase',
        'Handbag', 'Watch accessory', 'Home decor', 'Kitchen utensils'
    ]},
    'Other': {'min': 50, 'max': 1000, 'weight': 10, 'descriptions': [
        'Gift for relative', 'Donation to temple', 'Pet supplies',
        'Book purchase', 'Stationery', 'Flowers for puja',
        'Car wash', 'Tailoring charges', 'Photocopy print', 'Small repair'
    ]}
}

def parse_args(args):
    """Parse command line arguments."""
    if len(args) != 3:
        return None
    try:
        return {
            'user_id': int(args[0]),
            'count': int(args[1]),
            'months': int(args[2])
        }
    except ValueError:
        return None

def verify_user(user_id):
    """Check if user exists in database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_weighted_category():
    """Select a category based on weights (proportional distribution)."""
    categories = list(CATEGORIES.keys())
    weights = [CATEGORIES[cat]['weight'] for cat in categories]
    return random.choices(categories, weights=weights, k=1)[0]

def generate_expense(user_id, start_date, end_date):
    """Generate a single random expense."""
    category = get_weighted_category()
    cat_config = CATEGORIES[category]

    amount = round(random.uniform(cat_config['min'], cat_config['max']), 2)
    description = random.choice(cat_config['descriptions'])

    # Random date within range
    days_range = (end_date - start_date).days
    random_days = random.randint(0, max(0, days_range))
    expense_date = start_date + timedelta(days=random_days)

    return (user_id, amount, category, expense_date.strftime('%Y-%m-%d'), description)

def seed_expenses(user_id, count, months):
    """Generate and insert expenses for a user."""
    # Verify user exists
    user = verify_user(user_id)
    if not user:
        print(f"No user found with id {user_id}.")
        return

    print(f"Creating {count} expenses for {user['name']} (ID: {user_id})")
    print(f"Spreading across past {months} month(s)...\n")

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)

    # Generate all expenses
    expenses = [generate_expense(user_id, start_date, end_date) for _ in range(count)]

    # Insert in single transaction
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat()

    try:
        cursor.executemany('''
            INSERT INTO expenses (user_id, amount, category, date, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', [(exp[0], exp[1], exp[2], exp[3], exp[4], now) for exp in expenses])

        conn.commit()

        # Get inserted expenses for confirmation
        cursor.execute('''
            SELECT id, amount, category, date, description
            FROM expenses
            WHERE user_id = ?
            ORDER BY date DESC
            LIMIT 5
        ''', (user_id,))
        samples = cursor.fetchall()

        # Get date range of inserted expenses
        cursor.execute('''
            SELECT MIN(date), MAX(date) FROM expenses WHERE user_id = ?
        ''', (user_id,))
        date_range = cursor.fetchone()

        conn.close()

        # Print confirmation
        print(f"Successfully inserted {count} expenses!")
        print(f"Date range: {date_range[0]} to {date_range[1]}")
        print(f"\nSample of 5 inserted records:")
        print("-" * 80)
        for s in samples:
            print(f"  ID: {s[0]} | Rs. {s[1]:>7.2f} | {s[2]:<12} | {s[3]} | {s[4]}")
        print("-" * 80)

    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error inserting expenses: {e}")
        raise

if __name__ == '__main__':
    import sys
    args = sys.argv[1:]

    parsed = parse_args(args)
    if not parsed:
        print("Usage: /seed-expenses <user_id> <count> <months>")
        print("Example: /seed-expenses 1 50 6")
        sys.exit(1)

    seed_expenses(parsed['user_id'], parsed['count'], parsed['months'])
