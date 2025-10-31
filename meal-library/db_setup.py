# meal-library/db_setup.py
import sqlite3
import os

def initialize_db():
    # Use an absolute path so it works inside Docker too
    db_path = os.path.join(os.path.dirname(__file__), 'meal_library.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop the table if it exists (optional — good for testing)
    cursor.execute("DROP TABLE IF EXISTS meals")

    # Create the meals table
    cursor.execute("""
        CREATE TABLE meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            calories INTEGER,
            carbohydrates INTEGER,
            fat INTEGER,
            protein INTEGER,
            location TEXT
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized at: {db_path}")

if __name__ == "__main__":
    initialize_db()
