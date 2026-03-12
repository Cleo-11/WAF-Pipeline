"""Regex patterns for dynamic value normalization."""

from __future__ import annotations

import re

UUID_PATTERN = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"
)
TIMESTAMP_PATTERN = re.compile(r"\b\d{4}-\d{2}-\d{2}[T ][0-9:.+-Z]{2,}\b")
LONG_HEX_PATTERN = re.compile(r"\b[0-9a-fA-F]{16,}\b")
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
IPV4_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
INT_PATTERN = re.compile(r"\b\d+\b")

REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (UUID_PATTERN, "<UUID>"),
    (TIMESTAMP_PATTERN, "<TIMESTAMP>"),
    (LONG_HEX_PATTERN, "<HEX>"),
    (EMAIL_PATTERN, "<EMAIL>"),
    (IPV4_PATTERN, "<IP>"),
    (INT_PATTERN, "<INT>"),
]
