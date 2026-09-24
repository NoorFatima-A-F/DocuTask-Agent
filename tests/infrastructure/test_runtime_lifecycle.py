"""Tests for Infrastructure Runtime Lifecycle and Automated Recovery."""

import pytest
from app.infrastructure.core.exceptions import (
    InvalidStateTransitionError,
)
from app.infrastructure.core.lifecycle import (
    RuntimeLifecycleStateMachine,
    RuntimeState,
)
from app.infrastructure.core.runtime import InfrastructureRuntime


def test_runtime_state_machine_valid_and_invalid_transitions():
    assert RuntimeLifecycleStateMachine.can_transition(RuntimeState.CREATED, RuntimeState.INITIALIZING) is True
    assert RuntimeLifecycleStateMachine.can_transition(RuntimeState.RUNNING, RuntimeState.STOPPING) is True
    assert RuntimeLifecycleStateMachine.can_transition(RuntimeState.CREATED, RuntimeState.RUNNING) is False

    with pytest.raises(InvalidStateTransitionError):
        RuntimeLifecycleStateMachine.transition(RuntimeState.CREATED, RuntimeState.RUNNING)


def test_runtime_deploy_and_graceful_stop_start():
    runtime = InfrastructureRuntime()
    inst = runtime.deploy(
        service="workflow-engine",
        environment="TESTING",
        replicas=2,
        version="1.0.0",
    )

    assert inst.service_name == "workflow-engine"
    assert inst.state == RuntimeState.RUNNING
    assert inst.replicas == 2

    # Stop service
    stopped = runtime.stop_service(inst.instance_id)
    assert stopped.state == RuntimeState.STOPPED

    # Start service
    started = runtime.start_service(inst.instance_id)
    assert started.state == RuntimeState.RUNNING


def test_runtime_self_healing_recovery():
    runtime = InfrastructureRuntime()
    inst = runtime.deploy(
        service="document-worker",
        environment="DEVELOPMENT",
        replicas=1,
    )

    # Simulate unexpected failure
    recovered = runtime.mark_failed(inst.instance_id, error_msg="Out of memory crash")
    assert recovered.state == RuntimeState.RUNNING
    assert recovered.recovery_attempts == 1
    assert recovered.error_message is None
