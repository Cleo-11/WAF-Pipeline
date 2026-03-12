"""FastAPI entrypoint for the WAF scanning service."""

from __future__ import annotations

import logging

from fastapi import FastAPI

from app.config import get_settings
from app.logging_config import configure_logging
from inference.model_interface import StubAnomalyModel
from inference.scanner import RequestScanner
from parsing.schemas import HealthResponse, ScanRequest, ScanResponse

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name, version=settings.app_version)
scanner = RequestScanner(
    model=StubAnomalyModel(),
    score_threshold=settings.scanner_threshold,
    suspicious_rule_threshold=settings.suspicious_rule_threshold,
)


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    """Health check endpoint for liveness and metadata."""
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )


@app.post("/scan", response_model=ScanResponse, tags=["scanner"])
def scan(payload: ScanRequest) -> ScanResponse:
    """Normalize and scan an HTTP-like request payload."""
    result = scanner.scan(payload.request)
    logger.info("scan_completed verdict=%s score=%.3f", result.verdict, result.anomaly_score)
    return result

