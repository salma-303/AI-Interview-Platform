#!/bin/bash

# Start the Python backend
python3 "AI-Interview-Platform-backend"/app.py &

# Start the frontend (e.g., Node.js, Vite, etc.)
npm run AI-Interview-Platform-frontend/dev
