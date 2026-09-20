"""
Unit test suite for Erlang OTP-Style Runtime Supervisor Engine.
Validates:
- ONE_FOR_ONE restart strategy
- ONE_FOR_ALL restart strategy
- REST_FOR_ONE restart strategy
- Exponential backoff & cooldown window reset
- Max restarts threshold enforcement and SubsystemCrashError escalation
- ChildProcessRegistry and SupervisorTree hierarchies
"""

import asyncio
import time
import pytest
from app.agents.runtime.runtime_supervisor import (
    ChildProcessRegistry,
    ChildProcessSpec,
    RestartPolicy,
    RestartStrategy,
    RuntimeSupervisor,
    SupervisorTree,
)
from app.agents.runtime.exceptions import SubsystemCrashError


@pytest.mark.asyncio
async def test_restart_policy_backoff_calculation():
    policy = RestartPolicy(
        max_restarts=5,
        initial_backoff_seconds=0.1,
        backoff_multiplier=2.0,
        max_backoff_seconds=1.0,
    )
    assert policy.calculate_backoff(1) == pytest.approx(0.1)
    assert policy.calculate_backoff(2) == pytest.approx(0.2)
    assert policy.calculate_backoff(3) == pytest.approx(0.4)
    assert policy.calculate_backoff(4) == pytest.approx(0.8)
    assert policy.calculate_backoff(5) == pytest.approx(1.0)  # Capped by max_backoff


def test_child_process_registry_ordering():
    registry = ChildProcessRegistry()

    async def dummy_start():
        pass

    spec_a = ChildProcessSpec(name="worker_a", start_fn=dummy_start)
    spec_b = ChildProcessSpec(name="worker_b", start_fn=dummy_start)
    spec_c = ChildProcessSpec(name="worker_c", start_fn=dummy_start)

    registry.register(spec_a)
    registry.register(spec_b)
    registry.register(spec_c)

    specs = registry.list_specs()
    assert [s.name for s in specs] == ["worker_a", "worker_b", "worker_c"]

    subsequent = registry.get_subsequent("worker_b")
    assert [s.name for s in subsequent] == ["worker_b", "worker_c"]

    subsequent_c = registry.get_subsequent("worker_c")
    assert [s.name for s in subsequent_c] == ["worker_c"]

    assert registry.get_subsequent("non_existent") == []


@pytest.mark.asyncio
async def test_supervisor_one_for_one_strategy():
    tree = SupervisorTree(
        strategy=RestartStrategy.ONE_FOR_ONE,
        default_policy=RestartPolicy(initial_backoff_seconds=0.01, max_restarts=3),
    )

    restarts = {"a": 0, "b": 0, "c": 0}

    async def start_a():
        restarts["a"] += 1

    async def start_b():
        restarts["b"] += 1

    async def start_c():
        restarts["c"] += 1

    tree.add_child("worker_a", start_fn=start_a)
    tree.add_child("worker_b", start_fn=start_b)
    tree.add_child("worker_c", start_fn=start_c)

    # Initial starts recorded manually or on failure
    await tree.handle_child_failure("worker_b")

    # In ONE_FOR_ONE, only worker_b should be restarted
    assert restarts["a"] == 0
    assert restarts["b"] == 1
    assert restarts["c"] == 0


@pytest.mark.asyncio
async def test_supervisor_one_for_all_strategy():
    tree = SupervisorTree(
        strategy=RestartStrategy.ONE_FOR_ALL,
        default_policy=RestartPolicy(initial_backoff_seconds=0.01, max_restarts=3),
    )

    stopped = []
    started = []

    def make_worker(name: str):
        async def start_fn():
            started.append(name)

        async def stop_fn():
            stopped.append(name)

        return start_fn, stop_fn

    start_a, stop_a = make_worker("worker_a")
    start_b, stop_b = make_worker("worker_b")
    start_c, stop_c = make_worker("worker_c")

    tree.add_child("worker_a", start_fn=start_a, stop_fn=stop_a)
    tree.add_child("worker_b", start_fn=start_b, stop_fn=stop_b)
    tree.add_child("worker_c", start_fn=start_c, stop_fn=stop_c)

    await tree.handle_child_failure("worker_b")

    # ONE_FOR_ALL stops in reverse order: c, b, a
    assert stopped == ["worker_c", "worker_b", "worker_a"]
    # And starts in order: a, b, c
    assert started == ["worker_a", "worker_b", "worker_c"]


@pytest.mark.asyncio
async def test_supervisor_rest_for_one_strategy():
    tree = SupervisorTree(
        strategy=RestartStrategy.REST_FOR_ONE,
        default_policy=RestartPolicy(initial_backoff_seconds=0.01, max_restarts=3),
    )

    stopped = []
    started = []

    def make_worker(name: str):
        async def start_fn():
            started.append(name)

        async def stop_fn():
            stopped.append(name)

        return start_fn, stop_fn

    start_a, stop_a = make_worker("worker_a")
    start_b, stop_b = make_worker("worker_b")
    start_c, stop_c = make_worker("worker_c")

    tree.add_child("worker_a", start_fn=start_a, stop_fn=stop_a)
    tree.add_child("worker_b", start_fn=start_b, stop_fn=stop_b)
    tree.add_child("worker_c", start_fn=start_c, stop_fn=stop_c)

    await tree.handle_child_failure("worker_b")

    # REST_FOR_ONE stops only b and subsequent (c, then b)
    assert stopped == ["worker_c", "worker_b"]
    # And starts b, then c (a was untouched)
    assert started == ["worker_b", "worker_c"]


