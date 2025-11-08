# app/services/meal_library_addition.py
import os
import sqlite3


def _get_db_path():
    """Helper to get the absolute path to the main meal library database."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(base_dir, "meal-library", "meal_library.db")


def add_single_meal(data):
    """Adds a single meal entry into the meal library database."""
    try:
        required = ["name", "protein", "carbohydrates", "fat", "meal_type", "location"]
        missing = [f for f in required if f not in data]
        if missing:
            return {"error": f"Missing required fields: {', '.join(missing)}"}

        # Recalculate calories from macros
        calories = (
            (float(data["protein"]) * 4)
            + (float(data["carbohydrates"]) * 4)
            + (float(data["fat"]) * 9)
        )

        db_path = _get_db_path()

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO meals
            (name, calories, carbohydrates, fat, protein, meal_type, location)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                data["name"].strip(),
                round(calories, 1),
                float(data["carbohydrates"]),
                float(data["fat"]),
                float(data["protein"]),
                data["meal_type"].strip(),
                data["location"].strip(),
            ),
        )

        conn.commit()
        conn.close()

        return {"message": f"Meal '{data['name']}' added successfully!"}

    except Exception as e:
        return {"error": str(e)}
