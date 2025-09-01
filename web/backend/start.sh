#!/bin/bash

# Quick start script for Biblical Calendar Web Backend

echo "🚀 Starting Biblical Calendar Web Backend..."

# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install/upgrade dependencies
echo "🔧 Installing dependencies..."
pip install "numpy<2.0" --upgrade --quiet
pip install -r requirements.txt --quiet

# Set Python path
export PYTHONPATH="$(pwd)/../../src"

# Run the app
echo "✅ Starting Flask server..."
python app.py