"""
Tests for Platform RuntimeManager and 17-State Finite State Machine.
"""

import pytest
import asyncio
from app.platform.runtime.manager import RuntimeManager
from app.platform.runtime.states import RuntimeState
from app.platform.kernel.exceptions import LifecycleException


def test_runtime_initial_state():
    runtime = RuntimeManager()
    assert runtime.state == RuntimeState.CREATED
    assert len(runtime.get_state_history()) == 0


def test_runtime_bootstrap_full_cycle():
    runtime = RuntimeManager()
    events = []
    runtime.add_state_listener(lambda evt: events.append(evt.to_state))

    asyncio.run(runtime.bootstrap())

    assert runtime.state == RuntimeState.RUNNING
    assert RuntimeState.CONFIG_LOADING in events
    assert RuntimeState.DATABASE_READY in events
    assert RuntimeState.EVENT_BUS_READY in events
    assert RuntimeState.SERVICE_READY in events
    assert RuntimeState.READY in events
    assert RuntimeState.RUNNING in events
    assert len(runtime.get_state_history()) >= 13


def test_runtime_invalid_transition_fails():
    runtime = RuntimeManager()
    # Cannot jump from CREATED directly to RUNNING without bootstrap
    with pytest.raises(LifecycleException):
        runtime.transition(RuntimeState.RUNNING)


def test_runtime_shutdown_cycle():
    runtime = RuntimeManager()
    asyncio.run(runtime.bootstrap())
    assert runtime.state == RuntimeState.RUNNING

    asyncio.run(runtime.shutdown())
    assert runtime.state == RuntimeState.TERMINATED
    assert runtime.health_manager._is_ready is False
