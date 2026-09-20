"""
Tests for Global Errors, ProblemDetails, Recovery Engine, Resource Management, and Secrets.
"""

import pytest
import asyncio
from datetime import datetime, timezone, timedelta
from app.core.errors.exceptions import PlatformException, DatabasePlatformException
from app.core.errors.error_codes import ErrorCategory, ErrorSeverity, RecoveryPolicy
from app.platform.recovery.engine import RecoveryEngine
from app.platform.resources.manager import ResourceManager, ResourceQuota, ResourceType, QuotaExceededException
from app.infrastructure.secrets.secret_manager import SecretManager


def test_platform_exception_and_problem_details():
    exc = DatabasePlatformException("Connection refused by peer", details={"host": "10.0.0.1"})
    prob = exc.to_problem_details()

    assert prob.status == 500
    assert prob.title == "Database Error"
    assert prob.detail == "Connection refused by peer"
    assert prob.extensions["category"] == ErrorCategory.DATABASE.value


def test_recovery_engine_retry_policy():
    engine = RecoveryEngine()
    attempts = {"count": 0}

    def failing_then_success():
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise RuntimeError("Temporary glitch")
        return "OK"

    exc = PlatformException(
        "Temporary network drop",
        recovery_policy=RecoveryPolicy.RETRY,
        retryable=True,
    )

    action = asyncio.run(engine.execute_recovery(exc, retry_fn=failing_then_success, max_attempts=3))
    assert action.status == "COMPLETED"
    assert action.attempts == 2


def test_resource_manager_quotas_and_isolation():
    rm = ResourceManager()
    quota = ResourceQuota(
        tenant_id="tenant-alpha",
        resource_type=ResourceType.AI_TOKENS,
        limit=1000.0,
    )
    rm.set_quota(quota)

    assert rm.allocate("tenant-alpha", ResourceType.AI_TOKENS, 600.0) is True
    assert rm.get_usage("tenant-alpha", ResourceType.AI_TOKENS) == 600.0

    # Exceed quota
    with pytest.raises(QuotaExceededException):
        rm.allocate("tenant-alpha", ResourceType.AI_TOKENS, 500.0)

    # Release resource
    rm.release("tenant-alpha", ResourceType.AI_TOKENS, 400.0)
    assert rm.get_usage("tenant-alpha", ResourceType.AI_TOKENS) == 200.0


def test_secret_manager_rotation_and_tenant_partitioning():
    sm = SecretManager()
    sm.create_secret("api_key", "secret-value-123", tenant_id="org-1")

    assert sm.get_secret("api_key", tenant_id="org-1") == "secret-value-123"
    assert sm.get_secret("api_key", tenant_id="org-2") is None  # strict isolation

    # Rotate secret
    sm.rotate_secret("api_key", "new-secret-value-456", tenant_id="org-1")
    assert sm.get_secret("api_key", tenant_id="org-1") == "new-secret-value-456"

    # Expire / Revoke
    sm.revoke_secret("api_key", tenant_id="org-1")
    assert sm.get_secret("api_key", tenant_id="org-1") is None
