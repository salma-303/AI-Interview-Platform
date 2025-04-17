#!/bin/bash

# Exit on any error
set -e

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -i :$port > /dev/null; then
        echo "Error: Port $port is already in use. Please free it or change the port."
        exit 1
    fi
}

# Check if dependencies are installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed. Please install it."
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed. Please install Node.js and npm."
    exit 1
fi

# Navigate to backend directory
cd AI-Interview-Platform-backend || { echo "Error: Backend directory not found"; exit 1; }

# Check backend port (8000)
check_port 8000

# Install backend dependencies (if requirements.txt exists)
if [ -f requirements.txt ]; then
    echo "Installing backend dependencies..."
    pip3 install -r requirements.txt
fi

# Start the backend with uvicorn
echo "Starting backend..."
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

# Wait briefly to ensure backend starts
sleep 2

# Navigate to frontend directory
cd ../AI-Interview-Platform-frontend || { echo "Error: Frontend directory not found"; exit 1; }

# Check frontend port (8080 for Vite)
check_port 8080

# Install frontend dependencies (if package.json exists)
if [ -f package.json ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start the frontend
echo "Starting frontend..."
npm run dev
