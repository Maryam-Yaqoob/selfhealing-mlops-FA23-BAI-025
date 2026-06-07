import os
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

def test_health_endpoint():
    response = requests.get(f"{BASE_URL}/health", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_version" in data

def test_predict_returns_label_and_confidence():
    response = requests.post(
        f"{BASE_URL}/predict",
        json={"text": "This product is excellent and amazing"},
        timeout=20
    )
    assert response.status_code == 200
    data = response.json()
    assert data["label"] in ["POSITIVE", "NEGATIVE"]
    assert 0 <= data["confidence"] <= 1
    assert "model_version" in data

def test_predict_negative_text():
    response = requests.post(
        f"{BASE_URL}/predict",
        json={"text": "This is terrible and awful"},
        timeout=20
    )
    assert response.status_code == 200

def test_health_returns_model_version_unstable():
    response = requests.get(f"{BASE_URL}/health", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert data["model_version"] == "unstable-v1"
