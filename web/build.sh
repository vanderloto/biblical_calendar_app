#!/bin/bash

# Biblical Calendar Web - Build Script
# Builds frontend and backend for production deployment

set -e

echo "🏗️  Building Biblical Calendar Web Application..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 18+ first.${NC}"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.11+ first.${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
cd frontend
npm install

echo -e "${YELLOW}🔨 Building frontend for production...${NC}"
npm run build

echo -e "${GREEN}✅ Frontend build completed!${NC}"
echo -e "   📁 Files generated in: frontend/dist/"

echo -e "${YELLOW}📦 Installing backend dependencies...${NC}"
cd ../backend

# Fix numpy compatibility
echo -e "${YELLOW}🔧 Installing compatible numpy version...${NC}"
pip install "numpy<2.0" --upgrade

pip install -r requirements.txt

echo -e "${GREEN}✅ Backend dependencies installed!${NC}"

echo -e "${YELLOW}🧪 Testing backend...${NC}"
python test_import.py

echo -e "${GREEN}🎉 Build completed successfully!${NC}"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "1. Frontend: Serve files from frontend/dist/"
echo "2. Backend: Run 'python app.py' or use gunicorn"
echo "3. Configure reverse proxy (nginx) if needed"
echo ""
echo -e "${YELLOW}🚀 Quick start:${NC}"
echo "# Terminal 1 (Backend):"
echo "cd backend && python run.py"
echo ""
echo "# Terminal 2 (Frontend):"
echo "cd frontend/dist && python -m http.server 3000"
echo ""
echo "# Access: http://localhost:3000"