"""
Phase 3I.3: Enterprise Metrics Infrastructure Verification - Unit and Integration Tests
"""
import os
import json
import hashlib
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.metrics_infrastructure.domain.models import (
    MetricType,
    MetricsCertificationTier,
    MetricsServiceCoverage,
    MetricsArchitectureReport,
    MetricDefinitionSpec,
    MetricsCertificationReport,
)
from app.platform_verification.metrics_infrastructure.verifiers.metrics_architecture_verifier import MetricsArchitectureVerifier
from app.platform_verification.metrics_infrastructure.verifiers.metrics_standard_verifier import MetricsStandardVerifier
from app.platform_verification.metrics_infrastructure.verifiers.application_metrics_verifier import ApplicationMetricsVerifier
from app.platform_verification.metrics_infrastructure.verifiers.ai_metrics_verifier import AIMetricsVerifier
from app.platform_verification.metrics_infrastructure.verifiers.infrastructure_metrics_verifier import InfrastructureMetricsVerifier
from app.platform_verification.metrics_infrastructure.verifiers.business_sla_metrics_verifier import BusinessSLAMetricsVerifier
from app.platform_verification.metrics_infrastructure.verifiers.metrics_dashboard_verifier import MetricsDashboardVerifier
from app.platform_verification.metrics_infrastructure.verifiers.alert_metric_verifier import AlertMetricVerifier
from app.platform_verification.metrics_infrastructure.verifiers.metrics_accuracy_verifier import MetricsAccuracyVerifier
from app.platform_verification.metrics_infrastructure.verifiers.metrics_security_verifier import MetricsSecurityVerifier
from app.platform_verification.metrics_infrastructure.verifiers.metrics_performance_verifier import MetricsPerformanceVerifier
from app.platform_verification.metrics_infrastructure.verifiers.failure_simulation_metrics_verifier import FailureSimulationMetricsVerifier
from app.platform_verification.metrics_infrastructure.scoring.metrics_quality_scorer import MetricsQualityScorer
from app.platform_verification.metrics_infrastructure.runtime.metrics_verification_runtime import MetricsVerificationRuntime
from app.platform_verification.metrics_infrastructure.api.metrics_verification_api import router as metrics_api_router


# ─── 1. Domain Models Tests ───────────────────────────────────────────────────

def test_domain_models_instantiation():
    arch = MetricsArchitectureReport(
        services_monitored=8,
        services_coverage=[
            MetricsServiceCoverage(service_name="api_gateway", metrics_endpoint="/metrics", scrape_interval_seconds=15)
        ]
    )
    assert arch.services_monitored == 8
    assert arch.collector == "OpenTelemetry"
    assert arch.storage == "Prometheus"

    metric_def = MetricDefinitionSpec(
        metric_name="document_processing_duration_seconds",
        metric_type=MetricType.HISTOGRAM,
        description="Duration of document processing",
        unit="seconds",
        labels=["document_type", "status"]
    )
    assert metric_def.metric_type == MetricType.HISTOGRAM

    cert_rep = MetricsCertificationReport(
        certification_tier=MetricsCertificationTier.ENTERPRISE_METRICS_READY,
        overall_score_pct=98.0
    )
    assert cert_rep.certification_granted is True
    assert cert_rep.certification_tier == MetricsCertificationTier.ENTERPRISE_METRICS_READY


# ─── 2. Architecture Verifier Tests ───────────────────────────────────────────

def test_metrics_architecture_verifier():
    verifier = MetricsArchitectureVerifier()
    report = verifier.verify_metrics_architecture()

    assert report.status == "PASS"
    assert report.services_monitored == 8
    assert len(report.services_coverage) == 8
    assert report.collector == "OpenTelemetry"
    assert report.storage == "Prometheus"

    service_names = [s.service_name for s in report.services_coverage]
    assert "api_gateway" in service_names
    assert "gemini_llm_gateway" in service_names
    assert "postgresql_primary_db" in service_names


# ─── 3. Standard Verifier Tests ───────────────────────────────────────────────

