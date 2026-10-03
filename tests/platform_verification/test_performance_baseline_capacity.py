"""
Unit and Integration Tests for Phase 3J.3: Enterprise Performance Baseline & Capacity Verification Framework.
"""

import os
import shutil
import tempfile
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.platform_verification.performance_baseline_capacity.api.performance_baseline_api import (
    router,
    set_runtime,
)
from app.platform_verification.performance_baseline_capacity.domain.models import (
    BaselineCertificationTier,
    VerificationStatus,
)
from app.platform_verification.performance_baseline_capacity.runtime.performance_baseline_runtime import (
    PerformanceBaselineRuntime,
)
from app.platform_verification.performance_baseline_capacity.scoring.performance_baseline_scorer import (
    PerformanceBaselineScorer,
)
from app.platform_verification.performance_baseline_capacity.verifiers import (
    AIPipelinePerformanceVerifier,
    BaselinePerformanceVerifier,
    CapacityModelVerifier,
    ConcurrentLoadVerifier,
    DatabasePerformanceVerifier,
    LatencyDistributionVerifier,
    PerformanceArchitectureVerifier,
    PerformanceFailureVerifier,
    PerformanceRegressionVerifier,
    QueueCapacityVerifier,
    ResourceUtilizationVerifier,
    WorkerScalingVerifier,
    get_all_verifiers,
)


@pytest.fixture
def temp_export_dir():
    temp_dir = tempfile.mkdtemp(prefix="perf_baseline_test_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestIndividualVerifiers:
    """Test all 12 individual verifiers to ensure correct behavior, status, and metrics."""

    def test_performance_architecture_verifier(self):
        verifier = PerformanceArchitectureVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.load_generator.distributed_mode
        assert len(report.telemetry_collectors) == 3
        assert len(report.checks) == 4

    def test_baseline_performance_verifier(self):
        verifier = BaselinePerformanceVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.overall_p95_ms < 50.0
        assert len(report.workflow_metrics) == 6
        assert len(report.checks) == 4

    def test_ai_pipeline_performance_verifier(self):
        verifier = AIPipelinePerformanceVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.ocr_performance.pages_per_minute >= 100.0
        assert report.llm_performance.response_time_ms < 1000.0
        assert report.total_pipeline_ms <= 1500.0
        assert len(report.checks) == 4

    def test_concurrent_load_verifier(self):
        verifier = ConcurrentLoadVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.max_tested_users == 2000
        assert len(report.load_levels) == 3
        assert len(report.checks) == 4

    def test_capacity_model_verifier(self):
        verifier = CapacityModelVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.baseline_throughput_docs_per_hour == 240
        assert report.scaled_throughput_docs_per_hour == 1200
        assert len(report.checks) == 4

    def test_latency_distribution_verifier(self):
        verifier = LatencyDistributionVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.p95_sla_compliant
        assert len(report.percentiles) == 4
        assert len(report.checks) == 4

    def test_resource_utilization_verifier(self):
        verifier = ResourceUtilizationVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert not report.memory.leak_detected
        assert report.cpu.peak_usage_pct < 85.0
        assert len(report.checks) == 4

    def test_database_performance_verifier(self):
        verifier = DatabasePerformanceVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.connection_pool.timeout_count == 0
        assert report.index_analysis.missing_indexes_detected == 0
        assert len(report.checks) == 4

    def test_queue_capacity_verifier(self):
        verifier = QueueCapacityVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.queue_metrics.failed_jobs_count == 0
        assert report.queue_metrics.processing_rate_jobs_min > report.queue_metrics.incoming_rate_jobs_min
        assert len(report.checks) == 4

    def test_worker_scaling_verifier(self):
        verifier = WorkerScalingVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.overall_scaling_efficiency_pct >= 90.0
        assert len(report.scaling_points) == 3
        assert len(report.checks) == 4

    def test_performance_failure_verifier(self):
        verifier = PerformanceFailureVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.backpressure_active
        assert report.circuit_breaking_active
        assert len(report.scenarios) == 3
        assert len(report.checks) == 4

    def test_performance_regression_verifier(self):
        verifier = PerformanceRegressionVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert not report.regression_detected
        assert report.pipeline_gate_passed
        assert len(report.checks) == 3


class TestScoringAndExport:
    """Test 6-category weighted scoring and JSON evidence exporting."""

    def test_scoring_weights_and_tier(self):
        scorer = PerformanceBaselineScorer()
        verifiers = get_all_verifiers()
        reports = {}
        for v in verifiers:
            rep = v.verify()
            reports[v.verifier_id] = rep

        cert = scorer.score_reports(reports)
        assert cert.overall_score >= 95.0
        assert cert.certification_tier == BaselineCertificationTier.ENTERPRISE_PERFORMANCE_READY
        assert cert.passed
        assert len(cert.category_scores) == 6

        total_weight = sum(c.weight for c in cert.category_scores)
        assert pytest.approx(total_weight, 0.001) == 1.0

    def test_exporter_manifests_and_hashes(self, temp_export_dir):
        runtime = PerformanceBaselineRuntime(export_dir=temp_export_dir)
        result = runtime.run_full_verification()

        assert result["passed"]
        assert len(result["exported_files"]) >= 13

        expected_files = [
            "performance_architecture_report.json",
            "baseline_report.json",
            "ai_pipeline_report.json",
            "load_test_report.json",
            "capacity_report.json",
            "latency_distribution_report.json",
            "resource_utilization_report.json",
            "database_report.json",
            "queue_report.json",
            "scaling_report.json",
            "performance_failure_report.json",
            "regression_report.json",
            "certification_report.json",
            "metadata.json",
        ]
        for ef in expected_files:
            file_path = os.path.join(temp_export_dir, ef)
            assert os.path.isfile(file_path), f"Expected file {ef} was not exported."


class TestFastAPIRouter:
    """Test REST API endpoints."""

    def test_api_endpoints(self, temp_export_dir):
        app = FastAPI()
        app.include_router(router)
        runtime = PerformanceBaselineRuntime(export_dir=temp_export_dir)
        set_runtime(runtime)
        client = TestClient(app)

        prefix = "/api/v1/verification/performance-baseline"

        # 1. Health check
        res = client.get(f"{prefix}/health")
        assert res.status_code == 200
        assert res.json()["status"] == "HEALTHY"
        assert res.json()["phase"] == "3J.3"

        # 2. Trigger run
        res = client.post(f"{prefix}/run")
        assert res.status_code == 200
        data = res.json()
        assert data["passed"]
        assert data["score"] >= 95.0
        assert data["tier"] == "Enterprise Performance Ready"

        # 3. Get certification
        res = client.get(f"{prefix}/certification")
        assert res.status_code == 200
        assert res.json()["overall_score"] >= 95.0

        # 4. Get individual reports
        for r_type in ["architecture", "baseline", "ai", "load", "capacity", "latency", "resource", "database", "queue", "scaling", "failure", "regression"]:
            res = client.get(f"{prefix}/reports/{r_type}")
            assert res.status_code == 200
            assert "status" in res.json()
