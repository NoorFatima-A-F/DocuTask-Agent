"""Tests for Resilience, Circuit Breakers, and Exponential Retries."""

from app.networking.mesh.data_plane import MeshRequest, MeshResponse
from app.networking.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitState,
)
from app.networking.resilience.retry import (
    BackoffStrategy,
    RetryPolicy,
    RetryPolicyEngine,
)


def test_retry_engine_transient_failure_recovery():
    policy = RetryPolicy(
        max_attempts=3,
        initial_backoff_ms=5.0,
        retryable_status_codes={503},
        backoff_strategy=BackoffStrategy.FIXED,
    )
    engine = RetryPolicyEngine(default_policy=policy)

    req = MeshRequest(source_service="client", target_service="worker", action="job")
    attempts = 0

    def mock_flaky_service(r: MeshRequest) -> MeshResponse:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            return MeshResponse(status_code=503, error_message="Temporary outage")
        return MeshResponse(status_code=200, payload={"success": True})

    res = engine.execute_with_retry(req, mock_flaky_service, policy=policy)
    assert res.status_code == 200
    assert attempts == 3


def test_circuit_breaker_state_transitions():
    cfg = CircuitBreakerConfig(
        failure_rate_threshold_pct=50.0,
        sliding_window_size=4,
        minimum_number_of_calls=4,
        wait_duration_in_open_seconds=0.1,  # Short wait for testing
        permitted_calls_in_half_open=2,
    )
    cb = CircuitBreaker(service_name="flaky-service", config=cfg)
    assert cb.state == CircuitState.CLOSED
    assert cb.can_execute() is True

    # Record 4 calls: 2 failures, 2 successes (50% failure rate)
    cb.record_result(is_failure=True)
    cb.record_result(is_failure=True)
    cb.record_result(is_failure=False)
    cb.record_result(is_failure=False)

    # State should now be OPEN
    assert cb.state == CircuitState.OPEN
    assert cb.can_execute() is False

    # Wait for wait duration to expire
    import time
    time.sleep(0.15)

    # Should transition to HALF_OPEN upon next can_execute call
    assert cb.can_execute() is True
    assert cb.state == CircuitState.HALF_OPEN

    # In HALF_OPEN, record 2 successes -> should close
    cb.record_result(is_failure=False)
    cb.record_result(is_failure=False)
    assert cb.state == CircuitState.CLOSED
