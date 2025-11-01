Write-Host "Rebuild UFUEL Docker image..."

# Step 1: Write-Host "Stop Running Containers"
docker ps -q | ForEach-Object { docker stop $_ } 2>$null

# Step 2: Clean up any stopped containers
Write-Host "Clean Stopped Containers"
docker ps -aq | ForEach-Object { docker rm -f $_ } 2>$null

# Step 3: Prune unused Docker resources
Write-Host "Prune Unused Dockers"
docker system prune -af --volumes

# Step 4: Build the Docker image
Write-Host "Build New Docker Image"
docker build -t ufuel . --no-cache --progress=plain

# Step 5: Run the container
Write-Host "Start UFuel Container"
docker run -p 5000:5000 -v "${PWD}:/app" ufuel

# Step 6: Print Completion
Write-Host "Rebuild complete. UFUEL is running at http://localhost:5000"
