"""
Phase 3H.7: Comprehensive Test Suite for Enterprise Operational Resilience, Fault Tolerance & Self-Healing Verification
"""
import pytest
from fastapi.testclient import TestClient

from app.platform_verification.operational_resilience.domain.models import (
    CircuitBreakerState,
    DegradationMode,
    OperationalResilienceTier,
)
from app.platform_verification.operational_resilience.verifiers import (
    ResilienceArchitectureVerifier,
    CircuitBreakerVerifier,
    RetryStrategyVerifier,
    GracefulDegradationVerifier,
    BulkheadIsolationVerifier,
    LoadSheddingVerifier,
    SelfHealingVerifier,
    ChaosResilienceVerifier,
    BusinessContinuityVerifier,
    ResilienceMetricsVerifier,
)
from app.platform_verification.operational_resilience.scoring import OperationalResilienceScorer
from app.platform_verification.operational_resilience.runtime import OperationalResilienceRuntime
from app.platform_verification.operational_resilience.api import router
from fastapi import FastAPI


@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_resilience_architecture_verification():
    verifier = ResilienceArchitectureVerifier()
    report = verifier.verify_resilience_architecture()

    assert report.total_strategies_defined == 6
    assert len(report.strategies) == 6
    assert report.architecture_certified is True

    strategy_ids = [s.strategy_id for s in report.strategies]
    assert "STRAT-CB-001" in strategy_ids
    assert "STRAT-RETRY-002" in strategy_ids
    assert "STRAT-DEGRADE-003" in strategy_ids
    assert "STRAT-BULKHEAD-004" in strategy_ids
    assert "STRAT-SHED-005" in strategy_ids
    assert "STRAT-HEAL-006" in strategy_ids

    for strat in report.strategies:
        assert strat.is_active is True
        assert len(strat.observability_hooks) > 0
        assert len(strat.dependencies) > 0


def test_circuit_breaker_protection():
    verifier = CircuitBreakerVerifier()
    report = verifier.verify_circuit_breakers()

    assert report.total_circuit_breakers == 5
    assert report.all_circuit_breakers_active is True
    subsystems = [b.subsystem for b in report.breakers]
    assert "Gemini_AI_Provider" in subsystems
    assert "Tesseract_OCR_Engine" in subsystems
    assert "PostgreSQL_Database" in subsystems
    assert "Redis_Cache_and_Queue" in subsystems
    assert "External_Customer_Webhooks" in subsystems

    for breaker in report.breakers:
        assert breaker.state == CircuitBreakerState.CLOSED
        assert breaker.auto_reset_verified is True
        assert breaker.is_operational is True


def test_retry_strategy_governance():
    verifier = RetryStrategyVerifier()
    report = verifier.verify_retry_strategies()

    assert report.total_retry_policies == 6
    assert report.retry_governance_compliant is True

    for policy in report.policies:
        assert policy.max_retries >= 2
        assert policy.jitter_applied is True
        assert policy.retry_budget_enforced is True
        assert policy.dlq_routing_verified is True
        assert policy.is_idempotent is True


def test_graceful_degradation_modes():
    verifier = GracefulDegradationVerifier()
    report = verifier.verify_graceful_degradation()

    assert report.total_degradation_modes == 4
    assert report.graceful_degradation_verified is True

    modes = [s.degraded_mode for s in report.scenarios]
    assert DegradationMode.DB_READ_ONLY in modes
    assert DegradationMode.AI_FALLBACK_CACHED in modes
    assert DegradationMode.AI_OFFLINE_BUFFERED in modes
    assert DegradationMode.OCR_NATIVE_PDF_FALLBACK in modes

    for scenario in report.scenarios:
        assert scenario.user_messaging_sanitized is True
        assert scenario.audit_trail_recorded is True
        assert scenario.recovery_transition_automatic is True
        assert scenario.is_resilient is True


def test_bulkhead_resource_isolation():
    verifier = BulkheadIsolationVerifier()
    report = verifier.verify_bulkhead_isolation()

    assert report.total_isolated_pools == 6
    assert report.fault_containment_verified is True

    for pool in report.pools:
        assert pool.max_threads_or_workers > 0
        assert pool.queue_capacity > 0
        assert pool.isolated_from_other_pools is True
        assert pool.saturation_contained is True


def test_adaptive_load_shedding():
    verifier = LoadSheddingVerifier()
    report = verifier.verify_load_shedding()

    assert report.overload_protection_active is True
    assert report.cpu_pressure_threshold_pct == 85.0
    assert report.memory_pressure_threshold_pct == 90.0

    critical_decisions = [
        d for d in report.decisions if "P0" in d.traffic_priority_level
    ]
    assert len(critical_decisions) >= 2
    for d in critical_decisions:
        assert d.decision_under_stress == "ACCEPTED"
        assert d.critical_path_preserved is True


def test_self_healing_capabilities():
    verifier = SelfHealingVerifier()
    report = verifier.verify_self_healing_capabilities()

    assert report.total_scenarios_verified == 5
    assert report.stale_lock_cleanup_active is True
    assert report.orphan_task_recovery_active is True
    assert report.zero_manual_intervention_required is True

    for scenario in report.scenarios:
        assert scenario.resolution_latency_seconds < 10.0
        assert scenario.verification_passed is True


