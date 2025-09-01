@echo off
REM Quick start script for Biblical Calendar Web Backend

echo 🚀 Starting Biblical Calendar Web Backend...

REM Check if venv exists, if not create it
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo 🔧 Installing dependencies...
pip install "numpy<2.0" --upgrade --quiet
pip install -r requirements.txt --quiet

REM Set Python path
set PYTHONPATH=%cd%\..\..\src

REM Run the app
echo ✅ Starting Flask server...
python app.py

pause