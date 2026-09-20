"""
Pytest Test Suite for Part 3H.3.3: Enterprise Health State Transition & Service Recovery Intelligence Framework
"""
import os
import json
import pytest

from app.platform_verification.health_transition_intelligence.domain.models import (
    HealthState,
    DegradationSeverity,
    RecoveryActionType,
    HealthTier,
)
from app.platform_verification.health_transition_intelligence.state_machine.health_state_machine import HealthStateMachine
from app.platform_verification.health_transition_intelligence.signals.health_signal_collector import HealthSignalCollector
from app.platform_verification.health_transition_intelligence.rules.health_rule_engine import HealthRuleEngine
from app.platform_verification.health_transition_intelligence.analysis.degradation_analyzer import DegradationAnalyzer
from app.platform_verification.health_transition_intelligence.history.health_history_storage import HealthHistoryStorage
from app.platform_verification.health_transition_intelligence.flapping.flapping_detector import HealthFlappingDetector
from app.platform_verification.health_transition_intelligence.protection.cascading_failure_protector import CascadingFailureProtector
from app.platform_verification.health_transition_intelligence.recovery.recovery_orchestrator import ServiceRecoveryOrchestrator
from app.platform_verification.health_transition_intelligence.orchestration.k8s_transition_verifier import KubernetesTransitionVerifier
from app.platform_verification.health_transition_intelligence.alerting.health_alerting_engine import HealthAlertingEngine
from app.platform_verification.health_transition_intelligence.incident.incident_reconstruction_engine import IncidentReconstructionEngine
from app.platform_verification.health_transition_intelligence.simulation.health_simulation_runner import HealthSimulationRunner
from app.platform_verification.health_transition_intelligence.scoring.health_intelligence_scorer import HealthIntelligenceScorer
from app.platform_verification.health_transition_intelligence.exporter.health_evidence_exporter import HealthEvidenceExporter
from app.platform_verification.health_transition_intelligence.runtime.health_intelligence_runtime import HealthIntelligenceRuntime


def test_health_state_machine():
    sm = HealthStateMachine(service_name="test-service", initial_state=HealthState.STARTING)
    assert sm.current_state == HealthState.STARTING

    # STARTING -> READY
    ev1 = sm.transition(HealthState.READY, "Startup completed")
    assert sm.current_state == HealthState.READY
    assert ev1.previous_state == HealthState.STARTING
    assert ev1.new_state == HealthState.READY

    # READY -> DEGRADED
    sm.transition(HealthState.DEGRADED, "Elevated latency")
    assert sm.current_state == HealthState.DEGRADED

    # DEGRADED -> NOT_READY
    sm.transition(HealthState.NOT_READY, "Database offline")
    assert sm.current_state == HealthState.NOT_READY

    # NOT_READY -> RECOVERING
    sm.transition(HealthState.RECOVERING, "Reconnecting pool")
    assert sm.current_state == HealthState.RECOVERING

    # RECOVERING -> READY
    sm.transition(HealthState.READY, "Warm pool verified")
    assert sm.current_state == HealthState.READY

    # Invalid transition should raise ValueError
    with pytest.raises(ValueError):
        sm.transition(HealthState.STARTING, "Illegal reset")


def test_health_signal_collector():
    collector = HealthSignalCollector(service_name="test-service")
    sig = collector.record_signal("host", "cpu_usage", 45.2, "%")
    assert sig.value == 45.2
    assert sig.unit == "%"

    snapshot = collector.collect_standard_snapshot()
    assert "service" in snapshot
    assert "dependencies" in snapshot
    assert "application" in snapshot
    assert snapshot["service"]["cpu_usage_pct"] > 0


def test_health_rule_engine():
    rule_engine = HealthRuleEngine()

    # Nominal snapshot -> READY
    nominal = {
        "service": {"memory_usage_pct": 60.0, "event_loop_latency_ms": 4.0},
        "dependencies": {"postgres_available": True, "postgres_latency_ms": 10.0, "redis_available": True, "ai_latency_ms": 150.0},
    }
    state_nom, _ = rule_engine.evaluate_signals(nominal)
    assert state_nom == HealthState.READY

    # Database unavailable -> NOT_READY
    db_down = {
        "service": {"memory_usage_pct": 60.0, "event_loop_latency_ms": 4.0},
        "dependencies": {"postgres_available": False, "postgres_latency_ms": 10.0, "redis_available": True, "ai_latency_ms": 150.0},
    }
    state_db, _ = rule_engine.evaluate_signals(db_down)
    assert state_db == HealthState.NOT_READY

    # Memory >95% -> DEGRADED
    mem_high = {
        "service": {"memory_usage_pct": 97.0, "event_loop_latency_ms": 4.0},
        "dependencies": {"postgres_available": True, "postgres_latency_ms": 10.0, "redis_available": True, "ai_latency_ms": 150.0},
    }
    state_mem, _ = rule_engine.evaluate_signals(mem_high)
    assert state_mem == HealthState.DEGRADED


