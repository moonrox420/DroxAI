import os
import json
import time
import requests
import logging
import redis
from security_utils import detect_anomaly, block_ip

# Force-safe logging encoding
log_path = "logs/guardian.log"
os.makedirs(os.path.dirname(log_path), exist_ok=True)
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Load manifest
with open("droxai_bots_manifest.json") as f:
    config = json.load(f)

bots = config["bots"]
global_settings = config["global_settings"]
redis_client = redis.Redis.from_url(global_settings["redis_host"])

def check_uptime(url):
    try:
        r = requests.get(url, timeout=5)
        logging.info(f"[UPTIME] {url} → {r.status_code}")
        return r.status_code
    except Exception as e:
        logging.error(f"[UPTIME ERROR] {url}: {str(e)}")
        return None

def ml_anomaly_check(rate, threshold=0.95):
    return detect_anomaly(rate, threshold)

def process_triggers(bot):
    url = bot["settings"]["monitor_endpoint"]
    threshold = bot["settings"].get("anomaly_threshold", 0.95)
    status = check_uptime(url)

    # Check if bot has uptime monitoring triggers
    uptime_triggers = [t for t in bot["triggers"] if "check_uptime" in str(t.get("actions", []))]
    if uptime_triggers and status and status != 200:
        logging.warning(f"[TRIGGER] Uptime anomaly at {url} → {status}")
        block_ip(bot.get("ip", "unknown"))

    # Check if bot has anomaly detection triggers
    anomaly_triggers = [t for t in bot["triggers"] if "ml_anomaly_check" in str(t.get("actions", []))]
    if anomaly_triggers:
        simulated_rate = status or 0
        if ml_anomaly_check(simulated_rate, threshold):
            logging.warning(f"[TRIGGER] ML anomaly at {url} → {simulated_rate}")
            block_ip(bot.get("ip", "unknown"))

def main_loop():
    logging.info("SiteGuardian Bot Engine launched.")
    while True:
        for bot in bots:
            if bot.get("enabled"):
                process_triggers(bot)
        time.sleep(60)

if __name__ == "__main__":
    main_loop()
