#!/bin/bash
# Startup script for Nordnet Trading Simulator

echo "🚀 Starting Nordnet Trading Simulator..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.x"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js"
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Start backend server in background
echo "🔧 Starting backend server..."
python3 -m backend.api &
BACKEND_PID=$!
echo "Backend server started with PID: $BACKEND_PID"

# Wait for backend to be ready
sleep 3

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install

# Start frontend
echo "🌐 Starting frontend..."
npm start

# Cleanup on exit
trap "kill $BACKEND_PID" EXIT
