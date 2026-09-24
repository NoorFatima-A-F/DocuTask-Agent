"""Tests for Resource Abstraction and Lifecycle Transitions."""

from app.infrastructure.core.lifecycle import (
    ResourceLifecycleStateMachine,
    ResourceState,
)
from app.infrastructure.core.resources import (
    ComputeType,
    ResourceCategory,
    ResourceManager,
    ResourceSpecification,
)


def test_resource_state_machine():
    assert ResourceLifecycleStateMachine.can_transition(ResourceState.REQUESTED, ResourceState.ALLOCATING) is True
    assert ResourceLifecycleStateMachine.can_transition(ResourceState.ALLOCATING, ResourceState.READY) is True
    assert ResourceLifecycleStateMachine.can_transition(ResourceState.READY, ResourceState.ACTIVE) is True
    assert ResourceLifecycleStateMachine.can_transition(ResourceState.ACTIVE, ResourceState.DRAINING) is True
    assert ResourceLifecycleStateMachine.can_transition(ResourceState.DRAINING, ResourceState.RELEASED) is True


def test_resource_manager_allocation_and_release():
    mgr = ResourceManager()
    spec = ResourceSpecification(
        name="ocr-inference-cluster",
        category=ResourceCategory.COMPUTE,
        resource_type=ComputeType.CONTAINER.value,
        cpu_cores=4.0,
        memory_mb=8192,
        environment="PRODUCTION",
    )

    # 1. Request
    req = mgr.request_resource(spec, provider="kubernetes")
    assert req.state == ResourceState.REQUESTED

    # 2. Allocate
    allocated = mgr.allocate_resource(req.resource_id, endpoint_url="http://ocr.k8s.internal")
    assert allocated.state == ResourceState.ACTIVE
    assert allocated.endpoint_url == "http://ocr.k8s.internal"

    # 3. Query
    fetched = mgr.get_resource(allocated.resource_id)
    assert fetched.name == "ocr-inference-cluster"

    # 4. Release
    released = mgr.release_resource(allocated.resource_id)
    assert released.state == ResourceState.RELEASED
