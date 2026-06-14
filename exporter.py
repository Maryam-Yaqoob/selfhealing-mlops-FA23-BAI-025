import time
import requests
from prometheus_client import start_http_server, Gauge

# Metric definition
PREDICTION_CONFIDENCE = Gauge('prediction_confidence_score', 'Latest prediction confidence score from the ML model')

# Application NodePort URL inside EC2
APP_URL = "http://172.31.34.177:32500/api/latest-confidence"

def track_metrics():
    while True:
        try:
            response = requests.get(APP_URL, timeout=2)
            if response.status_code == 200:
                data = response.json()
                confidence = data.get("confidence", 1.0)
                PREDICTION_CONFIDENCE.set(confidence)
            else:
                PREDICTION_CONFIDENCE.set(1.0)
        except Exception:
            PREDICTION_CONFIDENCE.set(1.0)
        time.sleep(5)

if __name__ == '__main__':
    # Exporter port 8000 par start karein
    start_http_server(8000)
    print("Prometheus Custom Exporter running on port 8000...")
    track_metrics()
