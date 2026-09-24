"""Master Pytest Suite for Phase 3H.3 - Enterprise Readiness Verification Framework."""

import os
import json
from app.platform_verification.enterprise_readiness.domain.models import (
    ReadinessState,
    TrafficAction,
    ReadinessCertificationTier,
)
from app.platform_verification.enterprise_readiness.contract.readiness_contract_verifier import (
    ReadinessContractVerifier,
)
from app.platform_verification.enterprise_readiness.engine.dependency_readiness_engine import (
    DependencyReadinessEngine,
)
from app.platform_verification.enterprise_readiness.database.database_readiness_verifier import (
    DatabaseReadinessVerifier,
)
from app.platform_verification.enterprise_readiness.queue.queue_readiness_verifier import (
    QueueReadinessVerifier,
)
from app.platform_verification.enterprise_readiness.workers.worker_capacity_verifier import (
    WorkerCapacityVerifier,
)
from app.platform_verification.enterprise_readiness.ai_provider.ai_provider_readiness_verifier import (
    AIProviderReadinessVerifier,
)
from app.platform_verification.enterprise_readiness.startup.startup_readiness_verifier import (
    StartupReadinessVerifier,
)
from app.platform_verification.enterprise_readiness.simulation.readiness_failure_simulator import (
    ReadinessFailureSimulator,
)
from app.platform_verification.enterprise_readiness.orchestration.orchestrator_integration_verifier import (
    OrchestratorIntegrationVerifier,
)
from app.platform_verification.enterprise_readiness.observability.readiness_observability_exporter import (
    ReadinessObservabilityExporter,
)
from app.platform_verification.enterprise_readiness.runtime.enterprise_readiness_runtime import (
    EnterpriseReadinessRuntime,
)
from app.platform_verification.enterprise_readiness.api.enterprise_readiness_api import (
    get_ready,
    get_readiness_status,
    trigger_readiness_verification,
)


def test_readiness_contract_architecture():
    """Test 3H.3.1 - Readiness Contract Architecture."""
    verifier = ReadinessContractVerifier()
    rep = verifier.verify_contract()

    assert rep.endpoint == "/ready"
    assert rep.status_field_present is True
    assert rep.state_field_present is True
    assert rep.timestamp_present is True
    assert rep.version_present is True
    assert rep.checks_present is True
    assert rep.zero_sensitive_leak is True
    assert rep.deterministic_response is True
    assert rep.status == "PASS"


def test_dependency_readiness_engine():
    """Test 3H.3.2 - Dependency-Aware Readiness Engine."""
    engine = DependencyReadinessEngine()
    db_rep = DatabaseReadinessVerifier().verify_database()
    queue_rep = QueueReadinessVerifier().verify_queue()
    worker_rep = WorkerCapacityVerifier().verify_worker_capacity()
    ai_rep = AIProviderReadinessVerifier().verify_ai_provider()

    rep = engine.evaluate_dependencies(db_rep=db_rep, queue_rep=queue_rep, worker_rep=worker_rep, ai_rep=ai_rep)
    assert rep.total_dependencies == 5
    assert rep.critical_dependencies_count == 4
    assert rep.critical_dependencies_healthy is True
    assert rep.overall_readiness_state == ReadinessState.READY
    assert rep.traffic_decision == TrafficAction.ALLOW_TRAFFIC


def test_database_readiness_verifier():
    """Test 3H.3.3 - Database Readiness Verification."""
    verifier = DatabaseReadinessVerifier()
    rep = verifier.verify_database()

    assert rep.connection_available is True
    assert rep.authentication_valid is True
    assert rep.schema_compatible is True
    assert rep.alembic_migrations_complete is True
    assert rep.transaction_test_passed is True
    assert rep.query_latency_ms < rep.latency_threshold_ms
    assert rep.status == "READY"


def test_queue_readiness_verifier():
    """Test 3H.3.4 - Queue Readiness Verification."""
    verifier = QueueReadinessVerifier()
    rep = verifier.verify_queue(queue_depth_override=200)

    assert rep.redis_ping_pong_ok is True
    assert rep.write_test_passed is True
    assert rep.read_test_passed is True
    assert rep.queue_depth == 200
    assert rep.backlog_status == "READY"
    assert rep.status == "READY"

    # Degraded backlog test (1000 - 10000)
    rep_deg = verifier.verify_queue(queue_depth_override=2500)
    assert rep_deg.backlog_status == "DEGRADED"
    assert rep_deg.status == "DEGRADED"


def test_worker_capacity_verifier():
    """Test 3H.3.5 - Worker Capacity Readiness."""
    verifier = WorkerCapacityVerifier()
    rep = verifier.verify_worker_capacity()

    assert rep.total_registered_workers == 4
    assert rep.active_workers_count == 4
    assert rep.stuck_workers_count == 0
    assert rep.crashed_workers_count == 0
    assert rep.available_fleet_capacity > 0
    assert rep.sufficient_capacity is True
    assert rep.status == "READY"

    # Total failure test
    rep_fail = verifier.verify_worker_capacity(force_all_stopped=True)
    assert rep_fail.active_workers_count == 0
    assert rep_fail.sufficient_capacity is False
    assert rep_fail.status == "NOT_READY"


