"""
Test Suite: Part 3I Enterprise Observability Infrastructure (Logging & Metrics) Verification
"""
import os
import json
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.observability_infrastructure.domain.models import (
    LogLevel,
    GoldenSignalType,
    AlertSeverity,
    ObservabilityCertificationTier,
    LoggingArchitectureReport,
    StructuredLoggingReport,
    CorrelationReport,
    AIWorkflowLoggingReport,
    SecurityScanReport,
    RetentionReport,
    LogPerformanceReport,
    LoggingPillarScore,
    LoggingCertificationReport,
    MetricInventoryReport,
    GoldenSignalsReport,
    AppInfraMetricsReport,
    SLISLOReport,
    AlertingReport,
    DashboardReport,
    MetricsPerformanceReport,
    MetricsPillarScore,
    MetricsCertificationReport,
    UnifiedObservabilityCertification,
)

from app.platform_verification.observability_infrastructure.logging_verifiers.logging_architecture_verifier import (
    LoggingArchitectureVerifier,
)
from app.platform_verification.observability_infrastructure.logging_verifiers.structured_logging_verifier import (
    StructuredLoggingVerifier,
)
from app.platform_verification.observability_infrastructure.logging_verifiers.correlation_verifier import (
    CorrelationVerifier,
)
from app.platform_verification.observability_infrastructure.logging_verifiers.ai_workflow_logging_verifier import (
    AIWorkflowLoggingVerifier,
)
from app.platform_verification.observability_infrastructure.logging_verifiers.security_scan_verifier import (
    SecurityScanVerifier,
)
from app.platform_verification.observability_infrastructure.logging_verifiers.log_retention_verifier import (
    LogRetentionVerifier,
)
from app.platform_verification.observability_infrastructure.logging_verifiers.log_performance_verifier import (
    LogPerformanceVerifier,
)

from app.platform_verification.observability_infrastructure.metrics_verifiers.metrics_architecture_verifier import (
    MetricsArchitectureVerifier,
)
from app.platform_verification.observability_infrastructure.metrics_verifiers.golden_signals_verifier import (
    GoldenSignalsVerifier,
)
from app.platform_verification.observability_infrastructure.metrics_verifiers.app_infra_metrics_verifier import (
    AppInfraMetricsVerifier,
)
from app.platform_verification.observability_infrastructure.metrics_verifiers.sli_slo_verifier import (
    SLISLOVerifier,
)
from app.platform_verification.observability_infrastructure.metrics_verifiers.alerting_verifier import (
    AlertingVerifier,
)
from app.platform_verification.observability_infrastructure.metrics_verifiers.dashboard_verifier import (
    DashboardVerifier,
)
from app.platform_verification.observability_infrastructure.metrics_verifiers.metrics_performance_verifier import (
    MetricsPerformanceVerifier,
)

from app.platform_verification.observability_infrastructure.scoring.logging_quality_scorer import (
    LoggingQualityScorer,
)
from app.platform_verification.observability_infrastructure.scoring.metrics_quality_scorer import (
    MetricsQualityScorer,
)
from app.platform_verification.observability_infrastructure.scoring.observability_composite_scorer import (
    ObservabilityCompositeScorer,
)
from app.platform_verification.observability_infrastructure.exporter.observability_exporter import (
    ObservabilityExporter,
)
from app.platform_verification.observability_infrastructure.runtime.observability_runtime import (
    ObservabilityRuntime,
)
from app.platform_verification.observability_infrastructure.api.observability_api import (
    router,
)


@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestLoggingVerifiers:
    def test_logging_architecture(self):
        verifier = LoggingArchitectureVerifier()
        report = verifier.verify_logging_architecture()
        assert report.architecture_valid is True
        assert len(report.collectors) >= 3
        assert len(report.sink_backends) >= 2

    def test_structured_logging(self):
        verifier = StructuredLoggingVerifier()
        report = verifier.verify_structured_logging()
        assert report.structured_logging_passed is True
        assert report.schema_compliance_pct == 100.0
        assert report.plain_text_rejected is True
        assert len(report.mandatory_fields_verified) == 9

    def test_correlation(self):
        verifier = CorrelationVerifier()
        report = verifier.verify_correlation()
        assert report.lifecycle_complete is True
        assert report.correlation_fidelity_pct == 100.0
        assert len(report.lifecycle_hops) == 10
        assert report.lifecycle_request_id == "REQ-98273"

    def test_ai_workflow_logging(self):
        verifier = AIWorkflowLoggingVerifier()
        report = verifier.verify_ai_workflow_logging()
        assert report.ai_observability_passed is True
        assert len(report.agent_lifecycle_events_logged) >= 5
        assert len(report.ocr_events_logged) >= 3
        assert len(report.llm_telemetry_tracked) >= 6

    def test_security_scan(self):
        verifier = SecurityScanVerifier()
        report = verifier.verify_security_scanning()
        assert report.security_logging_passed is True
        assert report.leakage_incidents_detected == 0
        assert report.masking_compliance_pct == 100.0

    def test_log_retention(self):
        verifier = LogRetentionVerifier()
        report = verifier.verify_retention()
        assert report.retention_policy_passed is True
        assert report.application_log_retention_days == 30
        assert report.security_log_retention_days == 180
        assert report.audit_log_retention_days == 365

    def test_log_performance(self):
        verifier = LogPerformanceVerifier()
        report = verifier.verify_log_performance()
        assert report.performance_passed is True
        assert report.logging_overhead_pct < 1.0
        assert report.mean_processing_latency_ms < 1.0