def test_metrics_standard_verifier():
    verifier = MetricsStandardVerifier()
    report = verifier.verify_metrics_standard()

    assert report.standard_validation_passed is True
    assert report.naming_standard_compliance_pct == 100.0
    assert len(report.metric_definitions) >= 20

    types_found = {m.metric_type for m in report.metric_definitions}
    assert MetricType.COUNTER in types_found
    assert MetricType.GAUGE in types_found
    assert MetricType.HISTOGRAM in types_found
    assert MetricType.SUMMARY in types_found

    # Check snake_case and units in metric names
    for m in report.metric_definitions:
        assert m.metric_name.islower()
        assert m.naming_convention_valid is True
        assert len(m.description) > 0


# ─── 4. Application Metrics Verifier Tests ────────────────────────────────────

def test_application_metrics_verifier():
    verifier = ApplicationMetricsVerifier()
    report = verifier.verify_application_metrics()

    assert report.application_metrics_healthy is True
    assert report.total_system_requests > 0
    assert report.overall_p95_latency_ms < 500.0
    assert report.overall_error_rate_pct < 1.0
    assert len(report.endpoints) >= 3


# ─── 5. AI Agent & LLM Metrics Verifier Tests ─────────────────────────────────

def test_ai_metrics_verifier():
    verifier = AIMetricsVerifier()
    report = verifier.verify_ai_metrics()

    assert report.ai_observability_score == 100.0
    assert len(report.agent_metrics) >= 2
    assert len(report.llm_metrics) >= 2

    # Check agent telemetry
    for ag in report.agent_metrics:
        assert ag.tasks_completed > 0
        assert ag.tool_calls_total > 0
        assert ag.success_rate_pct >= 95.0
        assert ag.reflection_cycles_total > 0

    # Check LLM provider telemetry
    for llm in report.llm_metrics:
        assert llm.total_requests > 0
        assert llm.total_input_tokens > 0
        assert llm.total_output_tokens > 0
        assert llm.total_estimated_cost_usd > 0
        assert llm.cost_per_document_usd > 0


# ─── 6. Infrastructure, Queue & DB Metrics Verifier Tests ─────────────────────

def test_infrastructure_metrics_verifier():
    verifier = InfrastructureMetricsVerifier()
    report = verifier.verify_infrastructure_metrics()

    assert report.infrastructure_healthy is True

    # Queue checks
    assert report.queue_metrics.queue_depth > 0
    assert report.queue_metrics.jobs_completed_per_second > 0
    assert report.queue_metrics.saturation_risk == "LOW"

    # Worker checks
    assert report.worker_metrics.workers_active > 0
    assert report.worker_metrics.zombie_workers_detected == 0
    assert report.worker_metrics.heartbeat_healthy is True

    # Database checks
    assert report.database_metrics.active_connections < report.database_metrics.max_connections
    assert report.database_metrics.connection_exhaustion_risk == "NONE"
    assert report.database_metrics.database_errors_total == 0

    # Container checks
    assert len(report.container_resources) >= 6
    for c in report.container_resources:
        assert c.memory_leak_detected is False


# ─── 7. Business & SLA Metrics Verifier Tests ─────────────────────────────────

def test_business_sla_metrics_verifier():
    verifier = BusinessSLAMetricsVerifier()
    report = verifier.verify_business_sla_metrics()

    assert report.business_health == "EXCELLENT"
    assert report.documents_uploaded_total == 10000
    assert report.documents_processed_total == 9850
    assert report.average_confidence_score > 0.95
    assert report.sla_compliance_rate_pct >= 95.0


# ─── 8. Dashboard Verifier Tests ──────────────────────────────────────────────

def test_metrics_dashboard_verifier():
    verifier = MetricsDashboardVerifier()
    report = verifier.verify_dashboards()

    assert report.all_dashboards_operational is True
    assert len(report.dashboards) == 4

    dash_ids = [d.dashboard_id for d in report.dashboards]
    assert "dash_system_overview" in dash_ids
    assert "dash_ai_agents" in dash_ids
    assert "dash_queue_processing" in dash_ids
    assert "dash_database_postgresql" in dash_ids

    for d in report.dashboards:
        assert d.panels_count == len(d.panels)
        assert d.panels_count > 0


