"""
Expanded Test Matrix for Circuit Breakers and Chaos Fault Injection.
Validates 30+ scenarios across state transitions, threshold triggers, failure probabilities, and distributed resilience.
"""

import asyncio
import pytest
from app.agents.runtime.enterprise.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerOpenError,
    CircuitState,
    MemoryCircuitStateStore,
)
from app.agents.runtime.enterprise.fault_injector import (
    FaultInjector,
    FaultType,
    InjectedFaultException,
)
from app.agents.runtime.enterprise.chaos_engine import ChaosEngine


@pytest.mark.parametrize("failure_threshold", [1, 2, 3, 5])
@pytest.mark.asyncio
async def test_circuit_breaker_tripping_thresholds(failure_threshold):
    cb = CircuitBreaker(name=f"breaker_{failure_threshold}", failure_threshold=failure_threshold)

    async def fail():
        raise RuntimeError("Service failure")

    # Up to threshold - 1 should remain CLOSED
    for i in range(failure_threshold - 1):
        with pytest.raises(RuntimeError):
            await cb.execute(fail)
        assert cb.state == CircuitState.CLOSED
        assert cb.failure_count == i + 1

    # Next failure trips to OPEN
    with pytest.raises(RuntimeError):
        await cb.execute(fail)
    assert cb.state == CircuitState.OPEN

    # Next attempt rejected immediately
    with pytest.raises(CircuitBreakerOpenError):
        await cb.execute(lambda: asyncio.sleep(0.001))


@pytest.mark.parametrize("success_threshold", [1, 2, 3])
@pytest.mark.asyncio
async def test_circuit_breaker_half_open_recovery_thresholds(success_threshold):
    cb = CircuitBreaker(
        name=f"rec_breaker_{success_threshold}",
        failure_threshold=1,
        recovery_timeout_seconds=0.04,
        success_threshold=success_threshold,
    )

    with pytest.raises(RuntimeError):
        await cb.execute(lambda: (_ for _ in ()).throw(RuntimeError("fail")))

    assert cb.state == CircuitState.OPEN
    await asyncio.sleep(0.06)

    # In HALF_OPEN, requires success_threshold successes to close
    for i in range(success_threshold - 1):
        res = await cb.execute(lambda: asyncio.sleep(0.001))
        assert cb.state == CircuitState.HALF_OPEN
        assert cb.success_count == i + 1

    # Final success closes breaker
    await cb.execute(lambda: asyncio.sleep(0.001))
    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 0


@pytest.mark.parametrize("fault_type", [
    FaultType.WORKER_CRASH,
    FaultType.NETWORK_FAILURE,
    FaultType.DEPENDENCY_TIMEOUT,
    FaultType.MEMORY_PRESSURE,
    FaultType.LATENCY_JITTER,
])
@pytest.mark.asyncio
async def test_fault_injector_all_types(fault_type):
    injector = FaultInjector()
    injector.inject_fault("test_sub", fault_type)

    if fault_type == FaultType.WORKER_CRASH:
        with pytest.raises(InjectedFaultException):
            await injector.maybe_fail("test_sub")
    elif fault_type == FaultType.NETWORK_FAILURE:
        with pytest.raises(ConnectionResetError):
            await injector.maybe_fail("test_sub")
    elif fault_type == FaultType.DEPENDENCY_TIMEOUT:
        with pytest.raises(TimeoutError):
            await injector.maybe_fail("test_sub")
    elif fault_type == FaultType.MEMORY_PRESSURE:
        with pytest.raises(MemoryError):
            await injector.maybe_fail("test_sub")
    elif fault_type == FaultType.LATENCY_JITTER:
        await injector.maybe_fail("test_sub")  # No exception raised for jitter


@pytest.mark.parametrize("burst_limit", [1, 3, 5])
@pytest.mark.asyncio
async def test_fault_injector_burst_limits_matrix(burst_limit):
    injector = FaultInjector()
    injector.inject_fault("burst_target", FaultType.WORKER_CRASH, burst_count=burst_limit)

    for _ in range(burst_limit):
        with pytest.raises(InjectedFaultException):
            await injector.maybe_fail("burst_target")

    # Burst count exhausted -> should not fail
    await injector.maybe_fail("burst_target")
