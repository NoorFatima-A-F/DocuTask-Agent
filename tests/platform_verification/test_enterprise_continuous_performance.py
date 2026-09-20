"""
Phase 3J.12: Comprehensive Test Suite for Continuous Performance Engineering & Regression Intelligence.
"""

import json
import os
from pathlib import Path
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.platform_verification.continuous_performance_engineering.domain.models import (
    BaseVerificationReport,
    BenchmarkExecutionReport,
    ChangeImpactAnalysisReport,
    CheckResult,
    CICDPerformancePipelineReport,
    ContinuousPerformanceArchitectureReport,
    ContinuousPerformanceEngineeringTier,
    ContinuousPerformanceScorecard,
    MultiEnvironmentComparisonReport,
    PerformanceBaselineReport,
    PerformanceDashboardReport,
    PerformanceExperimentReport,
    PerformanceGateReport,
    PerformanceKnowledgeReport,
    PerformanceRegressionReport,
    PerformanceTrendReport,
    VerificationStatus,
)
from app.platform_verification.continuous_performance_engineering.domain.interfaces import (
    IContinuousPerformanceVerifier,
)
from app.platform_verification.continuous_performance_engineering.verifiers import (
    BenchmarkExecutionVerifier,
    ChangeImpactAnalysisVerifier,
    CICDPerformanceIntegrationVerifier,
    ContinuousPerformanceArchitectureVerifier,
    ContinuousPerformanceDashboardVerifier,
    MultiEnvironmentComparisonVerifier,
    PerformanceBaselineVerifier,
    PerformanceExperimentTrackingVerifier,
    PerformanceKnowledgeRepositoryVerifier,
    PerformanceQualityGatesVerifier,
    PerformanceRegressionEngineVerifier,
    PerformanceTrendAnalysisVerifier,
)
from app.platform_verification.continuous_performance_engineering.scoring.continuous_performance_scorer import (
    ContinuousPerformanceScorer,
)
from app.platform_verification.continuous_performance_engineering.exporter.continuous_performance_exporter import (
    ContinuousPerformanceExporter,
)
from app.platform_verification.continuous_performance_engineering.runtime.continuous_performance_runtime import (
    ContinuousPerformanceRuntime,
)
from app.platform_verification.continuous_performance_engineering.api.continuous_performance_api import (
    router,
)


