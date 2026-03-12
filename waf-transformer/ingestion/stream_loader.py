"""Streaming/tailing log ingestion skeleton."""

from __future__ import annotations

import time
from collections.abc import Iterator
from pathlib import Path


def tail_file(path: str | Path, poll_interval_seconds: float = 0.5) -> Iterator[str]:
    """
    Yield appended lines from a growing log file.

    TODO: Replace polling with event-driven source (Kafka, Fluent Bit, socket, etc.).
    """
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as handle:
        handle.seek(0, 2)
        while True:
            line = handle.readline()
            if line:
                yield line.rstrip("\n")
            else:
                time.sleep(poll_interval_seconds)

