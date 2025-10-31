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
        # generates meal plan based on user demographic and goals
        """
        Expected JSON body:
        {
            "age": 25,
            "height_in": 70,
            "weight_lb": 165,
            "gender": "male",
            "activity_level": "moderate",
            "goal": "maintain",
            "location": "Glen"
        }
        """
        try:
            # Parse input from frontend
            data = request.get_json()
            if not data:
                return jsonify({"error": "No input received"}), 400

            # Step 1: Calculate required daily calories
            required_calories = calories_required(
                age=data.get('age'),
                height_in=data.get('height_in'),
                weight_lb=data.get('weight_lb'),
                gender=data.get('gender'),
                activity_level=data.get('activity_level'),
                goal=data.get('goal')
            )

            # Step 2: Generate meal plan
            plan = generate_meal_plan(
                total_calories=required_calories,
                location=data.get('location')
            )

            # Step 3: Return structured JSON
            return jsonify({
                "target_daily_calories": required_calories,
                "meal_plan": plan
            }), 200

        except KeyError as e:
            return jsonify({"error": f"Missing required field: {e}"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
