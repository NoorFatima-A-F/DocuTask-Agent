"""
Unit test suite for Hardened Runtime Boot and Graceful Shutdown.
Validates:
- BootTransactionManager LIFO compensating rollback
- StartupPipeline full 10-step boot execution
- Startup failure transactional rollback & RuntimeBootFailedEvent emission
- ShutdownPipeline 8-step lifecycle transition (RUNNING -> DRAINING -> STOPPING -> TERMINATED)
- Drain timeout forced termination escalation
"""

from unittest.mock import patch
import pytest
from app.agents.runtime.configuration import PlatformRuntimeConfig
from app.agents.runtime.events import RuntimeBootFailedEvent
from app.agents.runtime.runtime_lifecycle import RuntimeLifecycleState
from app.agents.runtime.runtime_state import RuntimeState
from app.agents.runtime.shutdown import ShutdownPipeline
from app.agents.runtime.startup import BootTransactionManager, StartupPipeline


@pytest.mark.asyncio
async def test_boot_transaction_manager_lifo_rollback():
    tx = BootTransactionManager()
    rollback_order = []

    async def rb_step1():
        rollback_order.append("step1")

    async def rb_step2():
        rollback_order.append("step2")

    async def rb_step3():
        rollback_order.append("step3")

    tx.record_action("step1", rb_step1)
    tx.record_action("step2", rb_step2)
    tx.record_action("step3", rb_step3)

    executed = await tx.execute_rollback()

    # LIFO order: step3, step2, step1
    assert rollback_order == ["step3", "step2", "step1"]
    assert executed == ["step3", "step2", "step1"]

    # After execution, journal is empty
    executed_again = await tx.execute_rollback()
    assert executed_again == []


@pytest.mark.asyncio
async def test_startup_pipeline_success():
    config = PlatformRuntimeConfig(runtime_name="test_runtime", enable_plugins=False)
    pipeline = StartupPipeline(config=config)

    result = await pipeline.execute()

    assert "state" in result
    assert "container" in result
    assert "service_registry" in result
    assert result["state"].lifecycle_state == RuntimeLifecycleState.RUNNING


@pytest.mark.asyncio
async def test_startup_pipeline_failure_rollback():
    class DummyFailingEventBus:
        def __init__(self):
            self.events = []

        async def publish(self, event):
            self.events.append(event)

    bus = DummyFailingEventBus()
    config = PlatformRuntimeConfig(runtime_name="test_failing_runtime")
    pipeline = StartupPipeline(config=config, event_bus=bus)

    with patch("app.agents.runtime.startup.ModuleLoader.discover_modules", side_effect=RuntimeError("Discovery crash")):
        with pytest.raises(RuntimeError):
            await pipeline.execute()

    # Verify RuntimeBootFailedEvent was published
    failed_events = [e for e in bus.events if isinstance(e, RuntimeBootFailedEvent)]
    assert len(failed_events) >= 1
    assert "Discovery crash" in failed_events[0].payload.get("error", "")


@pytest.mark.asyncio
async def test_shutdown_pipeline_orderly_flow():
    pipeline = ShutdownPipeline()
    initial_state = RuntimeState(lifecycle_state=RuntimeLifecycleState.RUNNING)

    terminal_state = await pipeline.execute(current_state=initial_state, active_tasks_count=2)

    assert terminal_state.lifecycle_state == RuntimeLifecycleState.TERMINATED


@pytest.mark.asyncio
async def test_shutdown_pipeline_forced_timeout():
    pipeline = ShutdownPipeline(drain_timeout_seconds=0.01)
    initial_state = RuntimeState(lifecycle_state=RuntimeLifecycleState.RUNNING)

    terminal_state = await pipeline.execute(
        current_state=initial_state,
        active_tasks_count=5,
        force_timeout=True,
    )

    assert terminal_state.lifecycle_state == RuntimeLifecycleState.TERMINATED
