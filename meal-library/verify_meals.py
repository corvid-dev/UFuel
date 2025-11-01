# meal-library/verify_meals.py
import sqlite3
import os
from tabulate import tabulate

def verify_meals():
    db_path = os.path.join(os.path.dirname(__file__), 'meal_library.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='meals';
    """)
    if not cursor.fetchone():
        print("The 'meals' table does not exist. Did you run db_setup.py?")
        conn.close()
        return

    # Retrieve all meal data (including meal_type)
    cursor.execute("""
        SELECT name, location, meal_type, calories, carbohydrates, fat, protein
        FROM meals
        ORDER BY location, meal_type, name;
    """)
    rows = cursor.fetchall()

    if not rows:
        print("No meals found in the database.")
    else:
        headers = ["Name", "Location", "Meal Type", "Calories", "Carbs", "Fat", "Protein"]
        print(tabulate(rows, headers=headers, tablefmt="pretty"))

    conn.close()

if __name__ == "__main__":
    verify_meals()