#!/bin/bash

# Quick DroxAI startup script - minimal version for testing

echo "🚀 Starting DroxAI Platform (Quick Mode)..."

# Kill any existing processes on our ports
pkill -f "uvicorn.*main:app" 2>/dev/null || true
pkill -f "react-scripts start" 2>/dev/null || true
pkill -f "bot_engine.py" 2>/dev/null || true

# Go to project root
cd "$(dirname "$0")"

# Start backend
echo "Starting backend..."
cd backend
python3 main.py &
BACKEND_PID=$!
echo "Backend started (PID: $BACKEND_PID)"

# Wait for backend to be ready
sleep 3

# Test backend
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
fi

# Start bot engine
echo "Starting bot engine..."
python3 bot_engine.py &
BOT_PID=$!
echo "Bot engine started (PID: $BOT_PID)"

cd ..

echo ""
echo "🎉 DroxAI Platform is running!"
echo "Backend: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Health: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop"

# Keep running
trap "echo 'Stopping...'; kill $BACKEND_PID $BOT_PID 2>/dev/null; exit" INT TERM

while true; do
    sleep 1
done