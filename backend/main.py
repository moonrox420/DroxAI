#!/usr/bin/env python3
"""
DroxAI FastAPI Backend
Main application entry point for the DroxAI cybersecurity platform
"""

import os
import json
import logging
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from datetime import datetime
import asyncio

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="DroxAI API",
    description="DroxAI Cybersecurity Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "*"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    uptime: str

class BotStatus(BaseModel):
    id: str
    name: str
    status: str
    last_check: str

class SystemStatus(BaseModel):
    backend: str
    frontend: str
    bot_engine: str
    database: str

# Global variables
start_time = datetime.now()

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "DroxAI API is running", "status": "operational"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    uptime = str(datetime.now() - start_time)
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        uptime=uptime
    )

@app.get("/api/status", response_model=SystemStatus)
async def get_system_status():
    """Get overall system status"""
    return SystemStatus(
        backend="running",
        frontend="running",
        bot_engine="running",
        database="connected"
    )

@app.get("/api/bots", response_model=List[BotStatus])
async def get_bot_status():
    """Get status of all monitoring bots"""
    try:
        # Try to load bot manifest
        manifest_path = os.path.join(os.path.dirname(__file__), "droxai_bots_manifest.json")
        if os.path.exists(manifest_path):
            with open(manifest_path, "r") as f:
                config = json.load(f)
            
            bots = []
            for bot in config.get("bots", []):
                bots.append(BotStatus(
                    id=bot.get("id", "unknown"),
                    name=bot.get("name", "Unknown"),
                    status="active" if bot.get("enabled", False) else "inactive",
                    last_check=datetime.now().isoformat()
                ))
            return bots
        else:
            return [BotStatus(
                id="siteguardian",
                name="SiteGuardian",
                status="active",
                last_check=datetime.now().isoformat()
            )]
    except Exception as e:
        logger.error(f"Error getting bot status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get bot status")

@app.post("/api/bots/{bot_id}/toggle")
async def toggle_bot(bot_id: str):
    """Toggle bot status"""
    # This would integrate with the bot engine
    return {"message": f"Bot {bot_id} toggled", "status": "success"}

@app.get("/api/alerts")
async def get_alerts():
    """Get recent security alerts"""
    # Mock alerts for now
    return {
        "alerts": [
            {
                "id": "alert_1",
                "type": "uptime_check",
                "severity": "info",
                "message": "Site health check passed",
                "timestamp": datetime.now().isoformat()
            }
        ]
    }

@app.get("/api/monitoring/stats")
async def get_monitoring_stats():
    """Get monitoring statistics"""
    return {
        "uptime_checks": 1440,  # checks per day
        "threats_detected": 0,
        "requests_monitored": 10532,
        "avg_response_time": "45ms"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    logger.info("Starting DroxAI API server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )