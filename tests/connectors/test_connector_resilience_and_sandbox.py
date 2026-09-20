"""
Tests for ConnectorRetryEngine, CircuitBreaker, RateLimiter, ConnectorSandbox, and ConnectorPolicyEngine.
"""

import time
import pytest
from app.connectors.core.exceptions import (
    CircuitBreakerOpenError,
    PolicyViolationError,
    RateLimitExceededError,
    SandboxViolationError,
)
from app.connectors.core.models import (
    ActionDescriptor,
    Connector,
    ConnectorCategory,
    ConnectorPolicyRule,
)
from app.connectors.policies.policy_engine import ConnectorPolicyEngine
from app.connectors.resilience.circuit_breaker import CircuitBreaker, CircuitBreakerConfig, CircuitState
from app.connectors.resilience.rate_limiter import RateLimiter, RateLimitPolicy
from app.connectors.resilience.retry_engine import (
    ConnectorFailureCategory,
    ConnectorRetryEngine,
    RetryPolicy,
)
from app.connectors.sandbox.sandbox import ConnectorSandbox, SandboxConfig


def test_retry_engine_classification_and_backoff():
    engine = ConnectorRetryEngine()

    assert engine.classify_error("HTTP 429 Too Many Requests") == ConnectorFailureCategory.RATE_LIMIT
    assert engine.classify_error("HTTP 401 Unauthorized token") == ConnectorFailureCategory.AUTHENTICATION
    assert engine.classify_error("503 Service Unavailable") == ConnectorFailureCategory.TEMPORARY
    assert engine.classify_error("Connection timed out on socket") == ConnectorFailureCategory.NETWORK

    # Backoff calculation
    pol = RetryPolicy(initial_interval_seconds=1.0, backoff_multiplier=2.0, jitter=False)
    assert engine.calculate_delay(1, pol) == 1.0
    assert engine.calculate_delay(2, pol) == 2.0
    assert engine.calculate_delay(3, pol) == 4.0


def test_circuit_breaker_trip_and_recovery():
    config = CircuitBreakerConfig(
        failure_threshold=2,
        recovery_timeout_seconds=0.1,
        half_open_success_threshold=1,
    )
    cb = CircuitBreaker("test-breaker", config)

    assert cb.state == CircuitState.CLOSED
    assert cb.allow_request() is True

    # 1st failure
    cb.record_failure(Exception("Timeout 1"))
    assert cb.state == CircuitState.CLOSED

    # 2nd failure -> Trips to OPEN
    cb.record_failure(Exception("Timeout 2"))
    assert cb.state == CircuitState.OPEN
    assert cb.allow_request() is False

    # Calling through tripped breaker fails fast
    with pytest.raises(CircuitBreakerOpenError):
        cb.call(lambda: "never_executed")

    # Wait for recovery timeout
    time.sleep(0.15)
    assert cb.allow_request() is True  # Enters HALF_OPEN

    # Successful probe resets to CLOSED
    cb.record_success()
    assert cb.state == CircuitState.CLOSED


def test_rate_limiter_token_bucket():
    limiter = RateLimiter(
        default_policy=RateLimitPolicy(
            rate_limit_rps=5.0,
            burst_capacity=2.0,
        )
    )

    key = "org-test:ws-test:conn-api"

    # Consume 2 tokens (full burst capacity)
    limiter.acquire(key, 1.0)
    limiter.acquire(key, 1.0)

    # 3rd token immediately exceeds limit
    with pytest.raises(RateLimitExceededError) as exc_info:
        limiter.acquire(key, 1.0)

    assert exc_info.value.retry_after_seconds > 0


def test_connector_sandbox_enforcement():
    sandbox = ConnectorSandbox(
        config=SandboxConfig(
            max_payload_size_bytes=100,
            disallowed_domains=["malicious-exfiltration.com"],
        )
    )

    # Large payload violation
    large_data = {"data": "x" * 200}
    with pytest.raises(SandboxViolationError):
        sandbox.validate_payload_size(large_data)

    # Blocked domain violation
    with pytest.raises(SandboxViolationError):
        sandbox.validate_network_target("https://malicious-exfiltration.com/api/steal")


def test_connector_policy_engine():
    policy_engine = ConnectorPolicyEngine(
        default_policy=ConnectorPolicyRule(
            disallowed_connectors=["conn-untrusted-script"],
            allowed_regions=["us-east-1", "eu-west-1"],
            disallowed_data_tags=["PCI_CREDIT_CARD", "SECRET"],
            max_cost_per_call_usd=0.10,
            require_approval_above_cost_usd=0.05,
        )
    )

    allowed_conn = Connector(
        id="conn-authorized-email",
        name="Email",
        vendor="Google",
        category=ConnectorCategory.COMMUNICATION,
    )

    cheap_action = ActionDescriptor(name="send", connector_id="conn-authorized-email", capability="email.send", cost_usd=0.01)
    expensive_action = ActionDescriptor(name="bulk_send", connector_id="conn-authorized-email", capability="email.send", cost_usd=0.08)

    # 1. Valid execution
    res1 = policy_engine.evaluate(allowed_conn, cheap_action, {}, region="us-east-1")
    assert res1.allowed is True
    assert res1.requires_human_approval is False

    # 2. Requires approval due to cost > 0.05
    res2 = policy_engine.evaluate(allowed_conn, expensive_action, {}, region="us-east-1")
    assert res2.allowed is True
    assert res2.requires_human_approval is True

    # 3. Disallowed region
    res3 = policy_engine.evaluate(allowed_conn, cheap_action, {}, region="ap-southeast-1")
    assert res3.allowed is False

    # 4. Disallowed data tag
    res4 = policy_engine.evaluate(allowed_conn, cheap_action, {}, region="us-east-1", data_tags=["PCI_CREDIT_CARD"])
    assert res4.allowed is False
