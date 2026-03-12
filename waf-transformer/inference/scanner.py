"""Main scanning pipeline orchestration."""

from __future__ import annotations

from inference.model_interface import AnomalyModel
from inference.rules import detect_suspicious_markers
from normalization.normalizer import normalize_request
from parsing.schemas import HTTPRequestPayload, ScanResponse
from tokenization.request_serializer import serialize_request


class RequestScanner:
    """End-to-end scanner from raw request payload to verdict."""

    def __init__(
        self,
        model: AnomalyModel,
        score_threshold: float = 0.7,
        suspicious_rule_threshold: int = 1,
    ) -> None:
        self.model = model
        self.score_threshold = score_threshold
        self.suspicious_rule_threshold = suspicious_rule_threshold

    def scan(self, payload: HTTPRequestPayload) -> ScanResponse:
        """
        Scan one request.

        Anomaly score comes only from the model interface.
        Heuristic rules are evaluated separately and only affect verdict.
        """
        normalized = normalize_request(payload)
        serialized = serialize_request(normalized)
        anomaly_score = self.model.score(serialized)
        triggered_rules = detect_suspicious_markers(serialized)

        verdict = "allow"
        if anomaly_score >= self.score_threshold:
            verdict = "block"
        elif len(triggered_rules) >= self.suspicious_rule_threshold:
            verdict = "flag"

        return ScanResponse(
            normalized=normalized,
            serialized=serialized,
            anomaly_score=anomaly_score,
            verdict=verdict,
            triggered_rules=triggered_rules,
        )

