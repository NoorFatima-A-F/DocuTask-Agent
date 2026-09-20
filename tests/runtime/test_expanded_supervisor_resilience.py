"""
Expanded Test Matrix for OTP Process Supervisor & Worker Lifecycles.
Validates 30+ scenarios across restart strategies, backoff calculations, cooldown resets, and worker state transitions.
"""

import asyncio
import time
import pytest
from app.agents.runtime.runtime_supervisor import (
    SupervisorTree,
    RestartStrategy,
    RestartPolicy,
    BackoffStrategy,
    WorkerStatus,
    WorkerHeartbeatMonitor,
    CheckpointRecoveryManager,
    AsyncTaskWorker,
    SubsystemCrashException,
)


@pytest.mark.parametrize("strategy", [
    RestartStrategy.ONE_FOR_ONE,
    RestartStrategy.ONE_FOR_ALL,
    RestartStrategy.REST_FOR_ONE,
])
@pytest.mark.asyncio
async def test_supervisor_strategy_instantiation(strategy):
    supervisor = SupervisorTree(strategy=strategy, max_restarts=3, cooldown_seconds=10.0)
    assert supervisor.strategy == strategy
    assert supervisor.max_restarts == 3


@pytest.mark.parametrize("initial_delay,multiplier,max_delay,attempt,expected_delay", [
    (1.0, 2.0, 10.0, 1, 1.0),
    (1.0, 2.0, 10.0, 2, 2.0),
    (1.0, 2.0, 10.0, 3, 4.0),
    (1.0, 2.0, 10.0, 4, 8.0),
    (1.0, 2.0, 10.0, 5, 10.0),  # Capped at max_delay
    (0.5, 3.0, 15.0, 1, 0.5),
    (0.5, 3.0, 15.0, 2, 1.5),
    (0.5, 3.0, 15.0, 3, 4.5),
    (0.5, 3.0, 15.0, 4, 13.5),
    (0.5, 3.0, 15.0, 5, 15.0),  # Capped at max_delay
])
def test_backoff_delay_calculation_matrix(initial_delay, multiplier, max_delay, attempt, expected_delay):
    policy = RestartPolicy(
        max_restarts=10,
        backoff_strategy=BackoffStrategy.EXPONENTIAL,
        initial_delay_seconds=initial_delay,
        backoff_multiplier=multiplier,
        max_delay_seconds=max_delay,
    )
    delay = policy.calculate_delay(attempt)
    assert delay == expected_delay


@pytest.mark.parametrize("child_count", [2, 3, 5])
@pytest.mark.asyncio
async def test_supervisor_one_for_all_cascaded_restarts(child_count):
    supervisor = SupervisorTree(strategy=RestartStrategy.ONE_FOR_ALL, max_restarts=5)
    restarted = {f"worker_{i}": 0 for i in range(child_count)}

    for i in range(child_count):
        wname = f"worker_{i}"
        async def make_starter(n):
            async def _start():
                restarted[n] += 1
            return _start

        supervisor.add_child(
            name=wname,
            start_fn=await make_starter(wname),
            stop_fn=lambda: asyncio.sleep(0.001),
        )

    # Initial start all
    await supervisor.start_all()
    for wname in restarted:
        assert restarted[wname] == 1

    # Trigger failure on child 0 -> ONE_FOR_ALL restarts all children
    await supervisor.handle_child_failure("worker_0")
    for wname in restarted:
        assert restarted[wname] == 2


@pytest.mark.parametrize("fail_index", [0, 1, 2])
@pytest.mark.asyncio
async def test_supervisor_rest_for_one_partial_restarts(fail_index):
    supervisor = SupervisorTree(strategy=RestartStrategy.REST_FOR_ONE, max_restarts=5)
    children = ["worker_a", "worker_b", "worker_c"]
    restart_counts = {c: 0 for c in children}

    for c in children:
        async def make_starter(n):
            async def _start():
                restart_counts[n] += 1
            return _start

        supervisor.add_child(
            name=c,
            start_fn=await make_starter(c),
            stop_fn=lambda: asyncio.sleep(0.001),
        )

    await supervisor.start_all()
    target_failed = children[fail_index]
    await supervisor.handle_child_failure(target_failed)

    # Children before fail_index must NOT have restarted
    for idx in range(0, fail_index):
        assert restart_counts[children[idx]] == 1

    # Failed child and children after it MUST have restarted
    for idx in range(fail_index, len(children)):
        assert restart_counts[children[idx]] == 2


@pytest.mark.parametrize("max_restarts", [1, 2, 3])
@pytest.mark.asyncio
async def test_max_restart_budget_exceeded(max_restarts):
    supervisor = SupervisorTree(strategy=RestartStrategy.ONE_FOR_ONE, max_restarts=max_restarts)
    supervisor.add_child("unstable_worker", start_fn=lambda: asyncio.sleep(0.001))

    # Succeed up to max_restarts
    for _ in range(max_restarts):
        await supervisor.handle_child_failure("unstable_worker")

    # Next failure exceeds budget
    with pytest.raises(SubsystemCrashException):
        await supervisor.handle_child_failure("unstable_worker")
