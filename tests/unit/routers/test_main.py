from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello From Leto-Modelizer-AI-API!"}


def test_read_health():
    response = client.get("health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
