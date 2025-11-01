# Step 1
Write-Host "Rebuild UFUEL Docker image..."

# Step 2
Write-Host "Stop Running Containers"
docker ps -q | ForEach-Object { docker stop $_ } 2>$null

# Step 3
Write-Host "Remove Stopped Containers"
docker ps -aq | ForEach-Object { docker rm -f $_ } 2>$null

# Step 4
Write-Host "Prune Unused Dockers Resources"
docker system prune -af --volumes

# Step 5
Write-Host "Build New Docker Image"
docker build -t ufuel . --no-cache --progress=plain

# Step 6
Write-Host "Start UFuel Container"
docker run -p 5000:5000 -v "${PWD}:/app" ufuel

# Step 7
Write-Host "Rebuild complete. UFUEL is running at http://localhost:5000"
