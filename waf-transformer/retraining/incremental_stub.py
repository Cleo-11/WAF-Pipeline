"""Incremental retraining integration stub."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class RetrainingEvent:
    """Represents future training trigger metadata."""

    source: str
    reason: str
    created_at: datetime


def create_incremental_event(source: str, reason: str) -> RetrainingEvent:
    """
    Build retraining event object.

    TODO: Emit this event to a durable queue/workflow engine.
    """
    return RetrainingEvent(source=source, reason=reason, created_at=datetime.now(datetime.UTC))
