@echo off
REM Build frontend for deployment

echo 🔨 Building Vue.js frontend...

cd frontend

REM Install dependencies
echo 📦 Installing dependencies...
npm ci --only=production

REM Build for production
echo 🏗️ Building for production...
npm run build

REM Copy to static directory
echo 📁 Copying to static directory...
if not exist "..\static" mkdir "..\static"
xcopy /E /Y "dist\*" "..\static\"

echo ✅ Frontend build complete!
echo 📂 Files copied to web/static/