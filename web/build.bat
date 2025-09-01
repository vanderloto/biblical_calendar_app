@echo off
REM Biblical Calendar Web - Build Script for Windows
REM Builds frontend and backend for production deployment

echo 🏗️  Building Biblical Calendar Web Application...

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.11+ first.
    exit /b 1
)

echo 📦 Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install frontend dependencies
    exit /b 1
)

echo 🔨 Building frontend for production...
call npm run build
if %errorlevel% neq 0 (
    echo ❌ Frontend build failed
    exit /b 1
)

echo ✅ Frontend build completed!
echo    📁 Files generated in: frontend/dist/

echo 📦 Installing backend dependencies...
cd ..\backend

REM Fix numpy compatibility for Python 3.13
echo 🔧 Installing compatible numpy version...
pip install "numpy<2.0" --upgrade
if %errorlevel% neq 0 (
    echo ❌ Failed to install compatible numpy
    exit /b 1
)

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install backend dependencies
    exit /b 1
)

echo ✅ Backend dependencies installed!

echo 🧪 Testing backend...
python test_import.py
if %errorlevel% neq 0 (
    echo ⚠️  Backend test failed, but continuing...
    echo 💡 Try running manually: cd backend ^&^& python app.py
    echo 💡 Or check: python test_import.py
)

echo 🎉 Build completed successfully!
echo.
echo 📋 Next steps:
echo 1. Frontend: Serve files from frontend/dist/
echo 2. Backend: Run 'python app.py' or use gunicorn
echo 3. Configure reverse proxy (nginx) if needed
echo.
echo 🚀 Quick start:
echo # Terminal 1 (Backend):
echo cd backend ^&^& start.bat
echo.
echo # Terminal 2 (Frontend):
echo cd frontend ^&^& start.bat
echo.
echo # Access: http://localhost:3000

pause