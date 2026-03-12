# Transformer-based End-to-End WAF Pipeline (Prototype)

## Problem Statement
Traditional WAF systems are mostly rule-based and miss novel attack patterns. This project sets up a clean, transformer-ready pipeline that ingests logs, parses requests, normalizes dynamic values, serializes requests into canonical strings, and exposes a real-time scanning API.

## Current Scope (Prototype v1)
Implemented now:
- FastAPI service with `GET /health` and `POST /scan`
- Pydantic request/response schemas
- Structured JSON logging
- Batch and streaming log ingestion skeletons
- Apache/Nginx access log parser
- Request normalization for dynamic values:
  - integers/IDs
  - UUID-like tokens
  - timestamps
  - long hex strings
  - email addresses
  - IP addresses
- Canonical request serializer for future tokenizer/model input
- Isolated model interface with stub anomaly model
- Heuristic rules layer (separate from model score path)
- Unit tests for parser, normalizer, and scanner API
- Docker + docker-compose for local development

Intentionally deferred:
- Transformer architecture and training pipeline
- Real tokenizer integration (BPE/WordPiece/etc.)
- Incremental retraining jobs/workflows
- Reverse-proxy sidecar integration in live traffic path

## Repository Structure
```text
waf-transformer/
  app/
  ingestion/
  parsing/
  normalization/
  tokenization/
  inference/
  retraining/
  utils/
  tests/
  scripts/
  sample_data/
  docs/
```

## Quick Start
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   make install
   ```
3. Run API:
   ```bash
   make run
   ```
4. Verify health:
   ```bash
   curl http://127.0.0.1:8000/health
   ```

## Run Tests
```bash
make test
```

## Run Demos
Batch ingestion:
```bash
python scripts/run_batch_ingest.py --file sample_data/sample_apache.log
```

Streaming ingestion:
```bash
python scripts/run_stream_ingest.py --file sample_data/sample_nginx.log
```

Scan API demo:
```bash
python scripts/demo_scan.py
```

## Sample Scan Payload
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

## What `/scan` Returns
- `normalized`: Structured normalized request
- `serialized`: Canonical string for tokenizer/model input
- `anomaly_score`: Placeholder score from isolated model interface
- `verdict`: `allow | flag | block`
- `triggered_rules`: Trivial heuristic hits for demo visibility

## Next Milestones
1. Replace `StubAnomalyModel` with transformer inference wrapper.
2. Replace tokenizer stub with real tokenizer artifacts.
3. Add dataset writer for normalized + serialized training examples.
4. Add retraining trigger queue and job runner.
5. Integrate with reverse-proxy or sidecar for live request interception.

