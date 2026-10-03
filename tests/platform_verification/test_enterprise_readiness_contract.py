"""
Pytest Test Suite for Part 3H.3.1: Enterprise Readiness Contract Architecture Verification Framework
"""
import json
import pytest

from app.platform_verification.readiness_contract.domain.models import (
    ReadinessState,
    TrafficAction,
    ReadinessTier,
)
from app.platform_verification.readiness_contract.state_machine.readiness_state_machine import ReadinessStateMachine
from app.platform_verification.readiness_contract.contract.readiness_contract_manager import ReadinessContractManager
from app.platform_verification.readiness_contract.decision.readiness_decision_engine import ReadinessDecisionEngine
from app.platform_verification.readiness_contract.policy.readiness_policy_engine import ReadinessPolicyEngine
from app.platform_verification.readiness_contract.startup.startup_readiness_validator import StartupReadinessValidator
from app.platform_verification.readiness_contract.transitions.failure_transition_tester import FailureTransitionTester
from app.platform_verification.readiness_contract.orchestration.readiness_orchestration_verifier import ReadinessOrchestrationVerifier
from app.platform_verification.readiness_contract.security.readiness_security_verifier import ReadinessSecurityVerifier
from app.platform_verification.readiness_contract.observability.readiness_metrics_exporter import ReadinessMetricsExporter
from app.platform_verification.readiness_contract.runtime.readiness_runtime import ReadinessRuntime


def test_readiness_state_machine_transitions():
    sm = ReadinessStateMachine()
    assert sm.current_state == ReadinessState.INITIALIZING

    # Valid transitions
    assert sm.transition_to(ReadinessState.CHECKING_DEPENDENCIES) == ReadinessState.CHECKING_DEPENDENCIES
    assert sm.current_state == ReadinessState.CHECKING_DEPENDENCIES

    assert sm.transition_to(ReadinessState.READY) == ReadinessState.READY
    assert sm.current_state == ReadinessState.READY

    assert sm.transition_to(ReadinessState.DEGRADED) == ReadinessState.DEGRADED
    assert sm.current_state == ReadinessState.DEGRADED

    assert sm.transition_to(ReadinessState.NOT_READY) == ReadinessState.NOT_READY
    assert sm.current_state == ReadinessState.NOT_READY

    assert sm.transition_to(ReadinessState.RECOVERING) == ReadinessState.RECOVERING
    assert sm.current_state == ReadinessState.RECOVERING

    assert sm.transition_to(ReadinessState.READY) == ReadinessState.READY
    assert sm.current_state == ReadinessState.READY

    # Invalid transitions should raise ValueError
    with pytest.raises(ValueError):
        sm.transition_to(ReadinessState.INITIALIZING)


def test_readiness_contract_manager_payload():
    cm = ReadinessContractManager()

    # All healthy -> ready
    payload_ready = cm.generate_ready_payload()
    assert payload_ready["status"] == "ready"
    assert payload_ready["service"] == "docutask-api"
    assert "timestamp" in payload_ready
    assert len(payload_ready["checks"]) == 5

    # Critical failure -> not_ready
    payload_not_ready = cm.generate_ready_payload(db_status="failed")
    assert payload_not_ready["status"] == "not_ready"

    # Optional failure -> degraded
    payload_degraded = cm.generate_ready_payload(ai_status="failed")
    assert payload_degraded["status"] == "degraded"

    # Contract schema validation
    report = cm.validate_readiness_contract()
    assert report.contract_schema_valid is True
    assert report.passed is True
    assert report.endpoint == "/ready"


