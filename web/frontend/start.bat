@echo off
REM Quick start script for Biblical Calendar Web Frontend

echo 🌐 Starting Biblical Calendar Web Frontend...

REM Check if dist folder exists
if not exist "dist" (
    echo 📦 Building frontend...
    call npm install
    call npm run build
) else (
    echo ✅ Using existing build in dist/
)

REM Start HTTP server
echo 🚀 Starting server on http://localhost:3000
cd dist
python -m http.server 3000

pause