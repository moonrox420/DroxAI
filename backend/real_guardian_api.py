from fastapi import FastAPI
from datetime import datetime
import socket

app = FastAPI()

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "timestamp": datetime.utcnow().isoformat(),
        "host": socket.gethostname()
    }
