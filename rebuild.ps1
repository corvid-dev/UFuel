Write-Host "Rebuilding UFUEL Docker image..." -ForegroundColor Cyan

# Step 1: Clean up any stopped containers
Write-Host "Cleaning up old containers..." -ForegroundColor Yellow
docker ps -aq | ForEach-Object { docker rm -f $_ } 2>$null

# Step 2: Prune unused Docker resources (optional but keeps things tidy)
Write-Host "Pruning unused Docker resources..." -ForegroundColor Yellow
docker system prune -af --volumes

# Step 3: Build the Docker image
Write-Host "Building new Docker image..." -ForegroundColor Yellow
docker build -t ufuel . --no-cache --progress=plain

# Step 4: Run the container
Write-Host "Starting the UFUEL container on port 5000..." -ForegroundColor Yellow
docker run -p 5000:5000 -v "$(Get-Location):/app" ufuel

Write-Host "Rebuild complete. UFUEL is running at http://localhost:5000" -ForegroundColor Green