class TestMetricsVerifiers:
    def test_metrics_architecture(self):
        verifier = MetricsArchitectureVerifier()
        report = verifier.verify_metrics_architecture()
        assert report.prometheus_scraping_active is True
        assert report.total_metrics_registered >= 15

    def test_golden_signals(self):
        verifier = GoldenSignalsVerifier()
        report = verifier.verify_golden_signals()
        assert report.golden_signals_complete is True
        assert report.latency_tracked is True
        assert report.traffic_tracked is True
        assert report.errors_tracked is True
        assert report.saturation_tracked is True

    def test_app_infra_metrics(self):
        verifier = AppInfraMetricsVerifier()
        report = verifier.verify_app_infra_metrics()
        assert report.telemetry_coverage_passed is True
        assert report.document_metrics_active is True
        assert report.ocr_metrics_active is True
        assert report.ai_llm_metrics_active is True
        assert report.database_connection_metrics_active is True

    def test_sli_slo(self):
        verifier = SLISLOVerifier()
        report = verifier.verify_sli_slo()
        assert report.all_slos_met is True
        assert len(report.indicators) >= 4
        for sli in report.indicators:
            assert sli.status == "COMPLIANT"
            assert sli.achieved_sli_pct >= sli.target_slo_pct

    def test_alerting(self):
        verifier = AlertingVerifier()
        report = verifier.verify_alerting()
        assert report.alerting_system_verified is True
        assert report.total_alert_rules >= 6
        for rule in report.rules:
            assert rule.has_runbook_link is True
            assert rule.has_root_cause_hint is True

    def test_dashboards(self):
        verifier = DashboardVerifier()
        report = verifier.verify_dashboards()
        assert report.dashboards_coverage_passed is True
        assert len(report.dashboards) == 3

    def test_metrics_performance(self):
        verifier = MetricsPerformanceVerifier()
        report = verifier.verify_metrics_performance()
        assert report.metrics_resilience_passed is True
        assert report.scrape_duration_ms < 50.0
        assert report.metrics_data_integrity_pct == 100.0


class TestScorersAndExporter:
    def test_scorers_and_export(self, tmp_path):
        runtime = ObservabilityRuntime()
        export_dir = str(tmp_path / "observability_artifacts")
        res = runtime.run_full_verification(export_base_dir=export_dir)

        log_cert = res["logging"]["certification"]
        met_cert = res["metrics"]["certification"]
        uni_cert = res["unified_certification"]

        assert log_cert.overall_score_pct >= 95.0
        assert log_cert.certification_tier == "Enterprise Logging Ready"
        assert log_cert.certification_granted is True

        assert met_cert.overall_score_pct >= 95.0
        assert met_cert.certification_tier == "Enterprise Metrics Ready"
        assert met_cert.certification_granted is True

        assert uni_cert.overall_score_pct >= 95.0
        assert uni_cert.certification_tier == ObservabilityCertificationTier.ENTERPRISE_OBSERVABILITY_CERTIFIED
        assert uni_cert.certification_granted is True

        # Check export directory files
        assert os.path.exists(os.path.join(export_dir, "logging", "metadata.json"))
        assert os.path.exists(os.path.join(export_dir, "metrics", "metadata.json"))
        assert os.path.exists(os.path.join(export_dir, "unified_certification.json"))
        assert os.path.exists(os.path.join(export_dir, "metadata.json"))


class TestFastAPIRoutes:
    def test_all_endpoints(self, api_client):
        # /health
        res = api_client.get("/api/v1/observability/health")
        assert res.status_code == 200
        assert res.json()["status"] == "HEALTHY"

        # /verify
        res = api_client.post("/api/v1/observability/verify")
        assert res.status_code == 200
        assert res.json()["status"] == "COMPLETED"
        assert res.json()["overall_score_pct"] >= 95.0

        # /scorecard
        res = api_client.get("/api/v1/observability/scorecard")
        assert res.status_code == 200
        assert "unified_certification" in res.json()
        assert "logging_scorecard" in res.json()
        assert "metrics_scorecard" in res.json()

        # /logging/correlation
        res = api_client.get("/api/v1/observability/logging/correlation")
        assert res.status_code == 200
        assert res.json()["lifecycle_complete"] is True

        # /logging/security
        res = api_client.get("/api/v1/observability/logging/security")
        assert res.status_code == 200
        assert res.json()["security_logging_passed"] is True

        # /metrics/golden-signals
        res = api_client.get("/api/v1/observability/metrics/golden-signals")
        assert res.status_code == 200
        assert res.json()["golden_signals_complete"] is True

        # /metrics/sli-slo
        res = api_client.get("/api/v1/observability/metrics/sli-slo")
        assert res.status_code == 200
        assert res.json()["all_slos_met"] is True

        # /metrics/dashboards
        res = api_client.get("/api/v1/observability/metrics/dashboards")
        assert res.status_code == 200
        assert res.json()["dashboards_coverage_passed"] is True
