# 🚀 Running DroxAI Platform - "Run It All" Guide

This guide explains how to run the complete DroxAI cybersecurity platform with all its components.

## 🏗️ Platform Components

DroxAI consists of three main components:
- **Backend API**: FastAPI-based REST API (Port 8000)
- **Frontend**: React-based web interface (Port 3000)  
- **Bot Engine**: SiteGuardian monitoring system (Background service)

## ⚡ Quick Start - Run Everything

### Option 1: Quick Start Script (Recommended)
```bash
# Run the backend and bot engine
./quick_start.sh
```

### Option 2: Full Platform Script
```bash
# Run all components including frontend
./run_all.sh
```

### Option 3: Docker (Production)
```bash
# Build and run with Docker
docker build -t droxai .
docker run -p 8000:8000 -p 3000:3000 droxai
```

## 📋 Prerequisites

- **Python 3.12+** with pip
- **Node.js 20+** with npm  
- **curl** (for health checks)

## 🔧 Manual Setup

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 3. Bot Engine
```bash
cd backend
python bot_engine.py
```

## 🌐 Access Points

Once running, access the platform at:

| Service | URL | Description |
|---------|-----|-------------|
| **Backend API** | http://localhost:8000 | Main API endpoint |
| **API Documentation** | http://localhost:8000/docs | Interactive API docs |
| **Frontend** | http://localhost:3000 | Web interface |
| **Health Check** | http://localhost:8000/health | System health status |
| **System Status** | http://localhost:8000/api/status | Component status |
| **Bot Status** | http://localhost:8000/api/bots | Monitoring bots |

## 📊 API Endpoints

### Core Endpoints
- `GET /` - API status
- `GET /health` - Health check with uptime
- `GET /api/status` - System component status

### Monitoring Endpoints  
- `GET /api/bots` - Bot status and configuration
- `GET /api/alerts` - Recent security alerts
- `GET /api/monitoring/stats` - Platform statistics
- `POST /api/bots/{bot_id}/toggle` - Toggle bot status

## 🤖 Bot Engine Features

The SiteGuardian bot engine provides:
- **Uptime Monitoring**: Continuous endpoint health checks
- **ML Anomaly Detection**: Machine learning-based threat detection  
- **Security Alerts**: Real-time notification system
- **Auto-blocking**: Automatic IP blocking for threats

## 📁 Logs and Monitoring

Logs are stored in:
- `logs/backend.log` - API server logs
- `logs/frontend.log` - React development server logs  
- `logs/bot_engine.log` - Bot engine activity
- `backend/logs/guardian.log` - Security monitoring logs

## 🛠️ Development

### Running in Development Mode
```bash
# Terminal 1: Backend with hot reload
cd backend && python main.py

# Terminal 2: Frontend with hot reload  
cd frontend && npm start

# Terminal 3: Bot engine
cd backend && python bot_engine.py
```

### Environment Variables
Create `.env` files for configuration:
- `backend/.env` - API configuration
- `frontend/.env` - React environment

## 🐳 Docker Development

```bash
# Build development image
docker build -t droxai-dev .

# Run with volume mounting for development
docker run -p 8000:8000 -v $(pwd):/app droxai-dev
```

## 🔒 Security Features

- CORS protection for cross-origin requests
- JWT authentication support (configurable)
- Rate limiting and DDoS protection
- ML-based anomaly detection
- Real-time threat monitoring

## 🚨 Troubleshooting

### Port Conflicts
If ports 3000 or 8000 are in use:
```bash
# Kill processes on specific ports
sudo lsof -ti:3000 | xargs kill -9
sudo lsof -ti:8000 | xargs kill -9
```

### Dependency Issues
```bash
# Backend dependencies
cd backend && pip install -r requirements.txt --force-reinstall

# Frontend dependencies  
cd frontend && rm -rf node_modules && npm install
```

### Permission Issues
```bash
# Make scripts executable
chmod +x run_all.sh quick_start.sh
```

## 📈 Scaling and Production

### Production Deployment
- Use `gunicorn` for the backend API
- Build React for production with `npm run build`
- Configure reverse proxy (nginx/Apache)
- Set up proper logging and monitoring
- Configure environment-specific settings

### Performance Tuning
- Adjust `uvicorn` worker count
- Configure Redis for caching
- Set up database connections
- Implement proper error handling

## 🆘 Support

If you encounter issues:
1. Check the logs in the `logs/` directory
2. Verify all dependencies are installed
3. Ensure ports 3000 and 8000 are available
4. Run health checks: `curl http://localhost:8000/health`

## 🎯 What "Run It All" Achieves

The "run it all" implementation provides:
- ✅ **Single-command startup** for the entire platform
- ✅ **Health monitoring** and status checks
- ✅ **Automated dependency installation**
- ✅ **Service orchestration** with proper startup order
- ✅ **Graceful shutdown** and cleanup
- ✅ **Development and production** deployment options
- ✅ **Comprehensive logging** and monitoring
- ✅ **Error handling** and recovery