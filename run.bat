@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
echo ContentForge running at http://127.0.0.1:8000/
echo Demo login: demo / demo1234
python manage.py runserver
