"""Tests for Chaos Fault Injection Engine."""

from app.networking.mesh.data_plane import MeshRequest
from app.networking.resilience.fault_injection import (
    FaultInjectionEngine,
    FaultInjectionRule,
    FaultType,
)


def test_fault_injection_abort():
    engine = FaultInjectionEngine()
    rule = FaultInjectionRule(
        rule_id="fault-abort-500",
        target_service="payment-gateway",
        fault_type=FaultType.ABORT,
        percentage=100.0,
        status_code=500,
        error_message="Synthetic Database Deadlock",
    )
    engine.add_rule(rule)

    req = MeshRequest(
        source_service="checkout",
        target_service="payment-gateway",
        action="pay",
    )
    fault_res = engine.evaluate_and_inject(req)
    assert fault_res is not None
    assert fault_res.status_code == 500
    assert fault_res.error_message == "Synthetic Database Deadlock"
    assert "fault_injection:fault-abort-500" in fault_res.applied_policy


def test_fault_injection_corruption():
    engine = FaultInjectionEngine()
    rule = FaultInjectionRule(
        rule_id="fault-corrupt-data",
        target_service="analytics-feed",
        fault_type=FaultType.CORRUPTION,
        percentage=100.0,
    )
    engine.add_rule(rule)

    req = MeshRequest(
        source_service="dashboard",
        target_service="analytics-feed",
        action="fetch",
    )
    fault_res = engine.evaluate_and_inject(req)
    assert fault_res is not None
    assert "corrupted_payload" in fault_res.payload
