"""File watcher helpers for local streaming demos."""

from __future__ import annotations

import time
from collections.abc import Callable
from pathlib import Path


def watch_for_growth(
    path: str | Path,
    on_change: Callable[[Path], None],
    interval: float = 1.0,
) -> None:
    """
    Call callback whenever a file size changes.

    TODO: Replace with cross-platform FS event backend for production use.
    """
    file_path = Path(path)
    last_size = file_path.stat().st_size if file_path.exists() else 0
    while True:
        if file_path.exists():
            current_size = file_path.stat().st_size
            if current_size != last_size:
                on_change(file_path)
                last_size = current_size
        time.sleep(interval)
