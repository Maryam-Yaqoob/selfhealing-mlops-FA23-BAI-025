import time
import requests
from prometheus_client import start_http_server, Gauge

CONFIDENCE_SCORE = Gauge('prediction_confidence_score', 'Latest prediction confidence score')

APP_URL = "http://localhost:32500/api/latest-confidence"

def collect_metrics():
    while True:
        try:
            response = requests.get(APP_URL, timeout=5)
            data = response.json()
            confidence = data.get("confidence", 1.0)
            CONFIDENCE_SCORE.set(confidence)
        except Exception:
            CONFIDENCE_SCORE.set(1.0)
        time.sleep(5)

if __name__ == "__main__":
    start_http_server(8000)
    print("Exporter running on port 8000")
    collect_metrics()
