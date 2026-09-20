"""
Pytest Test Suite for Part 3H.3.2: Enterprise Dependency-Aware Readiness Decision Engine Verification Framework
"""
import os
import json
import pytest

from app.platform_verification.readiness_engine.domain.models import (
    ReadinessState,
    DependencyCriticality,
    TrafficAction,
    WorkerState,
    ReadinessTier,
)
from app.platform_verification.readiness_engine.policy.dependency_policy_engine import DependencyPolicyEngine
from app.platform_verification.readiness_engine.checkers.database_readiness_checker import DatabaseReadinessChecker
from app.platform_verification.readiness_engine.checkers.queue_readiness_checker import QueueReadinessChecker
from app.platform_verification.readiness_engine.checkers.storage_readiness_checker import StorageReadinessChecker
from app.platform_verification.readiness_engine.checkers.ai_readiness_checker import AIProviderReadinessChecker
from app.platform_verification.readiness_engine.checkers.worker_readiness_checker import WorkerReadinessChecker
from app.platform_verification.readiness_engine.aggregator.readiness_evaluator import ReadinessEvaluator
from app.platform_verification.readiness_engine.simulation.readiness_failure_simulator import ReadinessFailureSimulator
from app.platform_verification.readiness_engine.orchestration.k8s_readiness_verifier import KubernetesReadinessVerifier
from app.platform_verification.readiness_engine.security.readiness_security_auditor import ReadinessSecurityAuditor
from app.platform_verification.readiness_engine.observability.readiness_metrics_exporter import ReadinessMetricsExporter
from app.platform_verification.readiness_engine.scoring.readiness_quality_scorer import ReadinessQualityScorer
from app.platform_verification.readiness_engine.exporter.readiness_evidence_writer import ReadinessEvidenceWriter
from app.platform_verification.readiness_engine.runtime.readiness_engine_runtime import ReadinessEngineRuntime


def test_readiness_state_enums_and_models():
    assert len(ReadinessState) == 6
    assert ReadinessState.STARTING.value == "STARTING"
    assert ReadinessState.READY.value == "READY"
    assert ReadinessState.DEGRADED.value == "DEGRADED"
    assert ReadinessState.NOT_READY.value == "NOT_READY"
    assert ReadinessState.RECOVERING.value == "RECOVERING"
    assert ReadinessState.UNKNOWN.value == "UNKNOWN"

    assert DependencyCriticality.CRITICAL.value == "critical"
    assert DependencyCriticality.IMPORTANT.value == "important"
    assert DependencyCriticality.OPTIONAL.value == "optional"

    assert TrafficAction.ALLOW_TRAFFIC.value == "ALLOW_TRAFFIC"
    assert TrafficAction.THROTTLE_TRAFFIC.value == "THROTTLE_TRAFFIC"
    assert TrafficAction.REJECT_TRAFFIC.value == "REJECT_TRAFFIC"


def test_dependency_policy_engine():
    engine = DependencyPolicyEngine()
    assert engine.get_criticality("postgres") == DependencyCriticality.CRITICAL
    assert engine.get_criticality("redis") == DependencyCriticality.CRITICAL
    assert engine.get_criticality("gemini") == DependencyCriticality.IMPORTANT
    assert engine.get_criticality("analytics") == DependencyCriticality.OPTIONAL

    assert engine.get_traffic_action("postgres") == TrafficAction.REJECT_TRAFFIC
    assert engine.get_traffic_action("gemini") == TrafficAction.THROTTLE_TRAFFIC
    assert engine.get_traffic_action("analytics") == TrafficAction.ALLOW_TRAFFIC

    matrix = engine.evaluate_dependencies()
    assert matrix.passed is True
    assert matrix.critical_dependencies_count >= 3
    assert matrix.important_dependencies_count >= 1
    assert matrix.total_dependencies >= 4


def test_database_readiness_checker():
    checker = DatabaseReadinessChecker()
    healthy = checker.check_readiness()
    assert healthy.passed is True
    assert healthy.status == "READY"
    assert healthy.transaction_supported is True
    assert healthy.schema_compatible is True
    assert healthy.pool_exhausted is False
    assert healthy.connections_available > 0

    # Failure mode: disconnected
    failed = checker.check_readiness(override_connected=False)
    assert failed.passed is False
    assert failed.status == "NOT_READY"
    assert failed.connected is False

    # Failure mode: pool exhausted
    exhausted = checker.check_readiness(override_pool_exhausted=True)
    assert exhausted.passed is False
    assert exhausted.status == "NOT_READY"
    assert exhausted.connections_available == 0


