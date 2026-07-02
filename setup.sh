#!/bin/bash
# Setup script for FotoOwl AI Pipeline

set -e

echo "🦉 FotoOwl AI — Setup Script"
echo "=============================="
echo ""

# Check Python
echo "Checking Python version..."
python3 --version || { echo "Error: Python 3.11+ required"; exit 1; }

# Check Node.js
echo "Checking Node.js version..."
node --version || { echo "Error: Node.js 18+ required"; exit 1; }

# Create venv
echo ""
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate venv
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install Python deps
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Node deps
echo ""
echo "Installing Remotion dependencies..."
cd remotion
npm install
cd ..

# Create .env if missing
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your OPENAI_API_KEY"
echo "  2. Place images in sample_images/ folder"
echo "  3. Run: python main.py --images sample_images --prompt \"Your creative prompt\""
echo ""
