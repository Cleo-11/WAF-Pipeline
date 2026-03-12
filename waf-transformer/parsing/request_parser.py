"""Convert parsed log entries into scanner request payloads."""

from __future__ import annotations

from urllib.parse import parse_qsl, urlsplit

from parsing.schemas import AccessLogEntry, HTTPRequestPayload


def from_access_log(entry: AccessLogEntry) -> HTTPRequestPayload:
    """Build scanner request payload from a parsed access log entry."""
    split = urlsplit(entry.path)
    return HTTPRequestPayload(
        source_ip=entry.remote_addr,
        method=entry.method,
        path=split.path or "/",
        query_params=dict(parse_qsl(split.query, keep_blank_values=True)),
        headers={"user-agent": entry.user_agent or "", "referer": entry.referer or ""},
        protocol=entry.protocol,
    )