# ─── 9. Alert Metric Verifier Tests ───────────────────────────────────────────

def test_alert_metric_verifier():
    verifier = AlertMetricVerifier()
    report = verifier.verify_alert_metrics()

    assert report.alerting_pipeline_verified is True
    assert len(report.rules_validated) >= 5

    alert_names = [r.alert_name for r in report.rules_validated]
    assert "QueueSaturationWarning" in alert_names
    assert "HighHttpErrorRateCritical" in alert_names
    assert "LatencySlaDegradation" in alert_names
    assert "DatabaseConnectionExhaustionRisk" in alert_names


# ─── 10. Accuracy & Security Verifier Tests ───────────────────────────────────

def test_metrics_accuracy_verifier():
    verifier = MetricsAccuracyVerifier()
    report = verifier.verify_metrics_accuracy()

    assert report.drift_free is True
    assert report.accuracy_pct == 100.0
    for sim in report.simulations:
        assert sim.drift_detected is False
        assert (sim.metric_counter_after - sim.metric_counter_before) == sim.simulated_events_count


def test_metrics_security_verifier():
    verifier = MetricsSecurityVerifier()
    report = verifier.verify_metrics_security()

    assert report.security_compliant is True
    assert report.endpoint_authentication_enforced is True
    assert report.no_pii_in_labels is True
    for audit in report.audits:
        assert audit.pii_exposed is False
        assert audit.secrets_exposed is False
        assert audit.status == "SECURE"


# ─── 11. Performance & Failure Simulation Verifier Tests ──────────────────────

def test_metrics_performance_verifier():
    verifier = MetricsPerformanceVerifier()
    report = verifier.verify_metrics_performance()

    assert report.overhead_compliant is True
    assert report.cpu_overhead_pct < 3.0
    assert report.collector_latency_p99_ms < 5.0
    assert report.stress_events_per_minute == 100000


def test_failure_simulation_metrics_verifier():
    verifier = FailureSimulationMetricsVerifier()
    report = verifier.verify_failure_simulation_metrics()

    assert report.all_scenarios_verified is True
    assert len(report.scenarios) == 3

    scenario_ids = [s.scenario_id for s in report.scenarios]
    assert "CHAOS-METRIC-001" in scenario_ids
    assert "CHAOS-METRIC-002" in scenario_ids
    assert "CHAOS-METRIC-003" in scenario_ids

    for sc in report.scenarios:
        assert sc.alert_triggered is True
        assert sc.metric_anomaly_detected is True


# ─── 12. Quality Scorer Tests ─────────────────────────────────────────────────

def test_metrics_quality_scorer():
    runtime = MetricsVerificationRuntime()
    arch = runtime.arch_verifier.verify_metrics_architecture()
    std = runtime.std_verifier.verify_metrics_standard()
    app = runtime.app_verifier.verify_application_metrics()
    ai = runtime.ai_verifier.verify_ai_metrics()
    infra = runtime.infra_verifier.verify_infrastructure_metrics()
    biz = runtime.biz_verifier.verify_business_sla_metrics()
    dash = runtime.dash_verifier.verify_dashboards()
    alert = runtime.alert_verifier.verify_alert_metrics()
    acc = runtime.acc_verifier.verify_metrics_accuracy()
    sec = runtime.sec_verifier.verify_metrics_security()
    perf = runtime.perf_verifier.verify_metrics_performance()
    chaos = runtime.chaos_verifier.verify_failure_simulation_metrics()

    scorer = MetricsQualityScorer()
    certification = scorer.calculate_certification_score(
        arch_report=arch,
        std_report=std,
        app_report=app,
        ai_report=ai,
        infra_report=infra,
        biz_report=biz,
        dash_report=dash,
        alert_report=alert,
        acc_report=acc,
        sec_report=sec,
        perf_report=perf,
        chaos_report=chaos,
    )

    assert certification.overall_score_pct >= 95.0
    assert certification.certification_tier == MetricsCertificationTier.ENTERPRISE_METRICS_READY
    assert certification.certification_granted is True
    assert len(certification.pillar_scores) == 6

    # Verify pillar weights sum to 100%
    total_weight = sum(p.weight_pct for p in certification.pillar_scores)
    assert abs(total_weight - 100.0) < 0.001


