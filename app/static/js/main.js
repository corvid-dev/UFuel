document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("generate-btn");
    const mealName = document.getElementById("meal-name");
    const mealLocation = document.getElementById("meal-location");

    button.addEventListener("click", async () => {
        try {
            const response = await fetch("/generate-meal");
            const data = await response.json();

            mealName.textContent = data.meal_name;
            mealLocation.textContent = data.location ? `Location: ${data.location}` : "";
        } catch (error) {
            mealName.textContent = "Error generating meal.";
            mealLocation.textContent = "";
            console.error(error);
        }
    });
});