class TestEnterpriseContinuousPerformance:
    """Complete test suite for Phase 3J.12."""

    @pytest.fixture
    def app_client(self):
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)

    @pytest.fixture
    def temp_export_dir(self, tmp_path):
        export_path = tmp_path / "test_cont_perf"
        export_path.mkdir(parents=True, exist_ok=True)
        return str(export_path)

    # ──────────────────────────────────────────────────────────────────────────
    # 1. Verifiers Individual Tests (3J.12.1 - 3J.12.12)
    # ──────────────────────────────────────────────────────────────────────────

    def test_3j_12_1_architecture_verifier(self):
        verifier = ContinuousPerformanceArchitectureVerifier()
        assert verifier.verifier_id == "VERIFY-3J.12.1-CONT-PERF-ARCH"
        assert verifier.phase_id == "3J.12.1"
        report = verifier.verify()
        assert isinstance(report, ContinuousPerformanceArchitectureReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert all(c.passed for c in report.checks)
        assert report.components_count == 8
        assert report.pipeline_enabled is True

    def test_3j_12_2_baseline_management_verifier(self):
        verifier = PerformanceBaselineVerifier()
        assert verifier.verifier_id == "VERIFY-3J.12.2-BASELINE-MANAGEMENT"
        assert verifier.phase_id == "3J.12.2"
        report = verifier.verify()
        assert isinstance(report, PerformanceBaselineReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.baseline_version == "v1.0.0"
        assert len(report.profiles) == 4

    def test_3j_12_3_benchmark_execution_verifier(self):
        verifier = BenchmarkExecutionVerifier()
        assert verifier.verifier_id == "VERIFY-3J.12.3-BENCHMARK-EXECUTION"
        assert verifier.phase_id == "3J.12.3"
        report = verifier.verify()
        assert isinstance(report, BenchmarkExecutionReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.scenarios_executed == 4
        assert report.all_scenarios_passed is True

    def test_3j_12_4_regression_engine_verifier(self):
        verifier = PerformanceRegressionEngineVerifier()
        assert verifier.verifier_id == "VERIFY-3J.12.4-REGRESSION-ENGINE"
        assert verifier.phase_id == "3J.12.4"
        report = verifier.verify()
        assert isinstance(report, PerformanceRegressionReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.regressions_detected == 0
        assert report.latency_delta_pct == -28.0

    def test_3j_12_5_change_impact_verifier(self):
        verifier = ChangeImpactAnalysisVerifier()
        assert verifier.verifier_id == "VERIFY-3J.12.5-CHANGE-IMPACT"
        assert verifier.phase_id == "3J.12.5"
        report = verifier.verify()
        assert isinstance(report, ChangeImpactAnalysisReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.changes_evaluated == 3
        assert report.all_changes_safe is True

    def test_3j_12_6_quality_gates_verifier(self):
        verifier = PerformanceQualityGatesVerifier()
        assert verifier.verifier_id == "VERIFY-3J.12.6-QUALITY-GATES"
        assert verifier.phase_id == "3J.12.6"
        report = verifier.verify()
        assert isinstance(report, PerformanceGateReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.deployment_allowed is True
        assert report.gate_outcome == "PASS"

    def test_3j_12_7_multi_environment_verifier(self):
        verifier = MultiEnvironmentComparisonVerifier()
        assert verifier.verifier_id == "VERIFY-3J.12.7-MULTI-ENV-COMPARISON"
        assert verifier.phase_id == "3J.12.7"
        report = verifier.verify()
        assert isinstance(report, MultiEnvironmentComparisonReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.environments_compared == 3
        assert report.cross_environment_parity_verified is True

    def test_3j_12_8_knowledge_repository_verifier(self):
        verifier = PerformanceKnowledgeRepositoryVerifier()
        assert verifier.verifier_id == "VERIFY-3J.12.8-KNOWLEDGE-REPOSITORY"
        assert verifier.phase_id == "3J.12.8"
        report = verifier.verify()
        assert isinstance(report, PerformanceKnowledgeReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.total_knowledge_entries == 4
        assert report.pattern_retrieval_latency_ms < 15.0

    def test_3j_12_9_trend_analysis_verifier(self):
        verifier = PerformanceTrendAnalysisVerifier()
        assert verifier.verifier_id == "VERIFY-3J.12.9-TREND-ANALYSIS"
        assert verifier.phase_id == "3J.12.9"
        report = verifier.verify()
        assert isinstance(report, PerformanceTrendReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.horizons_analyzed == 3
        assert report.slow_degradation_detected is False

    def test_3j_12_10_dashboard_validation_verifier(self):
        verifier = ContinuousPerformanceDashboardVerifier()
        assert verifier.verifier_id == "VERIFY-3J.12.10-DASHBOARD-VALIDATION"
        assert verifier.phase_id == "3J.12.10"
        report = verifier.verify()
        assert isinstance(report, PerformanceDashboardReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.total_dashboards_verified == 4
        assert report.release_performance_view_ready is True

    def test_3j_12_11_cicd_integration_verifier(self):
        verifier = CICDPerformanceIntegrationVerifier()
        assert verifier.verifier_id == "VERIFY-3J.12.11-CICD-INTEGRATION"
        assert verifier.phase_id == "3J.12.11"
        report = verifier.verify()
        assert isinstance(report, CICDPerformancePipelineReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert len(report.supported_platforms) == 3
        assert report.automated_gating_verified is True

    def test_3j_12_12_experiment_tracking_verifier(self):
        verifier = PerformanceExperimentTrackingVerifier()
        assert verifier.verifier_id == "VERIFY-3J.12.12-EXPERIMENT-TRACKING"
        assert verifier.phase_id == "3J.12.12"
        report = verifier.verify()
        assert isinstance(report, PerformanceExperimentReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.experiments_tracked == 3
        assert report.hypothesis_testing_framework_active is True

    # ──────────────────────────────────────────────────────────────────────────
    # 2. Scoring & Certification Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_continuous_performance_scorer_full_pass(self):
        scorer = ContinuousPerformanceScorer()
        runtime = ContinuousPerformanceRuntime()
        reports = [v.verify() for v in runtime.verifiers]
        scorecard = scorer.score(reports)
        assert scorecard.overall_score == 100.0
        assert (
            scorecard.certification_tier
            == ContinuousPerformanceEngineeringTier.CONTINUOUS_PERFORMANCE_ENGINEERING_READY
        )
        assert scorecard.status == VerificationStatus.PASSED
        assert len(scorecard.categories) == 6

    def test_continuous_performance_scorer_degradation(self):
        scorer = ContinuousPerformanceScorer()
        report = BaseVerificationReport(
            verifier_id="VERIFY-3J.12.4-REGRESSION-ENGINE",
            phase_id="3J.12.4",
            phase_name="Regression Test",
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

    def test_continuous_performance_exporter(self, temp_export_dir):
        exporter = ContinuousPerformanceExporter(export_dir=temp_export_dir)
        verifier = ContinuousPerformanceArchitectureVerifier()
        report = verifier.verify()
        paths = exporter.export_report(report)
        assert len(paths) >= 1
        for p in paths:
            assert p.exists()
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert data["phase_id"] == "3J.12.1"

        scorer = ContinuousPerformanceScorer()
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

    def test_continuous_performance_runtime_execution(self, temp_export_dir):
        runtime = ContinuousPerformanceRuntime(export_dir=temp_export_dir)
        result = runtime.run_all()
        assert result["status"] == "PASSED"
        assert result["overall_score"] == 100.0
        assert len(result["reports"]) == 12
        assert result["manifest"] is not None

        single = runtime.run_verifier("VERIFY-3J.12.1-CONT-PERF-ARCH")
        assert single is not None
        assert single.phase_id == "3J.12.1"

    # ──────────────────────────────────────────────────────────────────────────
    # 5. REST API Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_api_health_endpoint(self, app_client):
        response = app_client.get("/api/v1/continuous-performance/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["phase"] == "3J.12"

    def test_api_status_endpoint(self, app_client):
        response = app_client.get("/api/v1/continuous-performance/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert data["total_verifiers"] == 12

    def test_api_verify_all_endpoint(self, app_client):
        response = app_client.post("/api/v1/continuous-performance/verify/all")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "PASSED"
        assert data["overall_score"] == 100.0
        assert data["total_reports"] == 12

    def test_api_get_report_endpoint(self, app_client):
        response = app_client.get("/api/v1/continuous-performance/reports/VERIFY-3J.12.1-CONT-PERF-ARCH")
        assert response.status_code == 200
        data = response.json()
        assert data["verifier_id"] == "VERIFY-3J.12.1-CONT-PERF-ARCH"

    def test_api_get_scorecard_endpoint(self, app_client):
        response = app_client.get("/api/v1/continuous-performance/scorecard")
        assert response.status_code == 200
        data = response.json()
        assert data["overall_score"] == 100.0
        assert "categories" in data

    def test_api_get_manifest_endpoint(self, app_client):
        response = app_client.get("/api/v1/continuous-performance/evidence/manifest")
        assert response.status_code == 200
        data = response.json()
        assert data["system"] == "DocuTask Agent"
        assert len(data["files"]) >= 10
