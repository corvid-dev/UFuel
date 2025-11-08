chmod +x rebuild_launch_docker.sh
./rebuild_launch_docker.sh


#!/bin/bash
# --------------------------------------------
# Rebuild and launch Docker environment on macOS
# Requires: Docker Desktop for Mac
# --------------------------------------------

# Step 1: Check if Docker is running
echo "Checking if Docker is running..."
if ! docker info >/dev/null 2>&1; then
    echo "Docker Desktop is not running. Attempting to start it..."

    # Locate Docker Desktop
    DOCKER_APP="/Applications/Docker.app"
    if [ ! -d "$DOCKER_APP" ]; then
        echo "Docker Desktop not found at /Applications/Docker.app"
        echo "Please install Docker Desktop from https://www.docker.com/products/docker-desktop/"
        exit 1
    fi

    # Start Docker Desktop
    open -a Docker
    echo "Starting Docker Desktop... please wait (~60s)"

    # Wait up to 60 seconds for Docker to start
    for i in {1..30}; do
        sleep 2
        if docker info >/dev/null 2>&1; then
            echo "Docker Desktop is now running."
            break
        fi

        if [ $i -eq 30 ]; then
            echo "Docker did not start within 60 seconds. Please start it manually."
            exit 1
        fi
    done
else
    echo " Docker Desktop is already running."
fi

# Step 2: Rebuild the UFuel Docker image
echo "--------------------------------------------"
echo "Rebuilding UFuel Docker image..."

# Step 3: Stop running containers
echo "Stopping running containers..."
docker ps -q | xargs -r docker stop

# Step 4: Remove stopped containers
echo "Removing stopped containers..."
docker ps -aq | xargs -r docker rm -f

# Step 5: Prune unused Docker resources
echo "Pruning unused Docker resources..."
docker system prune -af --volumes

# Step 6: Build new Docker image
echo "Building new Docker image (no cache)..."
docker build -t ufuel . --no-cache --progress=plain

# Step 7: Start the container
echo "Starting UFuel container..."
docker run -p 5000:5000 -v "$(pwd):/app" ufuel

# Step 8: Launch complete
echo "--------------------------------------------"
echo "Rebuild complete. UFUEL is running at http://localhost:5000"

# Step 9: Open browser automatically
open "http://127.0.0.1:5000/"