def test_chaos_resilience_experiments():
    verifier = ChaosResilienceVerifier()
    report = verifier.execute_chaos_validation()

    assert report.total_chaos_experiments == 6
    assert report.passed_experiments_count == 6
    assert report.chaos_resilience_certified is True

    for exp in report.experiments:
        assert exp.service_continuity_maintained is True
        assert exp.zero_data_loss_verified is True
        assert exp.recovery_duration_seconds < 5.0


def test_business_continuity_preservation():
    verifier = BusinessContinuityVerifier()
    report = verifier.verify_business_continuity()

    assert report.total_stages_audited == 4
    assert report.zero_document_loss_guaranteed is True

    for check in report.checks:
        assert check.documents_preserved_during_outage is True
        assert check.offline_buffering_active is True
        assert check.resumable_after_reconnection is True
        assert check.operator_reconciliation_available is True


def test_resilience_metrics_collection():
    verifier = ResilienceMetricsVerifier()
    report = verifier.collect_resilience_metrics()

    assert len(report.metrics) == 6
    assert report.telemetry_pipeline_operational is True

    metric_names = [m.metric_name for m in report.metrics]
    assert "resilience.circuit_breaker.tripped_total" in metric_names
    assert "resilience.self_healing.mean_recovery_time_seconds" in metric_names
    assert "resilience.chaos.success_rate_pct" in metric_names


def test_operational_resilience_scorer():
    arch = ResilienceArchitectureVerifier().verify_resilience_architecture()
    cb = CircuitBreakerVerifier().verify_circuit_breakers()
    retry = RetryStrategyVerifier().verify_retry_strategies()
    degrade = GracefulDegradationVerifier().verify_graceful_degradation()
    bulkhead = BulkheadIsolationVerifier().verify_bulkhead_isolation()
    shed = LoadSheddingVerifier().verify_load_shedding()
    self_heal = SelfHealingVerifier().verify_self_healing_capabilities()
    chaos = ChaosResilienceVerifier().execute_chaos_validation()
    continuity = BusinessContinuityVerifier().verify_business_continuity()
    metrics = ResilienceMetricsVerifier().collect_resilience_metrics()

    scorer = OperationalResilienceScorer()
    scorecard = scorer.calculate_scorecard(
        arch_report=arch,
        cb_report=cb,
        retry_report=retry,
        degrade_report=degrade,
        bulkhead_report=bulkhead,
        shed_report=shed,
        self_healing_report=self_heal,
        chaos_report=chaos,
        continuity_report=continuity,
        metrics_report=metrics,
    )

    assert scorecard.overall_resilience_score >= 98.0
    assert scorecard.certification_tier == OperationalResilienceTier.ENTERPRISE_AUTONOMOUS_RESILIENCE
    assert scorecard.passed is True
    assert len(scorecard.pillar_scores) == 7
    assert scorecard.automatic_recovery_rate_pct == 100.0
    assert scorecard.business_continuity_guaranteed is True


def test_evidence_exporter_and_signatures(tmp_path):
    runtime = OperationalResilienceRuntime(output_dir=tmp_path)
    result = runtime.run_full_verification(export_evidence=True)
    meta = result["export_metadata"]

    assert meta is not None
    assert meta["total_reports_exported"] == 11
    assert meta["overall_resilience_score"] >= 98.0
    assert meta["status"] == "PASSED"

    expected_files = [
        "resilience_architecture_report.json",
        "circuit_breaker_report.json",
        "retry_strategy_report.json",
        "graceful_degradation_report.json",
        "bulkhead_report.json",
        "load_shedding_report.json",
        "self_healing_report.json",
        "chaos_resilience_report.json",
        "business_continuity_report.json",
        "resilience_metrics_report.json",
        "resilience_certification_report.json",
        "metadata.json",
    ]

    for f in expected_files:
        p = tmp_path / f
        assert p.exists()
        assert p.stat().st_size > 0


def test_fastapi_endpoints(api_client):
    # GET /health
    resp = api_client.get("/api/v1/platform-verification/operational-resilience/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "HEALTHY"

    # GET /strategies
    resp = api_client.get("/api/v1/platform-verification/operational-resilience/strategies")
    assert resp.status_code == 200
    assert resp.json()["total_strategies_defined"] == 6

    # GET /circuit-breakers
    resp = api_client.get("/api/v1/platform-verification/operational-resilience/circuit-breakers")
    assert resp.status_code == 200
    assert resp.json()["total_circuit_breakers"] == 5

    # GET /metrics
    resp = api_client.get("/api/v1/platform-verification/operational-resilience/metrics")
    assert resp.status_code == 200
    assert len(resp.json()["metrics"]) == 6

    # GET /scorecard
    resp = api_client.get("/api/v1/platform-verification/operational-resilience/scorecard")
    assert resp.status_code == 200
    assert resp.json()["scorecard"]["overall_resilience_score"] >= 98.0

    # POST /verify
    resp = api_client.post("/api/v1/platform-verification/operational-resilience/verify?export_evidence=false")
    assert resp.status_code == 200
    assert resp.json()["status"] == "SUCCESS"
    assert resp.json()["summary"]["overall_score"] >= 98.0
