#!/bin/bash

# AHP Questionnaire Runner
# This script builds the React frontend and starts the Flask API server

set -e

echo "🚀 Starting AHP Questionnaire Setup..."

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Build React app
echo "🔨 Building React frontend..."
cd frontend
npm run build
cd ..

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r requirements-api.txt

# Start Flask server
echo "✅ Starting server at http://localhost:5000"
python api_server.py