def test_queue_readiness_checker():
    checker = QueueReadinessChecker()
    healthy = checker.check_readiness()
    assert healthy.passed is True
    assert healthy.status == "READY"
    assert healthy.ping_pong_ok is True
    assert healthy.enqueue_accessible is True

    # Failure mode: Redis down
    down = checker.check_readiness(override_ping=False)
    assert down.passed is False
    assert down.status == "NOT_READY"

    # Degraded mode: Queue depth overflow
    overflow = checker.check_readiness(override_queue_depth=1500)
    assert overflow.passed is False
    assert overflow.status == "DEGRADED"


def test_storage_readiness_checker():
    checker = StorageReadinessChecker()
    healthy = checker.check_readiness()
    assert healthy.passed is True
    assert healthy.status == "READY"
    assert healthy.reachable is True
    assert healthy.write_permission is True
    assert healthy.read_permission is True
    assert healthy.integrity_verified is True
    assert healthy.cleanup_verified is True

    # Failure mode: Write denied
    write_failed = checker.check_readiness(override_write=False)
    assert write_failed.passed is False
    assert write_failed.status == "NOT_READY"


def test_ai_provider_readiness_checker():
    checker = AIProviderReadinessChecker()
    healthy = checker.check_readiness()
    assert healthy.passed is True
    assert healthy.status == "READY"
    assert healthy.authenticated is True
    assert healthy.fallback_mode_active is False

    # Degraded mode: Elevated latency & quota low
    degraded = checker.check_readiness(override_latency_ms=3000.0, override_quota_pct=2.0)
    assert degraded.passed is False
    assert degraded.status == "DEGRADED"
    assert degraded.fallback_mode_active is True


def test_worker_readiness_checker():
    checker = WorkerReadinessChecker()
    healthy = checker.check_readiness()
    assert healthy.passed is True
    assert healthy.status == WorkerState.BUSY.value
    assert healthy.can_process_tasks is True

    # Overloaded mode
    overloaded = checker.check_readiness(override_active_jobs=10, override_capacity=10)
    assert overloaded.status == WorkerState.OVERLOADED.value
    assert overloaded.can_process_tasks is False

    # Failed worker mode (stale heartbeat)
    failed = checker.check_readiness(override_heartbeat_age=45.0)
    assert failed.passed is False
    assert failed.status == WorkerState.FAILED.value
    assert failed.can_process_tasks is False


def test_readiness_evaluator():
    evaluator = ReadinessEvaluator()
    db_c = DatabaseReadinessChecker()
    q_c = QueueReadinessChecker()
    st_c = StorageReadinessChecker()
    ai_c = AIProviderReadinessChecker()
    w_c = WorkerReadinessChecker()

    # All healthy -> READY, ALLOW_TRAFFIC
    res_ready = evaluator.evaluate_readiness(
        db_c.check_readiness(),
        q_c.check_readiness(),
        st_c.check_readiness(),
        ai_c.check_readiness(),
        w_c.check_readiness(),
    )
    assert res_ready.state == ReadinessState.READY
    assert res_ready.traffic_action == TrafficAction.ALLOW_TRAFFIC
    assert res_ready.traffic_allowed is True
    assert len(res_ready.failed_dependencies) == 0

    # Critical down (Postgres) -> NOT_READY, REJECT_TRAFFIC
    res_not_ready = evaluator.evaluate_readiness(
        db_c.check_readiness(override_connected=False),
        q_c.check_readiness(),
        st_c.check_readiness(),
        ai_c.check_readiness(),
        w_c.check_readiness(),
    )
    assert res_not_ready.state == ReadinessState.NOT_READY
    assert res_not_ready.traffic_action == TrafficAction.REJECT_TRAFFIC
    assert res_not_ready.traffic_allowed is False
    assert "postgres" in res_not_ready.failed_dependencies

    # Important degraded (Gemini) -> DEGRADED, THROTTLE_TRAFFIC, traffic_allowed is True
    res_degraded = evaluator.evaluate_readiness(
        db_c.check_readiness(),
        q_c.check_readiness(),
        st_c.check_readiness(),
        ai_c.check_readiness(override_latency_ms=3500.0, override_response_valid=False),
        w_c.check_readiness(),
    )
    assert res_degraded.state == ReadinessState.DEGRADED
    assert res_degraded.traffic_action == TrafficAction.THROTTLE_TRAFFIC
    assert res_degraded.traffic_allowed is True
    assert "gemini" in res_degraded.degraded_dependencies


