"""Tests for Structured Logger, JSON Formatter, and Storage Queries."""

from app.observability.core.context import ObservabilityContext
from app.observability.logging.formatter import JSONLogFormatter
from app.observability.logging.logger import StructuredLogger
from app.observability.logging.storage import LogStorageBackend


def test_json_formatter_masking():
    formatter = JSONLogFormatter(mask_pii=True)
    ctx = ObservabilityContext(tenant_id="tenant-acme", service_name="payment-svc")
    extra = {"api_key": "sk-12345SECRET", "user_email": "user@example.com"}

    rec = formatter.format("INFO", "Processing payment", ctx, extra)
    assert rec["level"] == "INFO"
    assert rec["service"] == "payment-svc"
    assert rec["metadata"]["api_key"] == "******[MASKED]******"
    assert rec["metadata"]["user_email"] == "user@example.com"


def test_structured_logger_and_storage_search():
    storage = LogStorageBackend()
    logger = StructuredLogger(service_name="auth-service", storage=storage)

    ctx = ObservabilityContext(tenant_id="tenant-1", trace_id="trace-xyz")
    logger.info("User login successful", context=ctx, user_id="user-1")
    logger.error("Invalid credentials provided", context=ctx, user_id="user-2")

    # Search by service
    results = storage.search(service="auth-service")
    assert len(results) == 2

    # Search by level
    errors = storage.search(service="auth-service", level="ERROR")
    assert len(errors) == 1
    assert "Invalid credentials" in errors[0].message

    # Search by query
    query_res = storage.search(query="login")
    assert len(query_res) == 1
