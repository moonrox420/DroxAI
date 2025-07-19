import logging
import random
from sklearn.ensemble import IsolationForest

# Train basic model
model = IsolationForest(random_state=42)
model.fit([[random.random()] for _ in range(100)])

def detect_anomaly(rate, threshold=0.95):
    data = [[rate]]
    prediction = model.predict(data)
    score = model.decision_function(data)[0]
    is_anomalous = prediction[0] == -1 and score < -threshold
    logging.info(f"[ANOMALY DETECTION] Rate: {rate}, Score: {score}, Anomalous: {is_anomalous}")
    return is_anomalous

def block_ip(ip="unknown"):
    logging.warning(f"[SECURITY] Blocking IP: {ip}")