def test_ai_provider_readiness_verifier():
    """Test 3H.3.6 - AI Provider Readiness Verification."""
    verifier = AIProviderReadinessVerifier()
    rep = verifier.verify_ai_provider()

    assert rep.gemini_auth_valid is True
    assert rep.gemini_reachable is True
    assert rep.quota_headroom_pct > 0.0
    assert rep.status == "READY"

    # Outage -> DEGRADED mode, not crash
    rep_outage = verifier.verify_ai_provider(simulate_outage=True)
    assert rep_outage.status == "DEGRADED"
    assert rep_outage.graceful_degradation_active is True


def test_startup_readiness_verifier():
    """Test 3H.3.7 - Startup Readiness Sequencing & TTR."""
    verifier = StartupReadinessVerifier()
    rep = verifier.verify_startup_sequence()

    assert rep.startup_steps_executed == 7
    assert rep.all_steps_successful is True
    assert rep.pre_initialization_traffic_blocked is True
    assert rep.time_to_ready_seconds <= rep.ttr_threshold_seconds
    assert rep.status == "PASS"


def test_readiness_failure_simulator():
    """Test 3H.3.8 - Controlled Readiness Failure Simulations."""
    simulator = ReadinessFailureSimulator()
    rep = simulator.run_failure_simulations()

    assert rep.total_simulations == 4
    assert rep.passed_simulations == 4
    assert rep.false_positive_rate_pct == 0.0
    assert rep.mean_detection_time_seconds <= 2.0
    assert rep.status == "PASS"


def test_orchestrator_integration_verifier():
    """Test 3H.3.9 - Kubernetes Orchestrator Integration."""
    verifier = OrchestratorIntegrationVerifier()
    rep = verifier.verify_orchestration()

    assert rep.k8s_readiness_probe_path == "/ready"
    assert rep.k8s_port == 8000
    assert rep.traffic_removed_on_failure is True
    assert rep.traffic_restored_on_recovery is True
    assert rep.cloud_lb_compatible is True
    assert rep.status == "PASS"


def test_readiness_observability_exporter():
    """Test 3H.3.10 - Readiness Observability & Prometheus Metrics."""
    exporter = ReadinessObservabilityExporter()
    rep = exporter.export_observability()

    assert rep.metrics_count == 6
    assert "service_readiness_state" in rep.prometheus_metrics_exposed
    assert "dependency_health_status" in rep.prometheus_metrics_exposed
    assert rep.service_readiness_dashboard_ready is True
    assert rep.dependency_dashboard_ready is True
    assert rep.status == "PASS"


def test_readiness_certification_scorer():
    """Test 3H.3.11 - Automated Readiness Certification Scoring."""
    runtime = EnterpriseReadinessRuntime()
    res = runtime.run_full_verification()
    scorecard = res["scorecard"]

    assert scorecard.overall_readiness_score >= 95.0
    assert scorecard.certification_tier == ReadinessCertificationTier.ENTERPRISE_READY
    assert scorecard.certification_verdict == "CERTIFIED"
    assert scorecard.passed is True


def test_readiness_evidence_exporter_all_11_files(tmp_path):
    """Test 3H.3.12 - Exporting all 11 JSON manifests to health_verification/."""
    runtime = EnterpriseReadinessRuntime(export_dir=str(tmp_path))
    res = runtime.run_full_verification()
    manifests = res["exported_manifests"]

    expected_files = [
        "readiness_contract_report.json",
        "dependency_readiness_report.json",
        "database_readiness_report.json",
        "queue_readiness_report.json",
        "worker_readiness_report.json",
        "ai_provider_readiness_report.json",
        "startup_readiness_report.json",
        "failure_simulation_report.json",
        "orchestration_report.json",
        "metrics_report.json",
        "metadata.json",
    ]

    assert len(manifests) == 11
    for fname in expected_files:
        assert fname in manifests
        fpath = manifests[fname]
        assert os.path.exists(fpath)
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert isinstance(data, dict)


def test_enterprise_readiness_api_endpoints():
    """Test FastAPI /ready and health endpoints."""
    ready_resp = get_ready()
    assert ready_resp["status"] == "ready"
    assert ready_resp["state"] == "READY"
    assert "checks" in ready_resp

    status_resp = get_readiness_status()
    assert "scorecard" in status_resp
    assert "dependency_report" in status_resp

    verify_resp = trigger_readiness_verification()
    assert verify_resp["scorecard"]["passed"] is True
    assert len(verify_resp["manifests"]) == 11
