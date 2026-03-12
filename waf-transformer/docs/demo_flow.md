# Demo Flow

## Objective
Demonstrate an end-to-end WAF preprocessing and scanning loop before transformer inference is integrated.

## Prerequisites
- Python 3.11+
- Local dependencies installed (`make install`)

## Demo Steps
1. Start API:
   - `make run`
2. Verify health:
   - `curl http://127.0.0.1:8000/health`
3. Run scan demo request:
   - `python scripts/demo_scan.py`
4. Show normalized output + serialized string + verdict.
5. Optional batch parsing demo:
   - `python scripts/run_batch_ingest.py --file sample_data/sample_apache.log`
6. Optional stream/tailing demo:
   - `python scripts/run_stream_ingest.py --file sample_data/sample_nginx.log`
   - In another terminal, append new log lines and observe parsed output.

## Talking Points for Judges
- Logs and API requests go through the same canonical preprocessing stack.
- Dynamic values are masked to support generalization and reduce overfitting.
- Model boundary is isolated, so a transformer can be plugged in without API or parser rewrites.
- Batch + stream ingestion skeletons are ready for pipeline hardening.

## What Is Deferred
- Transformer architecture and tokenizer integration.
- Training pipeline and incremental fine-tuning implementation.
- Live inline reverse-proxy/sidecar enforcement mode.

