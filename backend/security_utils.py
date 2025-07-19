# security_utils.py
"""
Utility functions for SiteGuardian cybersecurity bot in DroxAI.
Provides anomaly detection and IP blocking capabilities.
"""
import numpy as np
from sklearn.ensemble import IsolationForest

def detect_anomaly(request_rate: int, threshold: float) -> bool:
    """
    Detect anomalies in request rates using Isolation Forest.
    Args:
        request_rate (int): Number of requests per minute.
        threshold (float): Anomaly threshold.
    Returns:
        bool: True if an anomaly is detected, False otherwise.
    """
    model = IsolationForest(contamination=0.1, random_state=42)
    data = np.array([[request_rate]])
    prediction = model.predict(data)
    return prediction[0] == -1 and request_rate > threshold

def block_ip(ip: str, redis_client) -> None:
    """
    Block an IP address using Redis.
    Args:
        ip (str): IP address to block.
        redis_client: Redis client instance.
    """
    redis_client.sadd("blocked_ips", ip)
