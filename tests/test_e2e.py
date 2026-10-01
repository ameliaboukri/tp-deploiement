import os
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")

def test_app_disponible():
    resp = requests.get(f"{BASE_URL}/health", timeout=5)
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_endpoint_hello():
    resp = requests.get(f"{BASE_URL}/hello", timeout=5)
    assert resp.status_code == 200
    assert "message" in resp.json()