"""
Enterprise Chaos Testing & Fault Injection Test Suite.
Validates:
- Fault injector arming and triggering (WORKER_CRASH, NETWORK_FAILURE, DEPENDENCY_TIMEOUT, MEMORY_PRESSURE)
- Fault clearing disarms triggers
- ChaosEngine running automated chaos experiments and asserting recovery
"""

import pytest
from app.agents.runtime.enterprise.chaos_engine import ChaosEngine
from app.agents.runtime.enterprise.fault_injector import (
    FaultInjector,
    FaultType,
    InjectedFaultException,
)


@pytest.mark.asyncio
async def test_fault_injector_types():
    injector = FaultInjector()

    # Worker crash
    injector.inject_fault("planner", FaultType.WORKER_CRASH)
    with pytest.raises(InjectedFaultException):
        await injector.maybe_fail("planner")

    # Network failure
    injector.inject_fault("messaging", FaultType.NETWORK_FAILURE)
    with pytest.raises(ConnectionResetError):
        await injector.maybe_fail("messaging")

    # Dependency timeout
    injector.inject_fault("database", FaultType.DEPENDENCY_TIMEOUT)
    with pytest.raises(TimeoutError):
        await injector.maybe_fail("database")

    # Memory pressure
    injector.inject_fault("cache", FaultType.MEMORY_PRESSURE)
    with pytest.raises(MemoryError):
        await injector.maybe_fail("cache")

    # Unarmed subsystem does not fail
    await injector.maybe_fail("unarmed_subsystem")

    # Disarming fault
    injector.clear_fault("planner")
    await injector.maybe_fail("planner")


@pytest.mark.asyncio
async def test_chaos_engine_experiment_workflow():
    engine = ChaosEngine()

    recovered_status = False

    async def workload():
        await engine.injector.maybe_fail("execution_engine")

    async def assertion():
        nonlocal recovered_status
        recovered_status = True
        return recovered_status

    res = await engine.run_experiment(
        experiment_name="execution_engine_resilience",
        target_subsystem="execution_engine",
        fault_type=FaultType.WORKER_CRASH,
        workload_fn=workload,
        recovery_assertion=assertion,
    )

    assert res.passed is True
    assert res.experiment_name == "execution_engine_resilience"
    assert recovered_status is True


@pytest.mark.asyncio
async def test_fault_injector_burst_count():
    injector = FaultInjector()
    # Inject burst count of exactly 2
    injector.inject_fault("worker", FaultType.WORKER_CRASH, burst_count=2)

    # 1st time fails
    with pytest.raises(InjectedFaultException):
        await injector.maybe_fail("worker")

    # 2nd time fails
    with pytest.raises(InjectedFaultException):
        await injector.maybe_fail("worker")

    # 3rd time succeeds because burst count exhausted and auto-disarmed
    await injector.maybe_fail("worker")


@pytest.mark.asyncio
async def test_chaos_latency_jitter_and_metrics():
    import time
    engine = ChaosEngine()

    async def workload():
        await engine.injector.maybe_fail("slow_api")

    async def assertion():
        return True

    res = await engine.run_experiment(
        experiment_name="latency_test",
        target_subsystem="slow_api",
        fault_type=FaultType.LATENCY_JITTER,
        workload_fn=workload,
        recovery_assertion=assertion,
        delay_seconds=0.05,
    )

    assert res.passed is True
    assert res.duration_ms >= 40.0

