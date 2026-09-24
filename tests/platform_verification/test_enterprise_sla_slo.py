"""
Phase 3J.10: Comprehensive Test Suite for Enterprise Performance SLA, SLO & Continuous Reliability Verification.
"""

import json
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.platform_verification.enterprise_sla_slo_verification.domain.models import (
    BaseVerificationReport,
    CheckResult,
    EnterprisePerformanceReliabilityTier,
    VerificationStatus,
    SLADefinitionReport,
    SLOConfigurationReport,
    ErrorBudgetReport,
    ContinuousMonitoringReport,
    PerformanceRegressionReport,
    EndurancePerformanceReport,
    PerformanceAlertReport,
    PerformanceIncidentReport,
    PerformanceRecoveryReport,
    DashboardValidationReport,
    PerformanceGovernanceReport,
    PerformancePipelineReport,
)
from app.platform_verification.enterprise_sla_slo_verification.verifiers import (
    SLADefinitionVerifier,
    SLOImplementationVerifier,
    ErrorBudgetVerifier,
    ContinuousMonitoringVerifier,
    PerformanceRegressionVerifier,
    LongRunningReliabilityVerifier,
    PerformanceAlertVerifier,
    PerformanceIncidentVerifier,
    PerformanceRecoveryVerifier,
    DashboardValidationVerifier,
    PerformanceGovernanceVerifier,
    CICDPerformancePipelineVerifier,
)
from app.platform_verification.enterprise_sla_slo_verification.scoring.sla_slo_scorer import (
    SLASLOScorer,
)
from app.platform_verification.enterprise_sla_slo_verification.exporter.sla_slo_exporter import (
    SLASLOExporter,
)
from app.platform_verification.enterprise_sla_slo_verification.runtime.sla_slo_runtime import (
    SLASLORuntime,
)
from app.platform_verification.enterprise_sla_slo_verification.api.sla_slo_api import router