def test_readiness_decision_engine():
    de = ReadinessDecisionEngine()

    # All healthy -> READY, ADMIT_TRAFFIC
    signals_ok = {"database": "healthy", "queue": "healthy", "storage": "healthy", "workers": "healthy", "ai_provider": "healthy"}
    state, action = de.evaluate_signals(signals_ok)
    assert state == ReadinessState.READY
    assert action == TrafficAction.ADMIT_TRAFFIC

    # Critical down -> NOT_READY, WITHHOLD_TRAFFIC
    signals_crit = {"database": "failed", "queue": "healthy", "storage": "healthy", "workers": "healthy", "ai_provider": "healthy"}
    state_crit, action_crit = de.evaluate_signals(signals_crit)
    assert state_crit == ReadinessState.NOT_READY
    assert action_crit == TrafficAction.WITHHOLD_TRAFFIC

    # Non-critical down -> DEGRADED, THROTTLE_TRAFFIC
    signals_deg = {"database": "healthy", "queue": "healthy", "storage": "healthy", "workers": "healthy", "ai_provider": "degraded"}
    state_deg, action_deg = de.evaluate_signals(signals_deg)
    assert state_deg == ReadinessState.DEGRADED
    assert action_deg == TrafficAction.THROTTLE_TRAFFIC


def test_readiness_policy_engine():
    pe = ReadinessPolicyEngine()
    report = pe.evaluate_policy()

    assert report.passed is True
    assert report.policy_enforcement_valid is True
    assert report.traffic_actions_mapped is True
    assert len(report.critical_dependencies) >= 3
    assert len(report.degraded_dependencies) >= 1
    assert "postgres" in report.critical_dependencies


def test_startup_readiness_validator():
    sv = StartupReadinessValidator()
    report = sv.validate_startup_sequence()

    assert report.passed is True
    assert report.startup_sequence_valid is True
    assert report.false_readiness_prevented is True
    assert report.total_steps_verified == 7
    assert len(report.steps) == 7


def test_failure_transition_tester():
    ft = FailureTransitionTester()
    report = ft.test_failure_transitions()

    assert report.passed is True
    assert report.total_transitions_tested == 4
    assert report.passed_transitions == 4
    assert report.startup_to_ready_passed is True
    assert report.db_failure_to_not_ready_passed is True
    assert report.recovery_to_ready_passed is True
    assert report.optional_dep_to_degraded_passed is True


def test_orchestration_verifier():
    ov = ReadinessOrchestrationVerifier()
    report = ov.verify_orchestration()

    assert report.passed is True
    assert report.kubernetes_readiness_probe_valid is True
    assert report.docker_compose_compatible is True
    assert len(report.cloud_runtimes_supported) >= 5
    assert report.probe_frequency_seconds == 10
    assert report.failure_threshold == 3


def test_security_verifier():
    sec = ReadinessSecurityVerifier()
    report = sec.verify_security()

    assert report["passed"] is True
    assert report["public_endpoint_leak_free"] is True
    assert report["credentials_leaked_count"] == 0


def test_observability_metrics():
    me = ReadinessMetricsExporter()
    prom = me.generate_prometheus_payload()
    summary = me.get_metrics_summary()

    assert "readiness_state 1" in prom
    assert "time_to_ready_seconds" in prom
    assert summary["prometheus_compatible"] is True
    assert summary["total_metrics"] >= 6


def test_score_engine_and_certification():
    runtime = ReadinessRuntime()
    results = runtime.execute_full_verification()
    scorecard = results["scorecard"]

    assert scorecard.overall_readiness_score >= 95.0
    assert scorecard.certification_tier == ReadinessTier.ENTERPRISE_READY
    assert scorecard.certification_verdict == "CERTIFIED"
    assert scorecard.passed is True
    assert scorecard.traffic_admission_safe is True
    assert scorecard.contract_correctness_score == 100.0
    assert scorecard.state_model_quality_score == 100.0
    assert scorecard.dependency_modeling_score == 100.0
    assert scorecard.failure_handling_score == 100.0
    assert scorecard.security_score == 100.0
    assert scorecard.observability_score == 100.0


def test_evidence_exporter_generates_all_files(tmp_path):
    runtime = ReadinessRuntime(evidence_dir=str(tmp_path))
    runtime.execute_full_verification()

    expected_files = [
        "readiness_contract_report.json",
        "state_machine_report.json",
        "dependency_policy_report.json",
        "startup_validation_report.json",
        "failure_transition_report.json",
        "orchestration_report.json",
        "certification.json",
        "metadata.json",
    ]

    for fname in expected_files:
        fpath = tmp_path / fname
        assert fpath.exists(), f"Missing expected audit manifest: {fname}"
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert isinstance(data, dict)
