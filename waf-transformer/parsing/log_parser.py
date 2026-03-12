"""Parsers for Apache/Nginx common access log formats."""

from __future__ import annotations

import re
from collections.abc import Iterable

from parsing.schemas import AccessLogEntry

_COMMON_LOG_REGEX = re.compile(
    r'^(?P<remote_addr>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] '
    r'"(?P<request>[^"]*)" (?P<status>\d{3}) (?P<bytes_sent>\S+) '
    r'"(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"$'
)


def _parse_request_line(request_line: str) -> tuple[str, str, str]:
    parts = request_line.split()
    if len(parts) != 3:
        return "UNKNOWN", "/", "HTTP/1.1"
    return parts[0], parts[1], parts[2]


def parse_access_log_line(line: str) -> AccessLogEntry | None:
    """Parse one Apache/Nginx access log line into a structured model."""
    match = _COMMON_LOG_REGEX.match(line.strip())
    if not match:
        return None

    method, path, protocol = _parse_request_line(match.group("request"))
    bytes_raw = match.group("bytes_sent")
    bytes_sent = int(bytes_raw) if bytes_raw.isdigit() else 0

    return AccessLogEntry(
        remote_addr=match.group("remote_addr"),
        timestamp_raw=match.group("timestamp"),
        method=method,
        path=path,
        protocol=protocol,
        status=int(match.group("status")),
        bytes_sent=bytes_sent,
        referer=None if match.group("referer") == "-" else match.group("referer"),
        user_agent=None if match.group("user_agent") == "-" else match.group("user_agent"),
    )


def parse_access_log_lines(lines: Iterable[str]) -> list[AccessLogEntry]:
    """Parse multiple log lines, skipping malformed records."""
    parsed: list[AccessLogEntry] = []
    for line in lines:
        entry = parse_access_log_line(line)
        if entry:
            parsed.append(entry)
    return parsed
