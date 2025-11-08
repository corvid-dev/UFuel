# app/services/meal_library_upload.py
import os
import csv
import sqlite3
from werkzeug.utils import secure_filename


def _get_db_path():
    """Helper to get the absolute path to the main meal library database."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(base_dir, "meal-library", "meal_library.db")


def replace_meal_library_from_csv(uploaded_file):
    """Replaces the existing meal library with a new uploaded CSV."""

    try:
        # Step 1: Save uploaded CSV file
        upload_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
        )
        os.makedirs(upload_dir, exist_ok=True)

        filename = secure_filename(uploaded_file.filename)
        filepath = os.path.join(upload_dir, filename)
        uploaded_file.save(filepath)

        # Step 2: Get absolute DB path
        db_path = _get_db_path()

        # Create database and table if missing
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                calories REAL,
                carbohydrates REAL,
                fat REAL,
                protein REAL,
                meal_type TEXT,
                location TEXT
            )
        """
        )
        conn.commit()

        # Step 3: Clear existing rows
        cursor.execute("DELETE FROM meals")
        conn.commit()

        # Step 4: Import new CSV data
        with open(filepath, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                try:
                    carbs = float(row.get("carbohydrates", 0))
                    fat = float(row.get("fat", 0))
                    protein = float(row.get("protein", 0))
                    calories = round((carbs * 4) + (protein * 4) + (fat * 9), 1)
                except (ValueError, TypeError):
                    continue  # Skip malformed rows

                cursor.execute(
                    """
                    INSERT INTO meals (name, calories, carbohydrates, fat, protein, meal_type, location)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        row["name"].strip(),
                        calories,
                        carbs,
                        fat,
                        protein,
                        row["meal_type"].strip(),
                        row.get("location", "Any").strip(),
                    ),
                )
                count += 1

        conn.commit()
        conn.close()

        return {
            "message": f"Meal library uploaded successfully. Existing library replaced with {count} meals."
        }

    except Exception as e:
        return {"error": str(e)}
