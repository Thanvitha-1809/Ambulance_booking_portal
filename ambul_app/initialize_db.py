# initialize_db.py
import sqlite3

# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect('ambulance.db')
cursor = conn.cursor()

# Create patients and drivers tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    pickup_location TEXT,
    drop_location TEXT,
    cost INTEGER,
    driver_id INTEGER,
    condition TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS drivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    contact TEXT,
    total_trips INTEGER DEFAULT 0,
    total_earnings INTEGER DEFAULT 0
)
''')

# Add a sample driver
cursor.execute('''
INSERT INTO drivers (name, contact) VALUES ('John Doe', '123-456-7890')
''')

# Commit and close connection
conn.commit()
conn.close()

print("Database initialized with sample data.")
