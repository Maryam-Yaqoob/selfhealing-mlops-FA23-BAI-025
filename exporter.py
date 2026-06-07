from prometheus_client import Gauge, start_http_server
import requests
import time

CONFIDENCE = Gauge(
    "prediction_confidence_score",
    "Latest prediction confidence score"
)

APP_URL = "http://localhost:5000/api/latest-confidence"

def update_metric():
    try:
        response = requests.get(APP_URL, timeout=5)
        confidence = response.json().get("confidence", 1.0)
        CONFIDENCE.set(confidence)
    except Exception:
        CONFIDENCE.set(1.0)

if __name__ == "__main__":
    start_http_server(8000)

    while True:
        update_metric()
        time.sleep(5)
