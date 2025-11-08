# app/services/meal_library_deletion.py
import os
import sqlite3


def _get_db_path():
    """Helper to get the absolute path to the main meal library database."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(base_dir, "meal-library", "meal_library.db")


def delete_meal_by_name_and_location(name, location):
    """Deletes a specific meal from the meal library database."""
    try:
        db_path = _get_db_path()

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM meals WHERE name = ? AND location = ?", (name, location)
        )
        conn.commit()

        deleted_count = cursor.rowcount
        conn.close()

        if deleted_count == 0:
            return {"error": "Meal not found."}
        return {"message": f"Meal '{name}' at {location} deleted successfully!"}

    except Exception as e:
        return {"error": str(e)}
