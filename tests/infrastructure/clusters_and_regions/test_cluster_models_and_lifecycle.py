"""Tests for Cluster Domain Models and Lifecycle State Machine."""

import pytest
from app.infrastructure.clusters.models import (
    CapacityModel,
    Cluster,
    ClusterIdentity,
    ClusterLease,
    ClusterStatus,
    ClusterType,
)
from app.infrastructure.clusters.lifecycle import (
    ClusterLifecycleStateMachine,
    InvalidClusterStateTransitionError,
)


def test_cluster_model_instantiation():
    cluster = Cluster(
        cluster_id="cls-us-east-1a",
        name="Production Primary US East",
        region_id="us-east-1",
        cluster_type=ClusterType.PRODUCTION,
        status=ClusterStatus.DISCOVERED,
    )
    assert cluster.cluster_id == "cls-us-east-1a"
    assert cluster.provider == "kubernetes"
    assert cluster.status == ClusterStatus.DISCOVERED
    assert cluster.capacity.total_cpu_cores == 128.0
    assert "SOC2_TYPE_II" in cluster.compliance_profiles


def test_cluster_lifecycle_valid_transitions():
    sm = ClusterLifecycleStateMachine()

    # DISCOVERED -> REGISTERING -> REGISTERED -> VALIDATING -> READY -> ACTIVE
    assert sm.transition(ClusterStatus.DISCOVERED, ClusterStatus.REGISTERING) == ClusterStatus.REGISTERING
    assert sm.transition(ClusterStatus.REGISTERING, ClusterStatus.REGISTERED) == ClusterStatus.REGISTERED
    assert sm.transition(ClusterStatus.REGISTERED, ClusterStatus.VALIDATING) == ClusterStatus.VALIDATING
    assert sm.transition(ClusterStatus.VALIDATING, ClusterStatus.READY) == ClusterStatus.READY
    assert sm.transition(ClusterStatus.READY, ClusterStatus.ACTIVE) == ClusterStatus.ACTIVE

    # ACTIVE -> DEGRADED -> ACTIVE
    assert sm.transition(ClusterStatus.ACTIVE, ClusterStatus.DEGRADED) == ClusterStatus.DEGRADED
    assert sm.transition(ClusterStatus.DEGRADED, ClusterStatus.ACTIVE) == ClusterStatus.ACTIVE

    # ACTIVE -> DRAINING -> MAINTENANCE -> READY
    assert sm.transition(ClusterStatus.ACTIVE, ClusterStatus.DRAINING) == ClusterStatus.DRAINING
    assert sm.transition(ClusterStatus.DRAINING, ClusterStatus.MAINTENANCE) == ClusterStatus.MAINTENANCE
    assert sm.transition(ClusterStatus.MAINTENANCE, ClusterStatus.READY) == ClusterStatus.READY

    # READY -> SUSPENDED -> OFFLINE -> REMOVED
    assert sm.transition(ClusterStatus.READY, ClusterStatus.SUSPENDED) == ClusterStatus.SUSPENDED
    assert sm.transition(ClusterStatus.SUSPENDED, ClusterStatus.OFFLINE) == ClusterStatus.OFFLINE
    assert sm.transition(ClusterStatus.OFFLINE, ClusterStatus.REMOVED) == ClusterStatus.REMOVED


def test_cluster_lifecycle_invalid_transitions():
    sm = ClusterLifecycleStateMachine()

    # DISCOVERED cannot jump directly to ACTIVE or OFFLINE
    with pytest.raises(InvalidClusterStateTransitionError):
        sm.transition(ClusterStatus.DISCOVERED, ClusterStatus.ACTIVE)

    with pytest.raises(InvalidClusterStateTransitionError):
        sm.transition(ClusterStatus.DISCOVERED, ClusterStatus.OFFLINE)

    # REMOVED cannot transition to any state (terminal)
    with pytest.raises(InvalidClusterStateTransitionError):
        sm.transition(ClusterStatus.REMOVED, ClusterStatus.READY)


def test_routable_states():
    sm = ClusterLifecycleStateMachine()
    assert sm.is_routable(ClusterStatus.ACTIVE) is True
    assert sm.is_routable(ClusterStatus.READY) is True
    assert sm.is_routable(ClusterStatus.DEGRADED) is False
    assert sm.is_routable(ClusterStatus.DRAINING) is False
    assert sm.is_routable(ClusterStatus.MAINTENANCE) is False
    assert sm.is_routable(ClusterStatus.OFFLINE) is False
