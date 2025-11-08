# app/services/nutrition.py
def calories_required(age, height_in, weight_lb, gender, activity_level, goal):
    """Calculates the TDEE calories required using Mifflin-St Jeor"""
    # Convert to metric
    weight_kg = weight_lb * 0.453592
    height_cm = height_in * 2.54

    # Mifflin-St Jeor
    if gender.lower() == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    # Activity multiplier
    activity_factors = {"sedentary": 1.2, "moderate": 1.55, "active": 1.725}
    tdee = bmr * activity_factors.get(activity_level.lower(), 1.2)

    # Goal adjustment
    if goal.lower() == "gain":
        tdee += 500
    elif goal.lower() == "lose":
        tdee -= 500
    tdee = round(tdee / 10) * 10

    """
    Formula
    Source: https://reference.medscape.com/calculator/846/mifflin-st-jeor-equation
    Females: (10*weight [kg]) + (6.25*height [cm]) - (5*age [years]) - 161
    Males: (10*weight [kg]) + (6.25*height [cm]) - (5*age [years]) + 5

    Multiply by scale factor for activity level:
    Sedentary *1.2
    Lightly active *1.375
    Moderately active *1.55
    Active *1.725
    Very active *1.9
    """

    # Ensure between 1000 and 5000 calories
    tdee = min(tdee, 5000)
    tdee = max(1000, tdee)

    return int(tdee)
