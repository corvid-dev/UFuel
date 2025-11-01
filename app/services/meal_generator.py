# app/services/meal_generator.py
import sqlite3
import os
import itertools
import random

BREAKFAST_PERCENT = 0.25
LUNCH_PERCENT = 0.35
DINNER_PERCENT = 0.4

def generate_meal_plan(
    total_calories,
    breakfast_location=None,
    lunch_location=None,
    dinner_location=None,
    db_path=None
):
    """
    Generate a location-aware meal plan without cross-location drinks.
    If no drinks exist for a location, defaults to Water.
    """
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

    plan = {}

    # Location mapping per meal type
    location_map = {
        "breakfast": breakfast_location,
        "lunch": lunch_location,
        "dinner": dinner_location
    }

    for meal_type, fraction in calorie_distribution.items():
        loc = location_map[meal_type]

        # Fetch meals and drinks specific to this location
        meals = fetch_all(cursor, meal_type, loc)
        drinks = fetch_all(cursor, "drink", loc)

        target_cal = total_calories * fraction
        drink_percent = 0.2
        food_target = target_cal * (1-drink_percent)
        drink_target = target_cal * drink_percent

        # Pick best food combo
        meal_combo = choose_best_combination(meals, food_target)

        # Pick best drink — or fallback to Water if none available
        if drinks:
            drink_choice = choose_best_combination(drinks, drink_target, max_items=1)
        else:
            drink_choice = [fallback_item("Water", 0, loc)]

        # Fallbacks for missing food
        if not meal_combo:
            meal_combo = [fallback_item(f"{meal_type.title()} Special", food_target, loc)]
        if not drink_choice:
            drink_choice = [fallback_item("Water", 0, loc)]

        total_meal_cal = round(
            sum(m["calories"] for m in meal_combo) +
            sum(d["calories"] for d in drink_choice),
            1
        )

        plan[meal_type] = {
            "meals": meal_combo,
            "drink": drink_choice[0],
            "location": loc or "Any",
            "target_fraction": fraction,
            "target_meal_period_calories": round(target_cal,1),
            "total_meal_period_calories": total_meal_cal
        }

    conn.close()

    total_selected = sum(p["total_meal_period_calories"] for p in plan.values())

    return {
        "total_target_calories": round(total_calories, 1),
        "total_selected_calories": round(total_selected, 1),
        "match_percent": round((total_selected / total_calories) * 100, 1) if total_calories else 0,
        "plan": plan
    }



# --- Combination Search (0–1 Knapsack heuristic) ---
# Modified so that it has a tolerance so we have variety, rather than the most optimal.
def choose_best_combination(meals, target, max_items=3, tolerance=0.1):
    """
    Selects up to `max_items` meals whose total calories are within
    `tolerance` (e.g. 0.1 = ±10%) of the target.
    If multiple fit, picks one at random for variety.
    """
    if not meals:
        return None

    meals = sorted(meals, key=lambda m: m["calories"])

    combos_in_range = []
    best_diff = float("inf")
    best_combo = None

    lower_bound = target * (1 - tolerance)
    upper_bound = target * (1 + tolerance)

    for r in range(1, max_items + 1):
        for combo in itertools.combinations(meals, r):
            total_cal = sum(m["calories"] for m in combo)
            diff = abs(total_cal - target)

            # Collect all combos within tolerance range
            if lower_bound <= total_cal <= upper_bound:
                combos_in_range.append(combo)

            # Track the absolute best (fallback if no combos fit)
            if diff < best_diff:
                best_diff = diff
                best_combo = combo

    # Prefer random variety within range, else fallback to best
    if combos_in_range:
        return list(random.choice(combos_in_range))
    return list(best_combo) if best_combo else None



# --- DB & Fallback helpers ---

def fetch_all(cursor, meal_type, location=None):
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

    return [
        {
            "name": r[0],
            "calories": float(r[1]),
            "carbs": float(r[2]),
            "fat": float(r[3]),
            "protein": float(r[4]),
            "location": r[5]
        }
        for r in results
    ]


def fallback_item(name, cal, location=None):
    return {
        "name": name,
        "calories": round(cal, 1),
        "carbs": 0,
        "fat": 0,
        "protein": 0,
        "location": location or "Any"
    }
