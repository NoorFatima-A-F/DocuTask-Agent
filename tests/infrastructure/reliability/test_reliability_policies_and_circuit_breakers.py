"""
Tests for Reliability Policies, Circuit Breakers, 5 Retry Strategies, and Bulkheads.
"""

import asyncio
import time
import pytest

from app.infrastructure.reliability.models import (
    BulkheadConfig,
    CircuitBreakerConfig,
    CircuitBreakerState,
    ReliabilityPolicy,
    RetryPolicyConfig,
    RetryStrategy,
)
from app.infrastructure.reliability.policies import (
    Bulkhead,
    CircuitBreaker,
    CircuitBreakerOpenError,
    ReliabilityPolicyEngine,
    RetryEngine,
)


def test_circuit_breaker_lifecycle():
    cfg = CircuitBreakerConfig(
        failure_threshold=3,
        recovery_timeout_seconds=0.1,  # Short timeout for test
        half_open_success_threshold=2,
        half_open_max_requests=2,
    )
    cb = CircuitBreaker(name="test-breaker", config=cfg)

    assert cb.state == CircuitBreakerState.CLOSED

    # Record 2 failures (under threshold)
    cb.before_call()
    cb.on_failure(ValueError("err 1"))
    cb.before_call()
    cb.on_failure(ValueError("err 2"))
    assert cb.state == CircuitBreakerState.CLOSED

    # 3rd failure trips the breaker to OPEN
    cb.before_call()
    cb.on_failure(ValueError("err 3"))
    assert cb.state == CircuitBreakerState.OPEN

    # Calls while OPEN should be rejected
    with pytest.raises(CircuitBreakerOpenError):
        cb.before_call()

    # Wait for cooldown
    time.sleep(0.12)
    assert cb.state == CircuitBreakerState.HALF_OPEN

    # In HALF_OPEN: 2 consecutive successes should close the breaker
    cb.before_call()
    cb.on_success()
    assert cb.state == CircuitBreakerState.HALF_OPEN

    cb.before_call()
    cb.on_success()
    assert cb.state == CircuitBreakerState.CLOSED


def test_retry_engine_strategies():
    cfg_immediate = RetryPolicyConfig(strategy=RetryStrategy.IMMEDIATE)
    assert RetryEngine.calculate_delay(0, cfg_immediate) == 0.0
    assert RetryEngine.calculate_delay(2, cfg_immediate) == 0.0

    cfg_linear = RetryPolicyConfig(strategy=RetryStrategy.LINEAR, initial_interval_seconds=1.0)
    assert RetryEngine.calculate_delay(0, cfg_linear) == 1.0
    assert RetryEngine.calculate_delay(1, cfg_linear) == 2.0
    assert RetryEngine.calculate_delay(2, cfg_linear) == 3.0

    cfg_exponential = RetryPolicyConfig(
        strategy=RetryStrategy.EXPONENTIAL,
        initial_interval_seconds=1.0,
        backoff_multiplier=2.0,
        max_interval_seconds=10.0,
    )
    assert RetryEngine.calculate_delay(0, cfg_exponential) == 1.0
    assert RetryEngine.calculate_delay(1, cfg_exponential) == 2.0
    assert RetryEngine.calculate_delay(2, cfg_exponential) == 4.0

    cfg_jitter = RetryPolicyConfig(
        strategy=RetryStrategy.RANDOMIZED_JITTER,
        initial_interval_seconds=1.0,
        backoff_multiplier=2.0,
        jitter_factor=0.2,
    )
    delay = RetryEngine.calculate_delay(1, cfg_jitter)
    assert 1.5 <= delay <= 2.5

    cfg_adaptive = RetryPolicyConfig(
        strategy=RetryStrategy.ADAPTIVE,
        initial_interval_seconds=1.0,
        backoff_multiplier=2.0,
        jitter_factor=0.1,
    )
    adaptive_delay = RetryEngine.calculate_delay(1, cfg_adaptive, consecutive_errors=5)
    assert adaptive_delay > 2.0


def test_bulkhead_concurrency():
    cfg = BulkheadConfig(max_concurrent_calls=2, max_wait_queue_size=1)
    bulkhead = Bulkhead("test-bulkhead", cfg)

    assert bulkhead.acquire()  # call 1
    assert bulkhead.acquire()  # call 2
    assert bulkhead.acquire()  # call 3 in queue
    assert not bulkhead.acquire()  # Rejected (exceeded capacity + queue)

    bulkhead.release()
    assert bulkhead.acquire()


def test_policy_engine_execute_sync_success_and_fallback():
    engine = ReliabilityPolicyEngine()
    policy = ReliabilityPolicy(
        policy_id="pol-1",
        name="Test Policy",
        retry_policy=RetryPolicyConfig(strategy=RetryStrategy.IMMEDIATE, max_retries=2),
        fallback_enabled=True,
    )

    # Success case
    def healthy_op(x, y):
        return x + y

    res = engine.execute_sync("math-service", healthy_op, policy=policy, fallback_fn=None, x=10, y=20)
    assert res == 30

    # Failure with fallback
    def failing_op():
        raise ConnectionError("Service unreachable")

    def fallback_op():
        return "cached_response"

    res_fallback = engine.execute_sync("math-service-failing", failing_op, policy=policy, fallback_fn=fallback_op)
    assert res_fallback == "cached_response"


@pytest.mark.anyio
async def test_policy_engine_execute_async_with_timeout():
    engine = ReliabilityPolicyEngine()
    policy = ReliabilityPolicy(
        policy_id="pol-async",
        name="Async Timeout Policy",
        timeout_budget_seconds=0.1,
        retry_policy=RetryPolicyConfig(strategy=RetryStrategy.IMMEDIATE, max_retries=1),
        fallback_enabled=True,
    )

    async def slow_async_op():
        await asyncio.sleep(0.3)
        return "never_reached"

    async def fallback_async_op():
        return "fallback_result"

    res = await engine.execute_async("slow-service", slow_async_op, policy=policy, fallback_fn=fallback_async_op)
    assert res == "fallback_result"
