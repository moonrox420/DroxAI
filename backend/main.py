from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import socket
import json
import os
import logging
from security_utils import detect_anomaly, block_ip
from bot_engine import check_uptime, process_triggers
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="DroxAI Backend API",
    description="Backend API for DroxAI cybersecurity platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load bots configuration
def load_bots_config():
    try:
        with open("droxai_bots_manifest.json") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("droxai_bots_manifest.json not found")
        return {"bots": [], "global_settings": {}}

@app.get("/")
def root():
    return {
        "message": "DroxAI Backend API",
        "status": "online",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "timestamp": datetime.utcnow().isoformat(),
        "host": socket.gethostname(),
        "service": "DroxAI Backend"
    }

@app.get("/api/bots")
def get_bots():
    """Get all configured bots"""
    config = load_bots_config()
    return {
        "bots": config.get("bots", []),
        "count": len(config.get("bots", []))
    }

@app.get("/api/bots/{bot_id}")
def get_bot(bot_id: str):
    """Get specific bot by ID"""
    config = load_bots_config()
    bots = config.get("bots", [])
    
    for bot in bots:
        if bot.get("id") == bot_id:
            return bot
    
    raise HTTPException(status_code=404, detail="Bot not found")

@app.post("/api/bots/{bot_id}/trigger")
def trigger_bot(bot_id: str):
    """Manually trigger a bot's monitoring process"""
    config = load_bots_config()
    bots = config.get("bots", [])
    
    for bot in bots:
        if bot.get("id") == bot_id and bot.get("enabled"):
            try:
                process_triggers(bot)
                return {
                    "status": "success",
                    "message": f"Bot {bot_id} triggered successfully",
                    "timestamp": datetime.utcnow().isoformat()
                }
            except Exception as e:
                logger.error(f"Error triggering bot {bot_id}: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error triggering bot: {str(e)}")
    
    raise HTTPException(status_code=404, detail="Bot not found or not enabled")

@app.get("/api/security/anomaly-check")
def anomaly_check(rate: float, threshold: float = 0.95):
    """Check if a rate is anomalous"""
    try:
        is_anomalous = detect_anomaly(rate, threshold)
        return {
            "rate": rate,
            "threshold": threshold,
            "is_anomalous": bool(is_anomalous),  # Convert numpy bool to Python bool
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in anomaly check: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in anomaly detection: {str(e)}")

@app.post("/api/security/block-ip")
def block_ip_endpoint(ip: str):
    """Block an IP address"""
    try:
        block_ip(ip)
        return {
            "status": "success",
            "message": f"IP {ip} blocked successfully",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error blocking IP {ip}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error blocking IP: {str(e)}")

@app.get("/api/uptime/{url:path}")
def check_uptime_endpoint(url: str):
    """Check uptime of a given URL"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        status = check_uptime(url)
        return {
            "url": url,
            "status_code": status,
            "is_up": status == 200,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error checking uptime for {url}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error checking uptime: {str(e)}")

@app.get("/api/logs")
def get_logs(limit: int = 100):
    """Get recent log entries"""
    log_path = "logs/guardian.log"
    try:
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                lines = f.readlines()
                recent_lines = lines[-limit:] if len(lines) > limit else lines
                return {
                    "logs": [line.strip() for line in recent_lines],
                    "count": len(recent_lines),
                    "total_lines": len(lines)
                }
        else:
            return {
                "logs": [],
                "count": 0,
                "total_lines": 0,
                "message": "Log file not found"
            }
    except Exception as e:
        logger.error(f"Error reading logs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error reading logs: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)