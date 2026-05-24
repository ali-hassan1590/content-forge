@echo off
cd /d "%~dp0"
echo === ContentForge Setup ===

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt -q
python manage.py migrate
python manage.py seed_demo
echo.
echo === Done! Run: run.bat ===
pause
