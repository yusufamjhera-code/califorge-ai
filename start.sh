#!/bin/bash

echo "Starting CaliForge AI..."

# Start Backend in background
echo "Starting Backend Server..."
(cd backend && source venv/bin/activate && uvicorn app.main:app --reload) &
BACKEND_PID=$!

# Start Frontend in background
echo "Starting Frontend Server..."
(cd frontend && npm run dev) &
FRONTEND_PID=$!

echo "Both servers are running! Press Ctrl+C to stop."

# Wait for user to press Ctrl+C, then kill both servers
trap "kill $BACKEND_PID $FRONTEND_PID" SIGINT
wait
