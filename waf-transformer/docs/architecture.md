# Architecture

## Goal
Build a modular, transformer-ready Web Application Firewall pipeline with clear boundaries between ingestion, preprocessing, serialization, and inference.

## Module Layout
- `app/`: FastAPI service, runtime config, structured logging setup.
- `ingestion/`: Batch and streaming log input skeletons.
- `parsing/`: Access log parsing + request schema mapping.
- `normalization/`: Dynamic value masking and canonical normalization.
- `tokenization/`: Deterministic request serialization and tokenizer stub.
- `inference/`: Scanner orchestration, model interface, heuristic rules.
- `retraining/`: Incremental retraining trigger stubs.
- `utils/`: Shared helpers (I/O, paths, concurrency).

## Request Flow (`/scan`)
1. API receives `ScanRequest` with HTTP-like payload.
2. `RequestScanner` calls `normalize_request`.
3. `serialize_request` builds canonical text for model input.
4. `AnomalyModel.score` (currently `StubAnomalyModel`) returns anomaly score.
5. Heuristic markers are evaluated independently for demo-time flagging.
6. API returns:
   - normalized request object
   - serialized model-ready string
   - model anomaly score
   - verdict + triggered rules

## Ingestion Flows
### Batch
`ingestion.batch_loader.load_batch_log` reads full files and parses every line.

### Streaming
`ingestion.stream_loader.tail_file` tails a growing log file for near-real-time demos.

## Integration Points for Transformer
- Replace `inference.model_interface.StubAnomalyModel` with transformer inference adapter.
- Replace `tokenization.tokenizer_stub.TokenizerStub` with production tokenizer.
- Add feature store / training dataset writer after normalization + serialization.
- Extend `retraining.incremental_stub` to push job events to scheduler/queue.

## Concurrency Model (Current)
- API is async-capable via FastAPI.
- `utils.concurrency.submit_background` offers a simple threadpool for non-blocking side tasks.
- Future production deployments can introduce queue-based fanout and worker pools.

