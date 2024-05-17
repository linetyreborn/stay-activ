@echo off

REM Path to your Python script (app.py)
set "app_path=%~dp0app.py"

REM Check if the app is already running
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq %app_path:~0,-3%" | findstr python.exe > nul
if errorlevel 1 (
    echo Starting the app...
    REM Run your Flask app
    start "" python "%app_path%"
) else (
    echo App is already running.
)

REM Wait for the Flask app to start (adjust the delay if needed)
timeout /t 5

REM Open the web browser to the Flask app URL
start "" http://127.0.0.1:5000