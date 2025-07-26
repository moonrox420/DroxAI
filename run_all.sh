#!/bin/bash

# DroxAI Platform Startup Script
# This script runs all components of the DroxAI platform

set -e

echo "🚀 Starting DroxAI Platform..."
echo "======================================"

# Define colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_section() {
    echo -e "\n${BLUE}[SECTION]${NC} $1"
    echo "--------------------------------------"
}

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"

# Check if we're in the right directory
if [ ! -d "$PROJECT_ROOT/backend" ] || [ ! -d "$PROJECT_ROOT/frontend" ]; then
    print_error "Please run this script from the DroxAI project root directory"
    exit 1
fi

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to stop processes on ports
cleanup() {
    print_section "Cleaning up processes..."
    
    # Kill processes on common ports
    for port in 3000 8000 9000; do
        if check_port $port; then
            print_warning "Stopping process on port $port"
            kill -9 $(lsof -ti:$port) 2>/dev/null || true
        fi
    done
    
    # Kill background processes started by this script
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$BOT_PID" ]; then
        kill $BOT_PID 2>/dev/null || true
    fi
}

# Set up signal handlers for graceful shutdown
trap cleanup EXIT INT TERM

print_section "Environment Setup"

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed"
    exit 1
fi
print_status "Python 3: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is required but not installed"
    exit 1
fi
print_status "Node.js: $(node --version)"

# Check npm
if ! command -v npm &> /dev/null; then
    print_error "npm is required but not installed"
    exit 1
fi
print_status "npm: $(npm --version)"

print_section "Installing Dependencies"

# Install backend dependencies
print_status "Installing backend dependencies..."
cd "$PROJECT_ROOT/backend"
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found in backend directory"
    exit 1
fi

python3 -m pip install -r requirements.txt --user --quiet || {
    print_error "Failed to install backend dependencies"
    exit 1
}
print_status "Backend dependencies installed"

# Install frontend dependencies
print_status "Installing frontend dependencies..."
cd "$PROJECT_ROOT/frontend"
if [ ! -f "package.json" ]; then
    print_error "package.json not found in frontend directory"
    exit 1
fi

npm install --silent || {
    print_error "Failed to install frontend dependencies"
    exit 1
}
print_status "Frontend dependencies installed"

print_section "Starting Services"

# Create logs directory
mkdir -p "$PROJECT_ROOT/logs"

# Start backend service
print_status "Starting FastAPI backend on port 8000..."
cd "$PROJECT_ROOT/backend"
python3 main.py > "$PROJECT_ROOT/logs/backend.log" 2>&1 &
BACKEND_PID=$!
sleep 3

# Check if backend started successfully
if ! check_port 8000; then
    print_error "Backend failed to start on port 8000"
    cat "$PROJECT_ROOT/logs/backend.log"
    exit 1
fi
print_status "Backend started successfully (PID: $BACKEND_PID)"

# Start frontend service
print_status "Starting React frontend on port 3000..."
cd "$PROJECT_ROOT/frontend"
npm start > "$PROJECT_ROOT/logs/frontend.log" 2>&1 &
FRONTEND_PID=$!
sleep 5

# Check if frontend started successfully
if ! check_port 3000; then
    print_error "Frontend failed to start on port 3000"
    cat "$PROJECT_ROOT/logs/frontend.log"
    exit 1
fi
print_status "Frontend started successfully (PID: $FRONTEND_PID)"

# Start bot engine
print_status "Starting SiteGuardian bot engine..."
cd "$PROJECT_ROOT/backend"
python3 bot_engine.py > "$PROJECT_ROOT/logs/bot_engine.log" 2>&1 &
BOT_PID=$!
print_status "Bot engine started successfully (PID: $BOT_PID)"

print_section "Service Status"

# Health checks
sleep 2
print_status "Performing health checks..."

# Check backend health
if curl -s http://localhost:8000/health > /dev/null; then
    print_status "✅ Backend health check passed"
else
    print_warning "⚠️  Backend health check failed"
fi

# Check frontend
if curl -s http://localhost:3000 > /dev/null; then
    print_status "✅ Frontend health check passed"
else
    print_warning "⚠️  Frontend health check failed"
fi

print_section "DroxAI Platform Ready!"

echo -e "${GREEN}"
cat << "EOF"
 ____            __   _    ___ 
|  _ \ _ __ ___  \ \ _| |  |_ _|
| | | | '__/ _ \  \ / _ |   | | 
| |_| | | | (_) |/ / (_| |  | | 
|____/|_|  \___//_/ \__,_| |___|
                                
Cybersecurity Platform
EOF
echo -e "${NC}"

echo "🌐 Services are running:"
echo "   Backend API:    http://localhost:8000"
echo "   API Docs:       http://localhost:8000/docs" 
echo "   Frontend:       http://localhost:3000"
echo "   Bot Engine:     Running in background"
echo ""
echo "📊 Monitoring:"
echo "   Health Check:   http://localhost:8000/health"
echo "   System Status:  http://localhost:8000/api/status"
echo "   Bot Status:     http://localhost:8000/api/bots"
echo ""
echo "📁 Logs:"
echo "   Backend:        $PROJECT_ROOT/logs/backend.log"
echo "   Frontend:       $PROJECT_ROOT/logs/frontend.log"
echo "   Bot Engine:     $PROJECT_ROOT/logs/bot_engine.log"
echo "   Guardian:       $PROJECT_ROOT/backend/logs/guardian.log"
echo ""
echo "🛑 To stop all services, press Ctrl+C"
echo ""

# Keep the script running and monitor services
while true; do
    sleep 10
    
    # Check if services are still running
    if ! check_port 8000; then
        print_error "Backend service stopped unexpectedly"
        break
    fi
    
    if ! check_port 3000; then
        print_error "Frontend service stopped unexpectedly" 
        break
    fi
    
    # Check if bot engine is still running
    if ! kill -0 $BOT_PID 2>/dev/null; then
        print_warning "Bot engine stopped, restarting..."
        cd "$PROJECT_ROOT/backend"
        python3 bot_engine.py > "$PROJECT_ROOT/logs/bot_engine.log" 2>&1 &
        BOT_PID=$!
        print_status "Bot engine restarted (PID: $BOT_PID)"
    fi
done