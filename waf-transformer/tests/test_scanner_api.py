from fastapi.testclient import TestClient


def _client() -> TestClient:
    from app.main import app

    return TestClient(app)


def test_health_endpoint() -> None:
    response = _client().get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"


def test_scan_endpoint_returns_expected_shape() -> None:
    payload = {
        "request": {
            "method": "GET",
            "host": "example.com",
            "path": "/api/users/123",
            "query_params": {"email": "alice@example.com"},
            "headers": {"User-Agent": "pytest"},
            "body": None,
            "protocol": "HTTP/1.1",
        }
    }
    response = _client().post("/scan", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "normalized" in data
    assert "serialized" in data
    assert "anomaly_score" in data
    assert data["verdict"] in {"allow", "flag", "block"}
