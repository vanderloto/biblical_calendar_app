@echo off
REM Setup isolated environment for Biblical Calendar Web Backend

echo 🔧 Setting up Biblical Calendar Web Backend environment...

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install compatible numpy first
echo 🔧 Installing compatible numpy...
pip install "numpy<2.0" --upgrade

REM Install requirements
echo 📦 Installing requirements...
pip install -r requirements.txt

echo ✅ Environment setup complete!
echo.
echo 🚀 To run the backend:
echo call venv\Scripts\activate.bat
echo python app.py
echo.
echo Or simply run: python run.py

pause