#!/bin/bash


# Check if dependencies are installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python is not installed. Please install it."
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed. Please install Node.js and npm."
    exit 1
fi

# Navigate to backend directory
cd AI-Interview-Platform-backend || { echo "Error: Backend directory not found"; exit 1; }



# Start the backend with uvicorn
echo "Starting backend..."
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

# Wait briefly to ensure backend starts
sleep 20

# Navigate to frontend directory
cd ../AI-Interview-Platform-frontend || { echo "Error: Frontend directory not found"; exit 1; }

# Start the frontend
echo "Starting frontend..."
npm run dev
