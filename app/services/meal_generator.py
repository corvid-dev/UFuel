# app/services/meal_generator.py
import sqlite3
import os
import random

# Set ratio of calories
BREAKFAST_PERCENT = 0.25
LUNCH_PERCENT = 0.35
DINNER_PERCENT = 0.4

def generate_meal_plan(total_calories, location=None, db_path=None):

    calorie_distribution = {
        "breakfast": BREAKFAST_PERCENT,
        "lunch": LUNCH_PERCENT,
        "dinner": DINNER_PERCENT
    }

    # Resolve DB path
    if db_path is None:
        db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'meal-library', 'meal_library.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch all meals and drinks once
    meals_by_type = {}
    for meal_type in ["breakfast", "lunch", "dinner", "drink"]:
        meals_by_type[meal_type] = fetch_all(cursor, meal_type, location)

    plan = {}

    # Build each meal period (Breakfast+drink, Lunch+drink, Dinner+drink)
    for meal_type, fraction in calorie_distribution.items():
        target_total = total_calories * fraction

        # Split calories between food and drink, drink should be less than 1/4 total calories.
        drink_share = random.uniform(0.1, 0.25)
        drink_target = target_total * drink_share
        food_target = target_total * (1 - drink_share)

        # Pick best match for food and drink
        meal = choose_closest(meals_by_type.get(meal_type, []), food_target)
        drink = choose_closest(meals_by_type.get("drink", []), drink_target)

        # Fallbacks if DB lacks results
        if not meal:
            meal = fallback_item(f"{meal_type.title()} Special", food_target, location)
        if not drink:
            drink = fallback_item("Water", 0, location)

        total_meal_period = round(meal["calories"] + drink["calories"], 1)

        plan[meal_type] = {
            "meal": meal,
            "drink": drink,
            "target_fraction": fraction,
            "total_meal_period_calories": total_meal_period
        }

    conn.close()

    # Global calorie balancing
    total_selected = sum(p["total_meal_period_calories"] for p in plan.values())
    deviation = (total_selected - total_calories) / total_calories if total_calories else 0

    if abs(deviation) > 0.05 and total_selected > 0:
        adj = total_calories / total_selected
        print(f"[INFO] Adjusting meals globally (factor {adj:.3f})")

        for p in plan.values():
            for k in ["meal", "drink"]:
                item = p[k]
                if item:
                    item["calories"] = round(item["calories"] * adj, 1)
            p["total_meal_period_calories"] = round(
                (p["meal"]["calories"] if p["meal"] else 0)
                + (p["drink"]["calories"] if p["drink"] else 0),
                1
            )
        total_selected = sum(p["total_meal_period_calories"] for p in plan.values())

    # Final summary
    return {
        "total_target_calories": round(total_calories / 10) * 10,
        "total_selected_calories": round(total_selected / 10) * 10,
        "match_percent": round((total_selected / total_calories) * 100, 1) if total_calories else 0,
        "plan": plan
    }


# Helper methods

def fetch_all(cursor, meal_type, location=None):
# Gets all meals of target type and location from database

    query = """
        SELECT name, calories, carbohydrates, fat, protein, location
        FROM meals
        WHERE LOWER(TRIM(meal_type)) = LOWER(TRIM(?))
    """
    params = [meal_type]

    if location:
        query += " AND LOWER(TRIM(location)) = LOWER(TRIM(?))"
        params.append(location)

    cursor.execute(query, params)
    results = cursor.fetchall()

    meals = []
    for r in results:
        meals.append({
            "name": r[0],
            "calories": float(r[1]),
            "carbs": float(r[2]),
            "fat": float(r[3]),
            "protein": float(r[4]),
            "location": r[5]
        })
    return meals


def choose_closest(meals, target_cal):
# Finds closest meal to target calories
    if not meals:
        return None
    ranked = sorted(meals, key=lambda m: abs(m["calories"] - target_cal))
    top_n = ranked[:min(5, len(ranked))]
    return random.choice(top_n)


def fallback_item(name, cal, location=None):
# Fallback to ensure doesn't fail hard
    return {
        "name": name,
        "calories": round(cal, 1),
        "carbs": 0,
        "fat": 0,
        "protein": 0,
        "location": location or "Any"
    }
