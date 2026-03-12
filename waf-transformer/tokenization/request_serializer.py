"""Serializer for normalized requests into canonical model input text."""

from __future__ import annotations

from parsing.schemas import NormalizedRequest


def serialize_request(normalized: NormalizedRequest) -> str:
    """Serialize normalized request into deterministic string representation."""
    query_string = "&".join(f"{k}={v}" for k, v in normalized.query_params.items()) or "-"
    header_string = ";".join(f"{k}:{v}" for k, v in normalized.headers.items()) or "-"
    body_string = normalized.body or "-"
    source = normalized.source_ip or "-"
    ts = normalized.timestamp or "-"

    return (
        f"METHOD={normalized.method} "
        f"SCHEME={normalized.scheme} "
        f"HOST={normalized.host} "
        f"PORT={normalized.port if normalized.port is not None else '-'} "
        f"PATH={normalized.path} "
        f"QUERY={query_string} "
        f"HEADERS={header_string} "
        f"BODY={body_string} "
        f"SRC_IP={source} "
        f"TS={ts} "
        f"PROTO={normalized.protocol}"
    )