def test_readiness_failure_simulator():
    simulator = ReadinessFailureSimulator()
    report = simulator.run_all_simulations()

    assert report.all_scenarios_passed is True
    assert report.total_scenarios == 4
    assert report.passed_scenarios == 4

    scenario_ids = [s.scenario_id for s in report.scenarios]
    assert "SCENARIO-01" in scenario_ids
    assert "SCENARIO-02" in scenario_ids
    assert "SCENARIO-03" in scenario_ids
    assert "SCENARIO-04" in scenario_ids


def test_kubernetes_readiness_verifier():
    verifier = KubernetesReadinessVerifier()
    report = verifier.verify_kubernetes_compatibility()

    assert report.passed is True
    assert report.readiness_probe_path == "/ready"
    assert report.fast_response is True
    assert report.latency_ms < 100.0
    assert report.deterministic_response is True
    assert report.no_side_effects is True


def test_readiness_security_auditor():
    auditor = ReadinessSecurityAuditor()

    # Clean payload
    clean = {
        "service": "docutask-api",
        "state": "READY",
        "traffic_allowed": True,
        "reason": "All systems nominal",
        "checks": {"database": "READY", "queue": "READY"},
    }
    clean_rep = auditor.audit_security(clean)
    assert clean_rep.passed is True
    assert clean_rep.total_leaks_detected == 0

    # Dirty payload containing password and internal IP
    dirty = {
        "service": "docutask-api",
        "database_host": "db.internal.10.0.1.45",
        "password": "supersecretpassword",
        "connection_string": "postgresql://user:pass@192.168.1.10:5432/docutask",
    }
    dirty_rep = auditor.audit_security(dirty)
    assert dirty_rep.passed is False
    assert dirty_rep.total_leaks_detected >= 3


def test_observability_metrics_exporter():
    exporter = ReadinessMetricsExporter()
    exporter.set_readiness_state(ReadinessState.READY)
    exporter.update_dependency_metric("postgres", True, 0.012)
    exporter.update_dependency_metric("redis", True, 0.002)

    prom_text = exporter.generate_prometheus_payload()
    assert "service_readiness_status 1" in prom_text
    assert 'dependency_health_status{dependency="postgres"} 1' in prom_text
    assert "readiness_failure_total" in prom_text
    assert "dependency_latency_seconds" in prom_text

    summary = exporter.get_metrics_summary()
    assert summary["prometheus_compatible"] is True
    assert summary["current_state"] == "READY"


def test_quality_scorer_and_certification():
    runtime = ReadinessEngineRuntime()
    results = runtime.execute_full_verification()
    scorecard = results["scorecard"]

    assert scorecard.overall_readiness_score >= 95.0
    assert scorecard.certification_tier == ReadinessTier.ENTERPRISE_READY
    assert scorecard.certification_verdict == "CERTIFIED"
    assert scorecard.passed is True
    assert scorecard.traffic_admission_safe is True
    assert scorecard.dependency_detection_score == 100.0
    assert scorecard.failure_accuracy_score == 100.0
    assert scorecard.policy_correctness_score == 100.0
    assert scorecard.kubernetes_compatibility_score == 100.0
    assert scorecard.security_score == 100.0
    assert scorecard.observability_score == 100.0


def test_evidence_writer_generates_all_files(tmp_path):
    runtime = ReadinessEngineRuntime(evidence_dir=str(tmp_path))
    results = runtime.execute_full_verification()

    expected_files = [
        "readiness_engine_report.json",
        "dependency_matrix.json",
        "database_readiness.json",
        "queue_readiness.json",
        "storage_readiness.json",
        "ai_provider_readiness.json",
        "failure_tests.json",
        "metadata.json",
    ]

    for fname in expected_files:
        fpath = tmp_path / fname
        assert fpath.exists(), f"Missing expected audit manifest: {fname}"
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert isinstance(data, dict)
