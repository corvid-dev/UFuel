from flask import render_template, jsonify
import sqlite3
import random

def init_app(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/generate-meal')
    def generate_meal():
        conn = sqlite3.connect('meal-library/meal_library.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, location FROM meals")
        meals = cursor.fetchall()
        conn.close()

        if meals:
            meal = random.choice(meals)
            meal_name, location = meal
        else:
            meal_name, location = "No meals found", ""

        return jsonify({'meal_name': meal_name, 'location': location})
