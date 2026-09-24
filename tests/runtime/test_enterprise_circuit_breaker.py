"""
Enterprise Circuit Breaker Test Suite.
Validates:
- Normal execution in CLOSED state
- Threshold tripping into OPEN state
- Instant rejection with CircuitBreakerOpenError when OPEN
- Recovery timeout transition into HALF_OPEN state
- Successful probe requests resetting breaker back to CLOSED
- Probe failure tripping back to OPEN immediately
"""

import asyncio
import pytest
from app.agents.runtime.enterprise.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerOpenError,
    CircuitState,
)


@pytest.mark.asyncio
async def test_circuit_breaker_normal_closed_flow():
    cb = CircuitBreaker("test_breaker", failure_threshold=2)
    assert cb.state == CircuitState.CLOSED

    async def successful_call():
        return "ok"

    res = await cb.execute(successful_call)
    assert res == "ok"
    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 0


@pytest.mark.asyncio
async def test_circuit_breaker_trips_to_open():
    cb = CircuitBreaker("test_breaker", failure_threshold=2, recovery_timeout_seconds=0.1)

    async def failing_call():
        raise ValueError("Service down")

    # 1st failure
    with pytest.raises(ValueError):
        await cb.execute(failing_call)
    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 1

    # 2nd failure -> reaches threshold -> trips to OPEN
    with pytest.raises(ValueError):
        await cb.execute(failing_call)
    assert cb.state == CircuitState.OPEN

    # Subsequent call immediately rejected with CircuitBreakerOpenError
    called = False

    async def probe():
        nonlocal called
        called = True

    with pytest.raises(CircuitBreakerOpenError) as exc_info:
        await cb.execute(probe)
    assert not called
    assert "is OPEN. Request rejected" in str(exc_info.value)


@pytest.mark.asyncio
async def test_circuit_breaker_recovery_to_closed():
    cb = CircuitBreaker(
        "test_breaker",
        failure_threshold=1,
        recovery_timeout_seconds=0.05,
        success_threshold=2,
    )

    async def failing_call():
        raise RuntimeError("boom")

    # Trip to OPEN
    with pytest.raises(RuntimeError):
        await cb.execute(failing_call)
    assert cb.state == CircuitState.OPEN

    # Wait for recovery timeout
    await asyncio.sleep(0.06)

    # 1st success in HALF_OPEN
    async def good_call():
        return "healthy"

    res1 = await cb.execute(good_call)
    assert res1 == "healthy"
    assert cb.state == CircuitState.HALF_OPEN
    assert cb.success_count == 1

    # 2nd success -> meets threshold (2) -> recovers to CLOSED
    res2 = await cb.execute(good_call)
    assert res2 == "healthy"
    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 0


@pytest.mark.asyncio
async def test_circuit_breaker_half_open_failure_re_trips():
    cb = CircuitBreaker(
        "test_breaker",
        failure_threshold=1,
        recovery_timeout_seconds=0.05,
        success_threshold=2,
    )

    async def failing_call():
        raise RuntimeError("down")

    with pytest.raises(RuntimeError):
        await cb.execute(failing_call)
    assert cb.state == CircuitState.OPEN

    await asyncio.sleep(0.06)

    # In HALF_OPEN, failure immediately trips back to OPEN
    with pytest.raises(RuntimeError):
        await cb.execute(failing_call)
    assert cb.state == CircuitState.OPEN


class MockRedisKV:
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def set(self, key, val):
        self.data[key] = val


@pytest.mark.asyncio
async def test_distributed_redis_circuit_breaker_shared_across_workers():
    from app.agents.runtime.enterprise.circuit_breaker import RedisCircuitStateStore

    mock_redis = MockRedisKV()
    shared_store = RedisCircuitStateStore(redis_client=mock_redis)

    # Worker 1 creates breaker for external OCR service
    worker1_cb = CircuitBreaker("ocr_service", failure_threshold=2, state_store=shared_store)
    # Worker 2 creates breaker for same external OCR service
    worker2_cb = CircuitBreaker("ocr_service", failure_threshold=2, state_store=shared_store)

    async def failing_call():
        raise ConnectionResetError("Provider dropped connection")

    # Worker 1 experiences 1st failure
    with pytest.raises(ConnectionResetError):
        await worker1_cb.execute(failing_call)
    assert worker1_cb.state == CircuitState.CLOSED
    # Worker 2 immediately observes the failure count from the shared store
    assert worker2_cb.failure_count == 1

    # Worker 2 experiences 2nd failure -> trips circuit for EVERYONE
    with pytest.raises(ConnectionResetError):
        await worker2_cb.execute(failing_call)

    assert worker2_cb.state == CircuitState.OPEN
    # Worker 1 also sees it is now OPEN and rejects subsequent calls immediately!
    assert worker1_cb.state == CircuitState.OPEN
    with pytest.raises(CircuitBreakerOpenError):
        await worker1_cb.execute(lambda: "should not be called")

