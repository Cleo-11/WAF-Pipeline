"""Model interface layer isolated from scanner orchestration."""

from __future__ import annotations

from abc import ABC, abstractmethod


class AnomalyModel(ABC):
    """Abstraction for anomaly scoring models."""

    @abstractmethod
    def score(self, serialized_request: str) -> float:
        """Return anomaly score in range [0.0, 1.0]."""


class StubAnomalyModel(AnomalyModel):
    """
    Minimal placeholder model for current prototype stage.

    TODO: Replace with transformer-backed inference implementation.
    """

    def score(self, serialized_request: str) -> float:
        # Stable deterministic score from payload length.
        raw = len(serialized_request) % 100
        return round(raw / 100.0, 3)

