"""
Tests for Reliability Domain Models, RTO/RPO Targets, and 7-State Lifecycle State Machine.
"""

import pytest
from app.infrastructure.reliability.models import (
    FaultDomain,
    ReliabilityPolicy,
    ReliabilityState,
    ReliabilityTarget,
    RPOObjective,
    RTOObjective,
)
from app.infrastructure.reliability.state_machine import (
    ReliabilityInvalidTransitionError,
    ReliabilityLifecycleStateMachine,
)
from app.infrastructure.reliability.coordinator import ReliabilityCoordinator
from app.infrastructure.reliability.manager import ReliabilityManager


def test_reliability_models_and_objectives():
    rto = RTOObjective(target_seconds=120.0, max_acceptable_seconds=300.0, critical_path=True)
    rpo = RPOObjective(target_seconds=30.0, max_acceptable_seconds=90.0, allow_data_loss=False)

    target = ReliabilityTarget(
        target_id="target-api-gateway",
        component_name="api-gateway",
        availability_sla_percent=99.99,
        rto=rto,
        rpo=rpo,
        fault_domain=FaultDomain.SERVICE,
    )

    assert target.target_id == "target-api-gateway"
    assert target.rto.target_seconds == 120.0
    assert target.rpo.target_seconds == 30.0
    assert target.fault_domain == FaultDomain.SERVICE


def test_reliability_state_machine_valid_transitions():
    sm = ReliabilityLifecycleStateMachine(component_id="worker-cluster-01", initial_state=ReliabilityState.OPTIMAL)
    assert sm.current_state == ReliabilityState.OPTIMAL

    hook_calls = []
    sm.register_hook(lambda record: hook_calls.append(record.to_state))

    # OPTIMAL -> DEGRADED
    rec1 = sm.transition_to(ReliabilityState.DEGRADED, reason="Elevated latency detected")
    assert rec1.from_state == ReliabilityState.OPTIMAL
    assert rec1.to_state == ReliabilityState.DEGRADED
    assert sm.current_state == ReliabilityState.DEGRADED

    # DEGRADED -> FAILING
    sm.transition_to(ReliabilityState.FAILING, reason="Error rate > 20%")
    assert sm.current_state == ReliabilityState.FAILING

    # FAILING -> OUTAGE
    sm.transition_to(ReliabilityState.OUTAGE, reason="Unresponsive nodes")
    assert sm.current_state == ReliabilityState.OUTAGE

    # OUTAGE -> RECOVERING
    sm.transition_to(ReliabilityState.RECOVERING, reason="Recovery workflow started")
    assert sm.current_state == ReliabilityState.RECOVERING

    # RECOVERING -> RECOVERED
    sm.transition_to(ReliabilityState.RECOVERED, reason="Readiness checks passed")
    assert sm.current_state == ReliabilityState.RECOVERED

    # RECOVERED -> OPTIMAL
    sm.transition_to(ReliabilityState.OPTIMAL, reason="Full soak period completed")
    assert sm.current_state == ReliabilityState.OPTIMAL

    assert len(sm.history) == 6
    assert len(hook_calls) == 6
    assert hook_calls[-1] == ReliabilityState.OPTIMAL


def test_reliability_state_machine_invalid_transition():
    sm = ReliabilityLifecycleStateMachine(component_id="service-ocr", initial_state=ReliabilityState.OPTIMAL)

    # Cannot transition directly from OPTIMAL to RECOVERED
    assert not sm.can_transition_to(ReliabilityState.RECOVERED)

    with pytest.raises(ReliabilityInvalidTransitionError):
        sm.transition_to(ReliabilityState.RECOVERED, reason="Illegal jump")


def test_reliability_coordinator_assessment():
    coordinator = ReliabilityCoordinator()
    target = ReliabilityTarget(
        target_id="target-embeddings",
        component_name="embedding-service",
        rto=RTOObjective(target_seconds=60.0, max_acceptable_seconds=180.0),
        rpo=RPOObjective(target_seconds=10.0, max_acceptable_seconds=30.0),
    )
    coordinator.register_target(target)

    # Normal state assessment
    assessment1 = coordinator.assess_component(
        target_id="target-embeddings",
        current_downtime_seconds=0.0,
        current_lag_seconds=2.0,
        measured_availability_percent=100.0,
    )
    assert not assessment1.at_risk
    assert assessment1.state == ReliabilityState.OPTIMAL

    # Breach target RTO
    assessment2 = coordinator.assess_component(
        target_id="target-embeddings",
        current_downtime_seconds=75.0,
        current_lag_seconds=2.0,
    )
    assert assessment2.at_risk
    assert assessment2.recommended_action == "INITIATE_FAILOVER_PLANNING"
    assert assessment2.state == ReliabilityState.FAILING

    # Breach max acceptable RTO
    assessment3 = coordinator.assess_component(
        target_id="target-embeddings",
        current_downtime_seconds=200.0,
        current_lag_seconds=2.0,
    )
    assert assessment3.at_risk
    assert assessment3.recommended_action == "TRIGGER_EMERGENCY_FAILOVER"
    assert assessment3.state == ReliabilityState.OUTAGE


def test_reliability_manager_integration():
    manager = ReliabilityManager()
    policy = ReliabilityPolicy(
        policy_id="policy-standard",
        name="Standard Service Policy",
        timeout_budget_seconds=15.0,
    )

    manager.register_target(
        target_id="target-db",
        component_name="primary-database",
        fault_domain=FaultDomain.DATABASE,
        policy=policy,
    )

    assert manager.get_component_state("target-db") == ReliabilityState.OPTIMAL
    assert manager.get_policy_for_component("target-db").policy_id == "policy-standard"

    manager.record_transition("target-db", ReliabilityState.DEGRADED, reason="High disk I/O")
    assert manager.get_component_state("target-db") == ReliabilityState.DEGRADED

    summary = manager.get_resilience_summary()
    assert summary[ReliabilityState.DEGRADED.value] == 1
    assert summary[ReliabilityState.OPTIMAL.value] == 0
