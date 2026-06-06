@echo off
echo Starting CaliForge AI...

echo Starting Backend Server...
start cmd /k "cd backend && call venv\Scripts\activate && uvicorn app.main:app --reload"

echo Starting Frontend Server...
start cmd /k "cd frontend && npm run dev"

echo Both servers are starting up!
