# app/services/meal_planner.py

from app.services.user_nutrition import calories_required
from app.services.meal_generator import generate_meal_plan


def generate_full_meal_plan(data):
    """Generates Meal Plan"""
    required_fields = [
        "age",
        "height_in",
        "weight_lb",
        "gender",
        "activity_level",
        "goal",
        "breakfast_location",
        "lunch_location",
        "dinner_location",
    ]
    missing = [f for f in required_fields if f not in data]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    # Step 1: Calculate required daily calories
    required_calories = calories_required(
        age=data["age"],
        height_in=data["height_in"],
        weight_lb=data["weight_lb"],
        gender=data["gender"],
        activity_level=data["activity_level"],
        goal=data["goal"],
    )

    # Step 2: Generate meal plan with per-meal locations
    plan = generate_meal_plan(
        total_calories=required_calories,
        breakfast_location=data["breakfast_location"],
        lunch_location=data["lunch_location"],
        dinner_location=data["dinner_location"],
    )

    # Step 3: Structure and return the result
    return {"target_daily_calories": required_calories, "meal_plan": plan}
