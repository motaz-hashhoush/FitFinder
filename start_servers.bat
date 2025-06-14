@echo off
echo Starting Resume Ranker Application...
echo.

REM Start backend server
echo Starting Flask Backend Server...
start cmd /k "cd backend && venv\Scripts\python flask_server.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend server
echo Starting React Frontend Server...
start cmd /k "cd my-app && npm run dev"

echo.
echo Both servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo.
pause 