# app/routes.py
"""Perform Backend Routing for Flask Server"""

from flask import render_template, jsonify, request
from werkzeug.utils import secure_filename
import os
import sqlite3
import csv

# Service imports
from app.services.meal_planner import generate_full_meal_plan
from app.services.meal_library_upload import replace_meal_library_from_csv
from app.services.meal_library_viewer import view_all_meals
from app.services.meal_library_viewer import get_meal_names_and_locations
from app.services.meal_library_addition import add_single_meal
from app.services.meal_library_deletion import delete_meal_by_name_and_location

# Config
ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename):
    """Validates file extension *.csv for the upload meal.csv."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def init_app(app):
    """Registers all routes for the UFUEL Flask application."""

    # Home & Generator

    @app.route("/")
    def index():
        """Renders the home page."""
        return render_template("index.html")

    @app.route("/generator")
    def generator():
        """Renders the meal plan generator page."""
        return render_template("generator.html")

    @app.route("/generate-plan", methods=["POST"])
    def generate_plan():
        """Generates a personalized meal plan based on user input."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No input received"}), 400

            result = generate_full_meal_plan(data)
            return jsonify(result), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Meal Library CRUD

    # (Create) Meal Library Upload

    @app.route("/upload")
    def upload_page():
        """Renders the upload page for meal library CSV."""
        return render_template("upload.html")

    @app.route("/upload-meal-library", methods=["POST"])
    def upload_meal_library():
        """Uploads and replace the meal library CSV."""
        try:
            if "file" not in request.files:
                return jsonify({"error": "No file part in request"}), 400

            file = request.files["file"]
            if file.filename == "":
                return jsonify({"error": "No file selected"}), 400

            if not allowed_file(file.filename):
                return jsonify({"error": "Invalid file type. Only CSV allowed."}), 400

            result = replace_meal_library_from_csv(file)
            status = 200 if "message" in result else 500
            return jsonify(result), status

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # (Read) Meal Library Viewer

    @app.route("/view-meals")
    def view_meals():
        """Displays the full meal database in an HTML table."""
        try:
            meals, error = view_all_meals()
            if error:
                return f"<h2>Error loading meals: {error}</h2>", 500
            return render_template("view-meals.html", meals=meals)

        except Exception as e:
            return f"<h2>Error loading meals: {str(e)}</h2>", 500

    # (Update) Meal Library Addition

    @app.route("/add-meal", methods=["POST"])
    def add_meal():
        """Adds a single meal to the database."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No JSON payload received"}), 400

            result = add_single_meal(data)
            status = 200 if "message" in result else 400
            return jsonify(result), status

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # (Delete) Meal Library Deletion

    @app.route("/delete-meal", methods=["GET", "POST"])
    def delete_meal():
        """Deletes a meal from the database and refresh the list."""
        message = None
        try:
            if request.method == "POST":
                meal_value = request.form.get("meal")
                if meal_value:
                    # Each meal option in the dropdown is formatted as "name|location"

                    if "|" not in meal_value:
                        return jsonify({"error": "Invalid meal format"}), 400
                    # Split the value into its components
                    name, location = meal_value.split("|")
                    # Call deletion service
                    result = delete_meal_by_name_and_location(name, location)
                    message = result.get("message") or result.get("error")

                else:
                    message = "No meal selected."
            # Reload meal list so drop down is up to date after deletion.
            meals, error = get_meal_names_and_locations()

            if error:
                return f"<h2>Error loading meals: {error}</h2>", 500

            # Render delete meal page with the updated list and message
            return render_template("delete-meal.html", meals=meals, message=message)

        except Exception as e:
            return f"<h2>Error deleting meal: {str(e)}</h2>", 500


"""
HTTP Status Code Reference
--------------------------
Code | Category       | Meaning                       | When to Use
-----|----------------|-------------------------------|------------------------------
200  | Success        | Request succeeded             | Normal successful responses
201  | Created        | Resource successfully created | POST request that adds new data
400  | Client Error   | Bad request or invalid input  | Validation or missing field errors
401  | Unauthorized   | Authentication required       | User not logged in or no token
403  | Forbidden      | Access denied                 | User lacks permission
404  | Not Found      | Resource not found            | Invalid URL or missing record
409  | Conflict       | Data conflict                 | Duplicate entry or constraint conflict
500  | Server Error   | Internal server error         | Unexpected backend failure or exception
<<<<<<< HEAD
"""
=======
"""
>>>>>>> main