@pytest.mark.asyncio
async def test_max_restart_budget_exceeded_raises_subsystem_crash():
    tree = SupervisorTree(
        strategy=RestartStrategy.ONE_FOR_ONE,
        default_policy=RestartPolicy(
            max_restarts=2,
            restart_window_seconds=10.0,
            initial_backoff_seconds=0.01,
        ),
    )

    async def dummy_start():
        pass

    tree.add_child("flaky_worker", start_fn=dummy_start)

    # 1st restart
    await tree.handle_child_failure("flaky_worker")
    # 2nd restart
    await tree.handle_child_failure("flaky_worker")

    # 3rd restart should exceed budget of 2
    with pytest.raises(SubsystemCrashError) as exc_info:
        await tree.handle_child_failure("flaky_worker")

    assert "exceeded maximum restart threshold (2)" in str(exc_info.value)
    spec = tree.registry.get("flaky_worker")
    assert spec is not None
    assert not spec.is_healthy


@pytest.mark.asyncio
async def test_cooldown_window_resets_restart_history():
    policy = RestartPolicy(
        max_restarts=2,
        restart_window_seconds=10.0,
        cooldown_seconds=0.1,  # Short cooldown for test
        initial_backoff_seconds=0.01,
    )
    tree = SupervisorTree(strategy=RestartStrategy.ONE_FOR_ONE, default_policy=policy)

    async def dummy_start():
        pass

    tree.add_child("worker", start_fn=dummy_start)

    # 1st failure
    await tree.handle_child_failure("worker")
    spec = tree.registry.get("worker")
    assert len(spec.restart_timestamps) == 1

    # Wait for cooldown
    await asyncio.sleep(0.15)

    # 2nd failure should reset prior history due to cooldown
    await tree.handle_child_failure("worker")
    assert len(spec.restart_timestamps) == 1  # Reset and now 1


@pytest.mark.asyncio
async def test_runtime_supervisor_facade():
    supervisor = RuntimeSupervisor(strategy=RestartStrategy.ONE_FOR_ONE, max_restarts=3)

    started = []
    stopped = []

    async def start_subsystem():
        started.append(True)

    async def stop_subsystem():
        stopped.append(True)

    supervisor.register_subsystem_worker(
        module_name="workflow_engine",
        start_fn=start_subsystem,
        stop_fn=stop_subsystem,
    )

    async def failing_action():
        raise RuntimeError("simulated failure")

    # Supervise should catch exception, trigger restart, and return None
    result = await supervisor.supervise("workflow_engine", failing_action)
    assert result is None
    assert len(started) == 1
    assert len(stopped) == 1

    # Explicit manual restart
    await supervisor.restart_subsystem("workflow_engine")
    assert len(started) == 2
    assert len(stopped) == 2


@pytest.mark.asyncio
async def test_async_worker_restart():
    from app.agents.runtime.runtime_supervisor import AsyncTaskWorker, WorkerLifecycleManager

    run_count = 0

    async def worker_task():
        nonlocal run_count
        run_count += 1
        await asyncio.sleep(0.01)

    worker = AsyncTaskWorker("extraction_agent_worker", worker_task)
    manager = WorkerLifecycleManager()
    manager.register_worker(worker)

    await worker.start()
    assert worker.is_alive()
    await asyncio.sleep(0.02)
    assert run_count == 1

    # Simulate restart via lifecycle manager
    await manager.handle_worker_failure("extraction_agent_worker")
    assert worker.is_alive()
    await asyncio.sleep(0.02)
    assert run_count == 2
    await worker.stop()


@pytest.mark.asyncio
async def test_worker_heartbeat_timeout():
    from app.agents.runtime.runtime_supervisor import AsyncTaskWorker, WorkerHeartbeatMonitor, WorkerStatus

    async def idle_task():
        await asyncio.sleep(1.0)

    worker = AsyncTaskWorker("ocr_worker", idle_task)
    monitor = WorkerHeartbeatMonitor(default_timeout_seconds=0.05)
    monitor.register_worker(worker)

    await worker.start()
    assert worker.status == WorkerStatus.RUNNING

    # Heartbeat fresh -> no timeouts
    timed_out = monitor.check_heartbeats()
    assert timed_out == []

    # Wait past timeout without recording heartbeat
    await asyncio.sleep(0.07)
    timed_out = monitor.check_heartbeats()
    assert timed_out == ["ocr_worker"]
    assert worker.status == WorkerStatus.UNHEALTHY
    await worker.stop()


@pytest.mark.asyncio
async def test_checkpoint_restore_after_failure():
    from app.agents.runtime.runtime_supervisor import CheckpointRecoveryManager

    chk_mgr = CheckpointRecoveryManager()
    chk_mgr.save_checkpoint("validation_worker", {"doc_id": "inv-001", "step": "parsed", "processed_lines": 42})

    restored = chk_mgr.restore_checkpoint("validation_worker")
    assert restored is not None
    assert restored["doc_id"] == "inv-001"
    assert restored["step"] == "parsed"
    assert restored["processed_lines"] == 42

    chk_mgr.clear_checkpoint("validation_worker")
    assert chk_mgr.restore_checkpoint("validation_worker") is None


import threading


@pytest.mark.asyncio
async def test_supervisor_process_isolation():
    from app.agents.runtime.runtime_supervisor import ContainerWorker, ThreadWorker

    gate = threading.Event()

    def thread_body():
        gate.wait(timeout=2.0)

    thread_w = ThreadWorker("calc_thread", thread_body)
    await thread_w.start()
    assert thread_w.is_alive()
    gate.set()
    await thread_w.stop()
    assert not thread_w.is_alive()

    container_w = ContainerWorker("isolated_container", image="ocr:v1")
    await container_w.start()
    assert container_w.is_alive()
    await container_w.stop()
    assert not container_w.is_alive()