# ─── 13. Exporter & Runtime Tests ─────────────────────────────────────────────

def test_metrics_evidence_exporter(tmp_path):
    out_dir = str(tmp_path / "observability_verification" / "metrics")
    runtime = MetricsVerificationRuntime()
    result = runtime.run_full_verification(export_dir=out_dir)

    metadata = result["metadata"]
    assert metadata["services_monitored"] == 8
    assert metadata["total_artifacts"] == 10

    # Verify metadata.json and SHA-256 signatures
    metadata_path = os.path.join(out_dir, "metadata.json")
    assert os.path.exists(metadata_path)

    with open(metadata_path, "r", encoding="utf-8") as f:
        meta_loaded = json.load(f)

    assert "manifest_sha256" in meta_loaded
    for filename, recorded_hash in meta_loaded["manifest_sha256"].items():
        file_path = os.path.join(out_dir, filename)
        assert os.path.exists(file_path)
        with open(file_path, "r", encoding="utf-8") as rf:
            content_str = rf.read()
        computed_hash = hashlib.sha256(content_str.encode("utf-8")).hexdigest()
        assert computed_hash == recorded_hash


# ─── 14. FastAPI Router Tests ─────────────────────────────────────────────────

def test_metrics_verification_api_endpoints():
    app = FastAPI()
    app.include_router(metrics_api_router)
    client = TestClient(app)

    # Health endpoint
    resp = client.get("/api/v1/metrics-verification/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "HEALTHY"

    # Architecture endpoint
    resp = client.get("/api/v1/metrics-verification/architecture")
    assert resp.status_code == 200
    assert resp.json()["services_monitored"] == 8

    # Standards endpoint
    resp = client.get("/api/v1/metrics-verification/standards")
    assert resp.status_code == 200
    assert resp.json()["naming_standard_compliance_pct"] == 100.0

    # Application endpoint
    resp = client.get("/api/v1/metrics-verification/application")
    assert resp.status_code == 200
    assert resp.json()["application_metrics_healthy"] is True

    # AI Agent endpoint
    resp = client.get("/api/v1/metrics-verification/ai-agent")
    assert resp.status_code == 200
    assert resp.json()["ai_observability_score"] == 100.0

    # Infrastructure endpoint
    resp = client.get("/api/v1/metrics-verification/infrastructure")
    assert resp.status_code == 200
    assert resp.json()["infrastructure_healthy"] is True

    # Business SLA endpoint
    resp = client.get("/api/v1/metrics-verification/business-sla")
    assert resp.status_code == 200
    assert resp.json()["business_health"] == "EXCELLENT"

    # Dashboards endpoint
    resp = client.get("/api/v1/metrics-verification/dashboards")
    assert resp.status_code == 200
    assert resp.json()["all_dashboards_operational"] is True

    # Alerts endpoint
    resp = client.get("/api/v1/metrics-verification/alerts")
    assert resp.status_code == 200
    assert resp.json()["alerting_pipeline_verified"] is True

    # Accuracy endpoint
    resp = client.get("/api/v1/metrics-verification/accuracy")
    assert resp.status_code == 200
    assert resp.json()["drift_free"] is True

    # Security endpoint
    resp = client.get("/api/v1/metrics-verification/security")
    assert resp.status_code == 200
    assert resp.json()["security_compliant"] is True

    # Performance endpoint
    resp = client.get("/api/v1/metrics-verification/performance")
    assert resp.status_code == 200
    assert resp.json()["overhead_compliant"] is True

    # Chaos endpoint
    resp = client.get("/api/v1/metrics-verification/chaos")
    assert resp.status_code == 200
    assert resp.json()["all_scenarios_verified"] is True

    # Scorecard endpoint
    resp = client.get("/api/v1/metrics-verification/scorecard")
    assert resp.status_code == 200
    assert resp.json()["overall_score_pct"] >= 95.0

    # Verification run POST endpoint
    resp = client.post("/api/v1/metrics-verification/verify")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "COMPLETED"
    assert data["certification_tier"] == "Enterprise Metrics Ready"
