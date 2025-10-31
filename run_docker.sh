#!/bin/bash
echo "Starting UFUEL Flask app in Docker..."
docker run -p 5000:5000 -v ${PWD}:/app ufuel
