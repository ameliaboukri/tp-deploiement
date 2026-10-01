from app import app

def test_health():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"

def test_hello():
    client = app.test_client()
    resp = client.get("/hello")
    assert resp.status_code == 200
    assert "message" in resp.get_json()