def test_degradation_analyzer():
    analyzer = DegradationAnalyzer()
    report = analyzer.analyze_trends()

    assert report.passed is True
    assert report.condition in ["degrading", "warning", "stable"]
    assert report.confidence >= 0.80
    assert report.slope_rate > 0


def test_health_history_storage():
    storage = HealthHistoryStorage()
    sm = HealthStateMachine(service_name="test-service", initial_state=HealthState.STARTING)
    ev = sm.transition(HealthState.READY, "Started")
    storage.save_event(ev)

    events = storage.get_all_events()
    assert len(events) == 1
    summary = storage.get_transition_summary()
    assert summary["total_events"] == 1


def test_flapping_detector():
    detector = HealthFlappingDetector(max_allowed_transitions=3)

    # 4 quick transitions
    for _ in range(4):
        rep = detector.record_transition(HealthState.READY, HealthState.NOT_READY)

    assert rep.flapping_detected is True
    assert rep.dampening_active is True
    assert rep.suppressed_restart_count >= 1


def test_cascading_failure_protector():
    protector = CascadingFailureProtector(failure_threshold=3)
    assert protector.circuit_state == "CLOSED"

    protector.report_dependency_failure("gemini")
    protector.report_dependency_failure("gemini")
    rep = protector.report_dependency_failure("gemini")

    assert rep.circuit_breaker_state == "OPEN"
    assert rep.fallback_engaged is True
    assert rep.cascading_prevented is True

    protector.record_success()
    assert protector.circuit_state == "CLOSED"


def test_service_recovery_orchestrator():
    orchestrator = ServiceRecoveryOrchestrator(service_name="docutask-api")
    report = orchestrator.execute_and_validate_recovery(from_failure="postgres", simulate_success=True)

    assert report.passed is True
    assert report.recovery_state_reached is True
    assert report.final_state == HealthState.READY
    assert report.all_prerequisites_met is True


def test_kubernetes_transition_verifier():
    verifier = KubernetesTransitionVerifier()
    res = verifier.verify_transition_compatibility()

    assert res["passed"] is True
    assert res["all_transitions_compatible"] is True
    assert res["recovering_state_isolated"] is True
    assert res["ready_state_admitted"] is True


def test_health_alerting_engine():
    engine = HealthAlertingEngine()
    sm = HealthStateMachine(service_name="docutask-api", initial_state=HealthState.READY)
    ev1 = sm.transition(HealthState.NOT_READY, "Critical database disconnect")
    ev2 = sm.transition(HealthState.RECOVERING, "Reconnecting pool")
    ev3 = sm.transition(HealthState.READY, "Validated recovery")

    report = engine.evaluate_events([ev1, ev2, ev3])
    assert report.passed is True
    assert report.critical_alerts_count == 1
    assert report.recovery_alerts_count == 1
    assert report.prometheus_alertmanager_compatible is True


def test_incident_reconstruction_engine():
    reconstructor = IncidentReconstructionEngine()
    timeline = reconstructor.reconstruct_timeline(incident_id="INC-TEST")

    assert timeline.passed is True
    assert timeline.incident_id == "INC-TEST"
    assert len(timeline.timeline_entries) >= 4
    assert timeline.total_duration_seconds > 0


def test_health_simulation_runner():
    runner = HealthSimulationRunner()
    report = runner.run_all_simulations()

    assert report.all_scenarios_passed is True
    assert report.total_scenarios == 4
    assert report.passed_scenarios == 4


def test_health_intelligence_scorer():
    runtime = HealthIntelligenceRuntime()
    results = runtime.execute_full_verification()
    scorecard = results["scorecard"]

    assert scorecard.overall_score >= 95.0
    assert scorecard.certification_tier == HealthTier.ENTERPRISE_READY
    assert scorecard.certification_verdict == "CERTIFIED"
    assert scorecard.passed is True
    assert scorecard.state_accuracy_score == 100.0
    assert scorecard.transition_logic_score == 100.0
    assert scorecard.failure_detection_score == 100.0
    assert scorecard.recovery_validation_score == 100.0
    assert scorecard.alerting_score == 100.0
    assert scorecard.evidence_quality_score == 100.0


def test_health_evidence_exporter(tmp_path):
    runtime = HealthIntelligenceRuntime(evidence_dir=str(tmp_path))
    results = runtime.execute_full_verification()

    expected_files = [
        "state_machine_report.json",
        "transition_history.json",
        "degradation_report.json",
        "recovery_report.json",
        "flapping_report.json",
        "incident_timeline.json",
        "alerting_report.json",
        "metadata.json",
    ]

    for fname in expected_files:
        fpath = tmp_path / fname
        assert fpath.exists(), f"Missing expected audit manifest: {fname}"
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert isinstance(data, dict)
