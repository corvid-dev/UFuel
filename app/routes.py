# app/routes.py
from flask import render_template, jsonify, request
from app.services.nutrition import calories_required
from app.services.meal_generator import generate_meal_plan

def init_app(app):
    # Register all routes for the UFUEL Flask application.
    @app.route('/')
    def index():
        # Render the main testing page.
        return render_template('index.html')

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
