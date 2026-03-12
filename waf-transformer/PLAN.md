# Hackathon Execution Plan

## Objective
Deliver a credible end-to-end WAF prototype that demonstrates real-time request scanning and clean upgrade paths to transformer-based detection.

## Scope for Prototype v1
- Build modular preprocessing + inference skeleton.
- Support Apache/Nginx log ingestion (batch + streaming tail).
- Expose stable scanning API for live demo.
- Keep model/tokenizer as well-defined stubs only.
- Add tests and docs so team can parallelize confidently.

## Phased Roadmap
### Phase 1: Foundations (Day 1)
- Finalize repository structure and coding conventions.
- Implement parser, normalizer, serializer, scan API.
- Add sample data and baseline tests.

### Phase 2: Demo Reliability (Day 2)
- Harden logging, error handling, and scripts.
- Validate batch/stream demos with sample logs.
- Prepare API demo script and judge-facing walkthrough.

### Phase 3: Transformer Integration (Day 3+)
- Implement tokenizer and model loading wrappers.
- Add offline evaluation scripts and metrics.
- Tune thresholding and add explainability metadata.

### Phase 4: Retraining Path (Stretch)
- Define incremental data capture contract.
- Build retraining trigger + job orchestration.
- Add model versioning and rollback strategy.

## Module Ownership Suggestions
- `ingestion/`, `parsing/`: Data engineering lead.
- `normalization/`, `tokenization/`: NLP/feature engineer.
- `inference/`, `app/`: Backend/API engineer.
- `retraining/`, `scripts/`: MLOps engineer.
- `docs/`, demo packaging: Team lead/shared.

## Risks
- Over-investing in model training before pipeline is stable.
- Inconsistent request canonicalization between training and inference.
- Demo breakage due to environment/setup friction.
- Threshold tuning uncertainty without representative benign/malicious data.

## Demo Strategy
- Show `/health` and `/scan` API behavior live.
- Feed benign and malicious-style payloads; compare verdicts.
- Show batch parse output from Apache logs.
- Show stream tailing simulation and real-time parse.
- Explain model boundary where transformer drops in next.

## Success Criteria
- Team can run project locally in under 10 minutes.
- `/scan` returns deterministic normalized + serialized output.
- Parser/normalizer/API tests pass.
- Clear evidence of extensibility toward transformer integration.
- Demo flow remains stable on multiple machines.

## Deferred Items
- Transformer architecture implementation/training loop.
- Feature store and embedding management.
- High-throughput async workers and distributed queues.
- Full production reverse-proxy enforcement mode.

