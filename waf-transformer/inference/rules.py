"""Heuristic rules used alongside model score for early demos."""

from __future__ import annotations

SUSPICIOUS_MARKERS: tuple[str, ...] = (
    "union select",
    "<script",
    "../",
    "or 1=1",
    "cmd=",
    "drop table",
)


def detect_suspicious_markers(serialized_request: str) -> list[str]:
    """Return a list of triggered lightweight heuristic rule names."""
    lower = serialized_request.lower()
    triggered: list[str] = []
    for marker in SUSPICIOUS_MARKERS:
        if marker in lower:
            triggered.append(f"marker:{marker}")
    return triggered

