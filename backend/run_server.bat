@echo off
echo Starting Flask Backend Server with Virtual Environment...
cd /d "%~dp0"
venv\Scripts\python flask_server.py
pause 