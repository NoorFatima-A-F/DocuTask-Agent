"""
Phase 3J.11: Comprehensive Test Suite for Intelligent Performance Optimization & Autonomic Capacity Management.
"""

import json
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.platform_verification.enterprise_performance_optimization.domain.models import (
    AIPipelineOptimizationReport,
    AutomatedRemediationReport,
    AutonomousPerformanceTier,
    BaseVerificationReport,
    CapacityPredictionReport,
    CheckResult,
    ContinuousOptimizationLoopReport,
    DatabaseOptimizationReport,
    OptimizationPipelineReport,
    OptimizationRecommendationReport,
    OptimizationSafetyReport,
    PerformanceAnomalyReport,
    PerformanceIntelligenceArchitectureReport,
    RootCauseAnalysisReport,
    VerificationStatus,
    WorkerAutoscalingReport,
)
from app.platform_verification.enterprise_performance_optimization.verifiers import (
    AIPipelineOptimizationVerifier,
    AutomatedRemediationVerifier,
    BottleneckRootCauseVerifier,
    CICDOptimizationPipelineVerifier,
    ContinuousOptimizationLoopVerifier,
    DatabaseOptimizationVerifier,
    IntelligentAutoscalingVerifier,
    OptimizationRecommendationVerifier,
    OptimizationSafetyVerifier,
    PerformanceAnomalyVerifier,
    PerformanceIntelligenceArchitectureVerifier,
    PredictiveCapacityPlanningVerifier,
)
from app.platform_verification.enterprise_performance_optimization.scoring.optimization_scorer import (
    OptimizationScorer,
)
from app.platform_verification.enterprise_performance_optimization.exporter.optimization_exporter import (
    OptimizationExporter,
)
from app.platform_verification.enterprise_performance_optimization.runtime.optimization_runtime import (
    OptimizationRuntime,
)
from app.platform_verification.enterprise_performance_optimization.api.optimization_api import (
    router,
)


