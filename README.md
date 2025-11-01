# UFuel

**COSC412 Software Engineering Project**  
_J3R Industries_

---

Meal planning application for Towson Dining Halls

### Placeholder Readme

1. Build the database using Python:

   ```
   navigate to: app/meal-library:
   run py db_setup.py
   run py import_meals.py
   run py verify_meals.py
   ```

You should see the meal_library.db be created.

2. Build Docker using PowerShell:
   Navigate to your folder. Either run Powershell as administrator or use the Set-ExecutionPolicy command below.
   Then run rebuild_launch_docker.ps1. Sample command below:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\rebuild_launch_docker.ps1
   ```

3. Using your internet browser, connect to [http://127.0.0.1:5000](http://127.0.0.1:5000)

**Backend**

```
- Python 3.11

- Flask

- SQlite

- Docker
```

**Frontend**

```
- HTML?

- Javascript?

- css?

```
