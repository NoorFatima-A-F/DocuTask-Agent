"""
Tests for Centralized Structured Logging, Inverted Index Search, and Retention Policies.
"""

from datetime import datetime, timezone, timedelta
import pytest

from app.infrastructure.observability.logs.models import (
    LogLevel,
    LogRecord,
)
from app.infrastructure.observability.logs.ingestion import (
    LogIngestionPipeline,
)
from app.infrastructure.observability.logs.indexing import (
    LogIndex,
)
from app.infrastructure.observability.logs.retention import (
    LogRetentionManager,
    LogRetentionPolicy,
)


def test_log_record_creation_and_redaction():
    record = LogRecord(
        level=LogLevel.ERROR,
        message="Failed auth for user user@domain.com with secret='supersecret'",
        service_name="auth-service",
        tenant_id="tenant-beta",
        trace_id="trace-12345",
    )

    assert record.level == LogLevel.ERROR
    assert "supersecret" not in record.message
    assert "***REDACTED***" in record.message
    assert "user@domain.com" not in record.message
    assert "***@***.***" in record.message


def test_log_index_multi_field_search():
    index = LogIndex()

    r1 = LogRecord(level=LogLevel.INFO, message="Task started", service_name="worker-srv", tenant_id="tenant-1", trace_id="tr-1")
    r2 = LogRecord(level=LogLevel.ERROR, message="Task failed with timeout", service_name="worker-srv", tenant_id="tenant-1", trace_id="tr-1")
    r3 = LogRecord(level=LogLevel.DEBUG, message="Cache hit", service_name="cache-srv", tenant_id="tenant-2", trace_id="tr-2")

    index.index_batch([r1, r2, r3])

    # Search by service
    worker_logs = index.search(service_name="worker-srv")
    assert len(worker_logs) == 2

    # Search by trace
    trace_logs = index.search(trace_id="tr-1")
    assert len(trace_logs) == 2

    # Search by min_level (ERROR)
    error_logs = index.search(min_level=LogLevel.ERROR)
    assert len(error_logs) == 1
    assert error_logs[0].log_id == r2.log_id

    # Search by keyword
    kw_logs = index.search(keyword="timeout")
    assert len(kw_logs) == 1
    assert kw_logs[0].log_id == r2.log_id


def test_log_retention_and_legal_hold():
    mgr = LogRetentionManager(default_retention_days=30)
    now = datetime.now(timezone.utc)

    rec_old = LogRecord(
        timestamp=now - timedelta(days=45),
        level=LogLevel.INFO,
        message="Old log line",
        tenant_id="tenant-3",
    )

    # Normal policy: 45-day old log should not be retained under 30-day policy
    assert not mgr.should_retain(rec_old, now=now)

    # Enable legal hold for tenant-3
    mgr.set_legal_hold("tenant-3", active=True)
    assert mgr.is_under_legal_hold("tenant-3")
    assert mgr.should_retain(rec_old, now=now)  # Retained due to legal hold
