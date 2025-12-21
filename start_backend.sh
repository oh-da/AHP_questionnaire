#!/bin/bash
# Start AHP Questionnaire Backend Server

echo "=================================="
echo "AHP Questionnaire Backend Server"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements-backend.txt

# Start server
echo ""
echo "Starting server..."
python -m backend.main
