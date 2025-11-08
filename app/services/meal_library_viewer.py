# app/services/meal_library_viewer.py
import os
import sqlite3


def _get_db_path():
    """Helper to get the absolute path to the main meal library database."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(base_dir, "meal-library", "meal_library.db")


def view_all_meals():
    """Retrieves all meals from the meal library database."""
    try:
        db_path = _get_db_path()
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT name, calories, carbohydrates, fat, protein, meal_type, location
            FROM meals
            ORDER BY location, meal_type, name
        """
        )

        meals = cursor.fetchall()
        conn.close()

        return meals, None

    except Exception as e:
        return None, str(e)


def get_meal_names_and_locations():
    """Retrieves meal names and locations for dropdown menus (like delete-meal)."""
    try:
        db_path = _get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name, location FROM meals ORDER BY location, name")
        meals = cursor.fetchall()
        conn.close()

        return meals, None

    except Exception as e:
        return None, str(e)
