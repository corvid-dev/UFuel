# app/routes.py
from flask import render_template, jsonify, request
from app.services.nutrition import calories_required
from app.services.meal_generator import generate_meal_plan

def init_app(app):
    # Register all routes for the UFUEL Flask application.

    # Home Page
    @app.route('/')
    def index():
        return render_template('index.html')


    # Meal generator page
    @app.route('/generator')
    def generator():
        return render_template('generator.html')

    @app.route('/generate-plan', methods=['POST'])
    def generate_plan():
        """
        Generates a meal plan based on user demographics, goals,
        and potentially different locations for each meal.

        Expected JSON body:
        {
            "age": 25,
            "height_in": 70,
            "weight_lb": 165,
            "gender": "male",
            "activity_level": "moderate",
            "goal": "maintain",
            "breakfast_location": "Glen",
            "lunch_location": "Newell",
            "dinner_location": "West Village"
        }

        Response JSON:
        {
            "total_target_calories": 2700,
            "total_selected_calories": 2650,
            "match_percent": 98.1,
            "plan": {
                "breakfast": {
                    "target_fraction": 0.25,
                    "target_meal_period_calories": 675,
                    "total_meal_period_calories": 680,
                    "location": "Glen",
                    "meals": [...],
                    "drink": {...}
                },
                ...
            }
        }
        """
        try:
            # Parse input from frontend
            data = request.get_json()
            if not data:
                return jsonify({"error": "No input received"}), 400

            # Step 1: Calculate required daily calories
            required_calories = calories_required(
                age=data.get("age"),
                height_in=data.get("height_in"),
                weight_lb=data.get("weight_lb"),
                gender=data.get("gender"),
                activity_level=data.get("activity_level"),
                goal=data.get("goal")
            )

            # Step 2: Generate meal plan with per-meal locations
            plan = generate_meal_plan(
                total_calories=required_calories,
                breakfast_location=data.get("breakfast_location"),
                lunch_location=data.get("lunch_location"),
                dinner_location=data.get("dinner_location")
            )

            # Step 3: Return structured JSON response
            return jsonify({
                "target_daily_calories": required_calories,
                "meal_plan": plan
            }), 200

        except KeyError as e:
            return jsonify({"error": f"Missing required field: {e}"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @app.route('/upload')
    def upload_page():
        """Renders the upload page for meal library CSV."""
        return render_template('upload.html')

    # Add ability for upload a meal library .csv to the database.
    @app.route("/upload-meal-library", methods=["POST"])
    def upload_meal_library():
        """
        Upload a CSV file containing meal data and completely replace the existing meal library.
        The CSV should have columns:
        name,carbohydrates,fat,protein,meal_type,location
        Calories are auto-calculated as (carbs * 4) + (protein * 4) + (fat * 9).
        """
        import os, sqlite3, csv
        from werkzeug.utils import secure_filename

        if "file" not in request.files:
            return jsonify({"error": "No file part in request"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        if not file.filename.lower().endswith(".csv"):
            return jsonify({"error": "Invalid file type. Only CSV allowed."}), 400

        try:
            upload_dir = os.path.join(os.path.dirname(__file__), "..", "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_dir, filename)
            file.save(filepath)

            db_path = os.path.join(os.path.dirname(__file__), "..", "meal-library", "meal_library.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Step 1: Clear existing meals
            cursor.execute("DELETE FROM meals")
            conn.commit()

            # Step 2: Load new meals from CSV
            with open(filepath, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                count = 0
                for row in reader:
                    try:
                        carbs = float(row["carbohydrates"])
                        fat = float(row["fat"])
                        protein = float(row["protein"])
                        calories = round((carbs * 4) + (protein * 4) + (fat * 9), 1)
                    except (KeyError, ValueError):
                        continue  # skip malformed rows

                    cursor.execute("""
                        INSERT INTO meals (name, calories, carbohydrates, fat, protein, meal_type, location)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row["name"],
                        calories,
                        carbs,
                        fat,
                        protein,
                        row["meal_type"],
                        row.get("location", "Any")
                    ))
                    count += 1

            conn.commit()
            conn.close()

            return jsonify({"message": f"Meal library replaced with {count} meals (calories auto-calculated)."}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500




        
    # Add a single meal entry to database
    @app.route("/add-meal", methods=["POST"])
    def add_meal():
        """
        Add a single meal entry into the database.

        Expected JSON:
        {
            "name": "Grilled Chicken",
            "protein": 30,
            "carbohydrates": 5,
            "fat": 4,
            "calories": 176,
            "meal_type": "lunch",
            "location": "Glen"
        }
        """
        import os, sqlite3

        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No JSON payload received"}), 400

            required = ["name", "protein", "carbohydrates", "fat", "calories", "meal_type", "location"]
            missing = [f for f in required if f not in data]
            if missing:
                return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

            # Recalculate calories to ensure consistency
            calories = (float(data["protein"]) * 4) + (float(data["carbohydrates"]) * 4) + (float(data["fat"]) * 9)

            db_path = os.path.join(os.path.dirname(__file__), "..", "meal-library", "meal_library.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO meals
                (name, calories, carbohydrates, fat, protein, meal_type, location)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data["name"],
                round(calories, 1),
                float(data["carbohydrates"]),
                float(data["fat"]),
                float(data["protein"]),
                data["meal_type"],
                data["location"]
            ))

            conn.commit()
            conn.close()

            return jsonify({"message": f"Meal '{data['name']}' added successfully!"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/view-meals")
    def view_meals():
        """Display the full meal database in an HTML table."""
        import os, sqlite3

        try:
            db_path = os.path.join(os.path.dirname(__file__), "..", "meal-library", "meal_library.db")
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT name, calories, carbohydrates, fat, protein, meal_type, location
                FROM meals
                ORDER BY location, meal_type, name
            """)
            meals = cursor.fetchall()
            conn.close()

            return render_template("view-meals.html", meals=meals)

        except Exception as e:
            return f"<h2>Error loading meals: {e}</h2>", 500

    @app.route("/delete-meal", methods=["GET", "POST"])
    def delete_meal():
        import os, sqlite3

        db_path = os.path.join(os.path.dirname(__file__), "..", "meal-library", "meal_library.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        message = None

        if request.method == "POST":
            meal_value = request.form.get("meal")
            if meal_value:
                name, location = meal_value.split("|")
                cursor.execute("DELETE FROM meals WHERE name = ? AND location = ?", (name, location))
                conn.commit()
                message = "Meal deleted!"
            else:
                message = "No meal selected."

        # Always reload the (updated) meal list after any operation
        cursor.execute("SELECT name, location FROM meals ORDER BY location, name")
        meals = cursor.fetchall()
        conn.close()

        return render_template("delete-meal.html", meals=meals, message=message)