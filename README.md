# UFuel

**COSC412 Software Engineering Project**  
_J3R Industries_

---

Meal Planning Application for Towson Dining Halls

### Placeholder Readme

1. Build the database using Python:

   ```
   navigate to: app/meal-library
   run py db_setup.py
   run py import_meals.py
   run py verify_meals.py
   ```

You should see the meal_library.db be created.

2a. Windows: Build Docker using PowerShell:
   Install Docker Desktop for Windows.
   Navigate to the UFuel directory in Powershell or in the VSCode terminal.
   Then run rebuild_launch_docker.ps1. Sample command below:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\rebuild_launch_docker.ps1
   ```
   
2b. MacOS: Build Docker using bash:
   Install Docker Desktop for Mac.
   Navigate to the UFuel directory in the MacOS Terminal. 
   Then run commands below:

   ```bash
   chmod +x rebuild_launch_docker.sh
	./rebuild_launch_docker.sh
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
