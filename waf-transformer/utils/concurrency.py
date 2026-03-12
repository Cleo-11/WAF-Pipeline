"""Concurrency utilities for non-blocking scan workflows."""

from __future__ import annotations

from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import Any

_EXECUTOR = ThreadPoolExecutor(max_workers=4)


def submit_background(fn: Callable[..., Any], *args: Any, **kwargs: Any):
    """Submit callable to shared threadpool."""
    return _EXECUTOR.submit(fn, *args, **kwargs)
