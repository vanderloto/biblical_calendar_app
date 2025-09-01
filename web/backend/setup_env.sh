#!/bin/bash

# Setup isolated environment for Biblical Calendar Web Backend

echo "🔧 Setting up Biblical Calendar Web Backend environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install compatible numpy first
echo "🔧 Installing compatible numpy..."
pip install "numpy<2.0" --upgrade

# Install requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

echo "✅ Environment setup complete!"
echo ""
echo "🚀 To run the backend:"
echo "source venv/bin/activate"
echo "python app.py"
echo ""
echo "Or simply run: python run.py"