class TestEnterpriseSLASLOVerification:
    """Complete test suite for Phase 3J.10."""

    @pytest.fixture
    def app_client(self):
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)

    @pytest.fixture
    def temp_export_dir(self, tmp_path):
        export_path = tmp_path / "test_sla_slo"
        export_path.mkdir(parents=True, exist_ok=True)
        return str(export_path)

    # ──────────────────────────────────────────────────────────────────────────
    # 1. Verifiers Individual Tests (3J.10.1 - 3J.10.12)
    # ──────────────────────────────────────────────────────────────────────────

    def test_3j_10_1_sla_definition_verifier(self):
        verifier = SLADefinitionVerifier()
        assert verifier.verifier_id == "VERIFY-3J.10.1-SLA-DEFINITION"
        assert verifier.phase_id == "3J.10.1"
        report = verifier.verify()
        assert isinstance(report, SLADefinitionReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert all(c.passed for c in report.checks)
        assert report.total_slas_defined == 4
        assert report.api_availability_target == "99.9%"
        assert report.api_p95_latency_target == "<500ms"

    def test_3j_10_2_slo_implementation_verifier(self):
        verifier = SLOImplementationVerifier()
        assert verifier.verifier_id == "VERIFY-3J.10.2-SLO-IMPLEMENTATION"
        assert verifier.phase_id == "3J.10.2"
        report = verifier.verify()
        assert isinstance(report, SLOConfigurationReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert all(c.passed for c in report.checks)
        assert report.availability_slo_pct == 99.9
        assert report.p95_latency_target_ms == 3000.0
        assert len(report.slo_targets) == 4

    def test_3j_10_3_error_budget_verifier(self):
        verifier = ErrorBudgetVerifier()
        assert verifier.verifier_id == "VERIFY-3J.10.3-ERROR-BUDGET"
        assert verifier.phase_id == "3J.10.3"
        report = verifier.verify()
        assert isinstance(report, ErrorBudgetReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.remaining_budget_pct >= 90.0
        assert report.budget_health_status == "HEALTHY"
        assert len(report.service_budgets) == 4

    def test_3j_10_4_continuous_monitoring_verifier(self):
        verifier = ContinuousMonitoringVerifier()
        assert verifier.verifier_id == "VERIFY-3J.10.4-CONTINUOUS-MONITORING"
        assert verifier.phase_id == "3J.10.4"
        report = verifier.verify()
        assert isinstance(report, ContinuousMonitoringReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.latency_stream_active is True
        assert report.throughput_stream_active is True
        assert len(report.metric_streams) == 6

    def test_3j_10_5_performance_regression_verifier(self):
        verifier = PerformanceRegressionVerifier()
        assert verifier.verifier_id == "VERIFY-3J.10.5-REGRESSION-DETECTION"
        assert verifier.phase_id == "3J.10.5"
        report = verifier.verify()
        assert isinstance(report, PerformanceRegressionReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.regression_detected is False
        assert report.confidence_score_pct >= 95.0

    def test_3j_10_6_long_running_reliability_verifier(self):
        verifier = LongRunningReliabilityVerifier()
        assert verifier.verifier_id == "VERIFY-3J.10.6-LONG-RUNNING-RELIABILITY"
        assert verifier.phase_id == "3J.10.6"
        report = verifier.verify()
        assert isinstance(report, EndurancePerformanceReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.test_duration_hours == 72
        assert report.memory_leak_detected is False
        assert report.throughput_decay_pct == 0.0

    def test_3j_10_7_performance_alert_verifier(self):
        verifier = PerformanceAlertVerifier()
        assert verifier.verifier_id == "VERIFY-3J.10.7-PERFORMANCE-ALERTS"
        assert verifier.phase_id == "3J.10.7"
        report = verifier.verify()
        assert isinstance(report, PerformanceAlertReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.latency_alert_verified is True
        assert report.queue_alert_verified is True
        assert len(report.alert_rules) == 4

    def test_3j_10_8_performance_incident_verifier(self):
        verifier = PerformanceIncidentVerifier()
        assert verifier.verifier_id == "VERIFY-3J.10.8-INCIDENT-SIMULATION"
        assert verifier.phase_id == "3J.10.8"
        report = verifier.verify()
        assert isinstance(report, PerformanceIncidentReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.latency_spike_resilience is True
        assert report.queue_growth_resilience is True
        assert len(report.scenarios) == 4

    def test_3j_10_9_performance_recovery_verifier(self):
        verifier = PerformanceRecoveryVerifier()
        assert verifier.verifier_id == "VERIFY-3J.10.9-PERFORMANCE-RECOVERY"
        assert verifier.phase_id == "3J.10.9"
        report = verifier.verify()
        assert isinstance(report, PerformanceRecoveryReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.mttd_mean_seconds < 10.0
        assert report.mttr_mean_seconds < 60.0
        assert report.auto_remediation_success_rate_pct >= 95.0

    def test_3j_10_10_dashboard_validation_verifier(self):
        verifier = DashboardValidationVerifier()
        assert verifier.verifier_id == "VERIFY-3J.10.10-DASHBOARD-VALIDATION"
        assert verifier.phase_id == "3J.10.10"
        report = verifier.verify()
        assert isinstance(report, DashboardValidationReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.system_overview_dashboard_ready is True
        assert len(report.dashboards) == 4

    def test_3j_10_11_performance_governance_verifier(self):
        verifier = PerformanceGovernanceVerifier()
        assert verifier.verifier_id == "VERIFY-3J.10.11-PERFORMANCE-GOVERNANCE"
        assert verifier.phase_id == "3J.10.11"
        report = verifier.verify()
        assert isinstance(report, PerformanceGovernanceReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.governance_enforced is True
        assert report.performance_gates_passed is True

    def test_3j_10_12_cicd_performance_pipeline_verifier(self):
        verifier = CICDPerformancePipelineVerifier()
        assert verifier.verifier_id == "VERIFY-3J.10.12-CICD-PERFORMANCE-PIPELINE"
        assert verifier.phase_id == "3J.10.12"
        report = verifier.verify()
        assert isinstance(report, PerformancePipelineReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.pipeline_automated is True
        assert report.stages_count == 7

    # ──────────────────────────────────────────────────────────────────────────
    # 2. Scoring & Certification Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_sla_slo_scorer_full_pass(self):
        scorer = SLASLOScorer()
        runtime = SLASLORuntime()
        reports = [v.verify() for v in runtime.verifiers]
        scorecard = scorer.score(reports)
        assert scorecard.overall_score == 100.0
        assert (
            scorecard.certification_tier
            == EnterprisePerformanceReliabilityTier.ENTERPRISE_PERFORMANCE_RELIABILITY_READY
        )
        assert scorecard.status == VerificationStatus.PASSED
        assert len(scorecard.categories) == 6

    def test_sla_slo_scorer_degradation(self):
        scorer = SLASLOScorer()
        report = BaseVerificationReport(
            verifier_id="VERIFY-3J.10.1-SLA-DEFINITION",
            phase_id="3J.10.1",
            phase_name="SLA Test",
            checks=[
                CheckResult(name="c1", passed=False, details="fail"),
                CheckResult(name="c2", passed=False, details="fail"),
            ],
        )
        scorecard = scorer.score([report])
        assert scorecard.overall_score < 100.0

    # ──────────────────────────────────────────────────────────────────────────
    # 3. Exporter & Artifact Integrity Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_sla_slo_exporter(self, temp_export_dir):
        exporter = SLASLOExporter(export_dir=temp_export_dir)
        verifier = SLADefinitionVerifier()
        report = verifier.verify()
        paths = exporter.export_report(report)
        assert len(paths) >= 1
        for p in paths:
            assert p.exists()
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert data["phase_id"] == "3J.10.1"

        scorer = SLASLOScorer()
        scorecard = scorer.score([report])
        sc_paths = exporter.export_scorecard(scorecard)
        for p in sc_paths:
            assert p.exists()

        manifest = exporter.generate_manifest(scorecard, [report])
        assert manifest.system == "DocuTask Agent"
        assert len(manifest.files) >= len(paths) + len(sc_paths)

    # ──────────────────────────────────────────────────────────────────────────
    # 4. Runtime Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_sla_slo_runtime_execution(self, temp_export_dir):
        runtime = SLASLORuntime(export_dir=temp_export_dir)
        result = runtime.run_all()
        assert result["status"] == "PASSED"
        assert result["overall_score"] == 100.0
        assert len(result["reports"]) == 12
        assert result["manifest"] is not None

        single = runtime.run_verifier("VERIFY-3J.10.1-SLA-DEFINITION")
        assert single is not None
        assert single.phase_id == "3J.10.1"

    # ──────────────────────────────────────────────────────────────────────────
    # 5. REST API Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_api_health_endpoint(self, app_client):
        response = app_client.get("/api/v1/sla-slo/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["phase"] == "3J.10"

    def test_api_status_endpoint(self, app_client):
        response = app_client.get("/api/v1/sla-slo/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert data["total_verifiers"] == 12

    def test_api_verify_all_endpoint(self, app_client):
        response = app_client.post("/api/v1/sla-slo/verify/all")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "PASSED"
        assert data["overall_score"] == 100.0
        assert data["total_reports"] == 12

    def test_api_get_report_endpoint(self, app_client):
        response = app_client.get("/api/v1/sla-slo/reports/VERIFY-3J.10.1-SLA-DEFINITION")
        assert response.status_code == 200
        data = response.json()
        assert data["verifier_id"] == "VERIFY-3J.10.1-SLA-DEFINITION"

    def test_api_get_scorecard_endpoint(self, app_client):
        response = app_client.get("/api/v1/sla-slo/scorecard")
        assert response.status_code == 200
        data = response.json()
        assert data["overall_score"] == 100.0
        assert "categories" in data

    def test_api_get_manifest_endpoint(self, app_client):
        response = app_client.get("/api/v1/sla-slo/evidence/manifest")
        assert response.status_code == 200
        data = response.json()
        assert data["system"] == "DocuTask Agent"
        assert len(data["files"]) >= 10