class TestEnterprisePerformanceOptimization:
    """Complete test suite for Phase 3J.11."""

    @pytest.fixture
    def app_client(self):
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)

    @pytest.fixture
    def temp_export_dir(self, tmp_path):
        export_path = tmp_path / "test_perf_opt"
        export_path.mkdir(parents=True, exist_ok=True)
        return str(export_path)

    # ──────────────────────────────────────────────────────────────────────────
    # 1. Verifiers Individual Tests (3J.11.1 - 3J.11.12)
    # ──────────────────────────────────────────────────────────────────────────

    def test_3j_11_1_intelligence_architecture_verifier(self):
        verifier = PerformanceIntelligenceArchitectureVerifier()
        assert verifier.verifier_id == "VERIFY-3J.11.1-INTELLIGENCE-ARCH"
        assert verifier.phase_id == "3J.11.1"
        report = verifier.verify()
        assert isinstance(report, PerformanceIntelligenceArchitectureReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert all(c.passed for c in report.checks)
        assert report.total_layers_active == 6

    def test_3j_11_2_bottleneck_root_cause_verifier(self):
        verifier = BottleneckRootCauseVerifier()
        assert verifier.verifier_id == "VERIFY-3J.11.2-ROOT-CAUSE-ANALYSIS"
        assert verifier.phase_id == "3J.11.2"
        report = verifier.verify()
        assert isinstance(report, RootCauseAnalysisReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.primary_root_cause == "worker_pool"
        assert report.confidence_score_pct >= 90.0

    def test_3j_11_3_optimization_recommendation_verifier(self):
        verifier = OptimizationRecommendationVerifier()
        assert verifier.verifier_id == "VERIFY-3J.11.3-OPTIMIZATION-RECOMMENDATION"
        assert verifier.phase_id == "3J.11.3"
        report = verifier.verify()
        assert isinstance(report, OptimizationRecommendationReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.total_recommendations == 4
        assert report.compute_opt_ready is True
        assert report.database_opt_ready is True

    def test_3j_11_4_intelligent_autoscaling_verifier(self):
        verifier = IntelligentAutoscalingVerifier()
        assert verifier.verifier_id == "VERIFY-3J.11.4-INTELLIGENT-AUTOSCALING"
        assert verifier.phase_id == "3J.11.4"
        report = verifier.verify()
        assert isinstance(report, WorkerAutoscalingReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.scaling_time_seconds < 30.0
        assert report.max_workers == 30

    def test_3j_11_5_database_optimization_verifier(self):
        verifier = DatabaseOptimizationVerifier()
        assert verifier.verifier_id == "VERIFY-3J.11.5-DATABASE-OPTIMIZATION"
        assert verifier.phase_id == "3J.11.5"
        report = verifier.verify()
        assert isinstance(report, DatabaseOptimizationReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.slow_queries_identified == 2
        assert "20x" in report.query_speedup_factor

    def test_3j_11_6_ai_pipeline_optimization_verifier(self):
        verifier = AIPipelineOptimizationVerifier()
        assert verifier.verifier_id == "VERIFY-3J.11.6-AI-PIPELINE-OPTIMIZATION"
        assert verifier.phase_id == "3J.11.6"
        report = verifier.verify()
        assert isinstance(report, AIPipelineOptimizationReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.token_reduction_pct >= 25.0
        assert report.cost_reduction_pct >= 30.0

    def test_3j_11_7_predictive_capacity_planning_verifier(self):
        verifier = PredictiveCapacityPlanningVerifier()
        assert verifier.verifier_id == "VERIFY-3J.11.7-PREDICTIVE-CAPACITY"
        assert verifier.phase_id == "3J.11.7"
        report = verifier.verify()
        assert isinstance(report, CapacityPredictionReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.target_docs_per_month == 500000
        assert len(report.forecasts) == 3

    def test_3j_11_8_performance_anomaly_verifier(self):
        verifier = PerformanceAnomalyVerifier()
        assert verifier.verifier_id == "VERIFY-3J.11.8-PERFORMANCE-ANOMALY"
        assert verifier.phase_id == "3J.11.8"
        report = verifier.verify()
        assert isinstance(report, PerformanceAnomalyReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.false_positive_rate_pct < 3.0
        assert report.total_anomalies_detected == 4

    def test_3j_11_9_automated_remediation_verifier(self):
        verifier = AutomatedRemediationVerifier()
        assert verifier.verifier_id == "VERIFY-3J.11.9-AUTOMATED-REMEDIATION"
        assert verifier.phase_id == "3J.11.9"
        report = verifier.verify()
        assert isinstance(report, AutomatedRemediationReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.remediation_success_rate_pct == 100.0
        assert len(report.remediations) == 4

    def test_3j_11_10_optimization_safety_verifier(self):
        verifier = OptimizationSafetyVerifier()
        assert verifier.verifier_id == "VERIFY-3J.11.10-OPTIMIZATION-SAFETY"
        assert verifier.phase_id == "3J.11.10"
        report = verifier.verify()
        assert isinstance(report, OptimizationSafetyReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.max_worker_limit == 100
        assert report.max_db_connection_limit == 500

    def test_3j_11_11_continuous_optimization_loop_verifier(self):
        verifier = ContinuousOptimizationLoopVerifier()
        assert verifier.verifier_id == "VERIFY-3J.11.11-CONTINUOUS-LOOP"
        assert verifier.phase_id == "3J.11.11"
        report = verifier.verify()
        assert isinstance(report, ContinuousOptimizationLoopReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.throughput_improvement_factor >= 2.0
        assert report.latency_reduction_pct >= 50.0

    def test_3j_11_12_cicd_optimization_pipeline_verifier(self):
        verifier = CICDOptimizationPipelineVerifier()
        assert verifier.verifier_id == "VERIFY-3J.11.12-CICD-OPTIMIZATION-PIPELINE"
        assert verifier.phase_id == "3J.11.12"
        report = verifier.verify()
        assert isinstance(report, OptimizationPipelineReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.pipeline_gating_active is True
        assert report.deployment_decision == "PROCEED_TO_PRODUCTION"

    # ──────────────────────────────────────────────────────────────────────────
    # 2. Scoring & Certification Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_optimization_scorer_full_pass(self):
        scorer = OptimizationScorer()
        runtime = OptimizationRuntime()
        reports = [v.verify() for v in runtime.verifiers]
        scorecard = scorer.score(reports)
        assert scorecard.overall_score == 100.0
        assert (
            scorecard.certification_tier
            == AutonomousPerformanceTier.AUTONOMOUS_PERFORMANCE_READY
        )
        assert scorecard.status == VerificationStatus.PASSED
        assert len(scorecard.categories) == 6

    def test_optimization_scorer_degradation(self):
        scorer = OptimizationScorer()
        report = BaseVerificationReport(
            verifier_id="VERIFY-3J.11.2-ROOT-CAUSE-ANALYSIS",
            phase_id="3J.11.2",
            phase_name="Root Cause Test",
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

    def test_optimization_exporter(self, temp_export_dir):
        exporter = OptimizationExporter(export_dir=temp_export_dir)
        verifier = PerformanceIntelligenceArchitectureVerifier()
        report = verifier.verify()
        paths = exporter.export_report(report)
        assert len(paths) >= 1
        for p in paths:
            assert p.exists()
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert data["phase_id"] == "3J.11.1"

        scorer = OptimizationScorer()
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

    def test_optimization_runtime_execution(self, temp_export_dir):
        runtime = OptimizationRuntime(export_dir=temp_export_dir)
        result = runtime.run_all()
        assert result["status"] == "PASSED"
        assert result["overall_score"] == 100.0
        assert len(result["reports"]) == 12
        assert result["manifest"] is not None

        single = runtime.run_verifier("VERIFY-3J.11.1-INTELLIGENCE-ARCH")
        assert single is not None
        assert single.phase_id == "3J.11.1"

    # ──────────────────────────────────────────────────────────────────────────
    # 5. REST API Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_api_health_endpoint(self, app_client):
        response = app_client.get("/api/v1/performance-optimization/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["phase"] == "3J.11"

    def test_api_status_endpoint(self, app_client):
        response = app_client.get("/api/v1/performance-optimization/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert data["total_verifiers"] == 12

    def test_api_verify_all_endpoint(self, app_client):
        response = app_client.post("/api/v1/performance-optimization/verify/all")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "PASSED"
        assert data["overall_score"] == 100.0
        assert data["total_reports"] == 12

    def test_api_get_report_endpoint(self, app_client):
        response = app_client.get("/api/v1/performance-optimization/reports/VERIFY-3J.11.1-INTELLIGENCE-ARCH")
        assert response.status_code == 200
        data = response.json()
        assert data["verifier_id"] == "VERIFY-3J.11.1-INTELLIGENCE-ARCH"

    def test_api_get_scorecard_endpoint(self, app_client):
        response = app_client.get("/api/v1/performance-optimization/scorecard")
        assert response.status_code == 200
        data = response.json()
        assert data["overall_score"] == 100.0
        assert "categories" in data

    def test_api_get_manifest_endpoint(self, app_client):
        response = app_client.get("/api/v1/performance-optimization/evidence/manifest")
        assert response.status_code == 200
        data = response.json()
        assert data["system"] == "DocuTask Agent"
        assert len(data["files"]) >= 10
