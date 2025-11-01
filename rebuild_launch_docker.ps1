# Start 
# Install Docker Desktop, default directory is C:\Program Files\Docker\
# To run this script, navigate to the folder containing rebuild_launch_docker.ps1,
# open Powershell as Administrator, 
# or run command: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# Then run: .\rebuild_launch_docker.ps1

# Step 1: Check if Docker is running
try {
    docker info > $null 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Docker Desktop is not running. Attempting to locate and start it..."

        # Try to locate Docker Desktop.exe
        $dockerPath = (Get-ChildItem "C:\Program Files" -Recurse -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -eq "Docker Desktop.exe" } |
            Select-Object -First 1 -ExpandProperty FullName)

        if (-not $dockerPath) {
            Write-Host "Docker Desktop could not be found under 'C:\Program Files'. Please start it manually and rerun this script."
            exit 1
        }
        if ($dockerPath) {
        Write-Host "Docker Desktop executable found at: $dockerPath"
    }
        # Attempt to start Docker Desktop
        Start-Process $dockerPath
        Write-Host "Starting Docker Desktop. Please wait..."

        # Wait for Docker to start (up to ~60 seconds)
        $dockerStarted = $false
        for ($i = 0; $i -lt 30; $i++) {
            Start-Sleep -Seconds 2
            docker info > $null 2>&1
            if ($LASTEXITCODE -eq 0) {
                $dockerStarted = $true
                break
            }
        }

        if (-not $dockerStarted) {
            Write-Host "Docker Desktop failed to start after waiting 60 seconds. Please open Docker Desktop manually and rerun this script."
            exit 1
        }
        else {
            Write-Host "Docker Desktop is now running and ready."
        }
    }
    else {
        Write-Host "Docker Desktop is already running."
    }
}
catch {
    Write-Host "Unable to connect to Docker. Make sure Docker Desktop is installed and running."
    exit 1
}



# Step 2
Write-Host "Rebuild UFUEL Docker image..."

# Step 3
Write-Host "Stop Running Containers"
docker ps -q | ForEach-Object { docker stop $_ } 2>$null

# Step 4
Write-Host "Remove Stopped Containers"
docker ps -aq | ForEach-Object { docker rm -f $_ } 2>$null

# Step 5
Write-Host "Prune Unused Dockers Resources"
docker system prune -af --volumes

# Step 6
Write-Host "Build New Docker Image"
docker build -t ufuel . --no-cache --progress=plain

# Step 7
Write-Host "Start UFuel Container"
docker run -p 5000:5000 -v "${PWD}:/app" ufuel

# Step 8
Write-Host "Rebuild complete. UFUEL is running at http://localhost:5000"
