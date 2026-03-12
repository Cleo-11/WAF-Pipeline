# API Contract

Base URL (local): `http://127.0.0.1:8000`

## `GET /health`
Returns service metadata and liveness.

### Response `200`
```json
{
  "status": "ok",
  "service": "WAF Transformer Prototype",
  "version": "0.1.0",
  "environment": "development"
}
```

## `POST /scan`
Scans one HTTP-like request payload.

### Request Body
```json
{
  "request": {
    "timestamp": "2026-03-12T08:40:00Z",
    "source_ip": "192.168.10.25",
    "method": "GET",
    "scheme": "https",
    "host": "demo.example.com",
    "port": 443,
    "path": "/api/users/123/profile",
    "query_params": {
      "email": "alice@example.com"
    },
    "headers": {
      "User-Agent": "Mozilla/5.0"
    },
    "body": null,
    "protocol": "HTTP/1.1"
  }
}
```

### Response `200`
```json
{
  "normalized": {
    "method": "GET",
    "scheme": "https",
    "host": "demo.example.com",
    "port": 443,
    "path": "/api/users/<INT>/profile",
    "query_params": {
      "email": "<EMAIL>"
    },
    "headers": {
      "user-agent": "Mozilla/5.0"
    },
    "body": null,
    "source_ip": "<IP>",
    "timestamp": "<TIMESTAMP>",
    "protocol": "HTTP/1.1"
  },
  "serialized": "METHOD=GET SCHEME=https HOST=demo.example.com ...",
  "anomaly_score": 0.42,
  "verdict": "allow",
  "triggered_rules": []
}
```

## Notes
- `anomaly_score` currently comes from `StubAnomalyModel`.
- `verdict` is based on score threshold and lightweight heuristic rule triggers.
- Future transformer integration should preserve this contract to avoid frontend/demo breakage.

