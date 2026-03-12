"""Request normalization utilities."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from normalization.patterns import REPLACEMENTS
from parsing.schemas import HTTPRequestPayload, NormalizedRequest


def normalize_text(value: str) -> str:
    """Normalize dynamic tokens while preserving structural text."""
    normalized = value
    for pattern, token in REPLACEMENTS:
        normalized = pattern.sub(token, normalized)
    return normalized


def _normalize_value(value: Any) -> str:
    if value is None:
        return "<NULL>"
    return normalize_text(str(value))


def _normalize_timestamp(ts: datetime | None) -> str | None:
    if ts is None:
        return None
    return "<TIMESTAMP>"


def normalize_request(payload: HTTPRequestPayload) -> NormalizedRequest:
    """Normalize request payload into canonical structured form."""
    headers = {
        key.lower().strip(): _normalize_value(val).strip()
        for key, val in sorted(payload.headers.items(), key=lambda item: item[0].lower())
        if key and val is not None
    }
    query_params = {
        str(key): _normalize_value(val)
        for key, val in sorted(payload.query_params.items(), key=lambda item: str(item[0]))
    }

    return NormalizedRequest(
        method=payload.method.upper(),
        scheme=payload.scheme.lower(),
        host=normalize_text(payload.host.lower()),
        port=payload.port,
        path=normalize_text(payload.path),
        query_params=query_params,
        headers=headers,
        body=normalize_text(payload.body) if payload.body else None,
        source_ip=normalize_text(payload.source_ip) if payload.source_ip else None,
        timestamp=_normalize_timestamp(payload.timestamp),
        protocol=payload.protocol.upper(),
    )

