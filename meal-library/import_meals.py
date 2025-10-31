# meal-library/import_meals.py
import csv
import sqlite3
import os

def import_meals():
    db_path = os.path.join(os.path.dirname(__file__), 'meal_library.db')
    csv_path = os.path.join(os.path.dirname(__file__), 'meals.csv')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Normalize (strip whitespace and make consistent case)
            name = row['name'].strip()
            location = row['location'].strip()
            calories = row['calories']
            carbs = row['carbohydrates']
            fat = row['fat']
            protein = row['protein']

            # Check for an existing meal (case-insensitive match)
            cursor.execute("""
                SELECT id FROM meals
                WHERE LOWER(TRIM(name)) = LOWER(?) AND LOWER(TRIM(location)) = LOWER(?)
            """, (name, location))
            existing = cursor.fetchone()

            if existing:
                cursor.execute("""
                    UPDATE meals
                    SET calories = ?, carbohydrates = ?, fat = ?, protein = ?
                    WHERE id = ?
                """, (calories, carbs, fat, protein, existing[0]))
                print(f"Updated: {name} ({location})")
            else:
                cursor.execute("""
                    INSERT INTO meals (name, calories, carbohydrates, fat, protein, location)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (name, calories, carbs, fat, protein, location))
                print(f"Added: {name} ({location})")

    conn.commit()
    conn.close()
    print("\nImport complete!")

if __name__ == "__main__":
    import_meals()
