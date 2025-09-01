#!/bin/bash

# Quick start script for Biblical Calendar Web Frontend

echo "🌐 Starting Biblical Calendar Web Frontend..."

# Check if dist folder exists
if [ ! -d "dist" ]; then
    echo "📦 Building frontend..."
    npm install
    npm run build
else
    echo "✅ Using existing build in dist/"
fi

# Start HTTP server
echo "🚀 Starting server on http://localhost:3000"
cd dist
python3 -m http.server 3000