"""Batch log ingestion helpers."""

from __future__ import annotations

from pathlib import Path

from parsing.log_parser import parse_access_log_lines
from parsing.schemas import AccessLogEntry


def load_batch_log(path: str | Path) -> list[AccessLogEntry]:
    """Load and parse a complete log file in batch mode."""
    file_path = Path(path)
    lines = file_path.read_text(encoding="utf-8").splitlines()
    return parse_access_log_lines(lines)

