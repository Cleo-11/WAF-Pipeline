"""Pydantic schemas shared across API, parsing, and inference layers."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class HTTPRequestPayload(BaseModel):
    """HTTP-like request structure accepted by the scanner."""

    timestamp: datetime | None = None
    source_ip: str | None = None
    method: str
    scheme: str = "http"
    host: str = "localhost"
    port: int | None = None
    path: str
    query_params: dict[str, Any] = Field(default_factory=dict)
    headers: dict[str, str] = Field(default_factory=dict)
    body: str | None = None
    protocol: str = "HTTP/1.1"


class NormalizedRequest(BaseModel):
    """Normalized request preserving semantic structure."""

    method: str
    scheme: str
    host: str
    port: int | None = None
    path: str
    query_params: dict[str, str] = Field(default_factory=dict)
    headers: dict[str, str] = Field(default_factory=dict)
    body: str | None = None
    source_ip: str | None = None
    timestamp: str | None = None
    protocol: str


class ScanRequest(BaseModel):
    """API contract for /scan endpoint input."""

    request: HTTPRequestPayload


class ScanResponse(BaseModel):
    """API contract for /scan endpoint output."""

    normalized: NormalizedRequest
    serialized: str
    anomaly_score: float
    verdict: Literal["allow", "flag", "block"]
    triggered_rules: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    """Response model for /health endpoint."""

    status: Literal["ok"]
    service: str
    version: str
    environment: str


class AccessLogEntry(BaseModel):
    """Minimal structured representation of a parsed log entry."""

    remote_addr: str
    timestamp_raw: str
    method: str
    path: str
    protocol: str
    status: int
    bytes_sent: int
    referer: str | None = None
    user_agent: str | None = None

