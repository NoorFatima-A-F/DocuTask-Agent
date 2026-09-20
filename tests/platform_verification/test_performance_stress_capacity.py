"""
Unit and Integration Tests for Phase 3J.2: Performance Stress Verification & Capacity Boundary Analysis Framework.
"""

import os
import shutil
import tempfile
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.platform_verification.performance_stress_capacity.api.performance_stress_api import (
    router,
    set_runtime,
)
from app.platform_verification.performance_stress_capacity.domain.models import (
    CertificationTier,
    VerificationStatus,
)
from app.platform_verification.performance_stress_capacity.exporter.performance_stress_exporter import (
    PerformanceStressExporter,
)
from app.platform_verification.performance_stress_capacity.runtime.performance_stress_runtime import (
    PerformanceStressRuntime,
)
from app.platform_verification.performance_stress_capacity.scoring.performance_stress_scorer import (
    PerformanceStressScorer,
)
from app.platform_verification.performance_stress_capacity.verifiers import (
    AIProviderStressVerifier,
    BaselineStressVerifier,
    CapacityBoundaryVerifier,
    DatabaseStressVerifier,
    MemoryStabilityVerifier,
    OverloadStressVerifier,
    PerformanceEnvironmentVerifier,
    PerformanceRecoveryVerifier,
    PerformanceRegressionGateVerifier,
    ProgressiveLoadVerifier,
    WorkerScalingVerifier,
    get_all_verifiers,
)


@pytest.fixture
def temp_export_dir():
    temp_dir = tempfile.mkdtemp(prefix="perf_test_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestIndividualVerifiers:
    """Test individual verifiers to ensure correct behavior, status, and metrics."""

    def test_performance_environment_verifier(self):
        verifier = PerformanceEnvironmentVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.isolated_services_count == 8
        assert not report.shared_db_detected
        assert len(report.checks) == 4

    def test_baseline_stress_verifier(self):
        verifier = BaselineStressVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.api_upload_p95_ms < 50.0
        assert report.agent_lifecycle_total_ms == 1250.0
        assert len(report.checks) == 4

    def test_progressive_load_verifier(self):
        verifier = ProgressiveLoadVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.max_concurrent_users_tested == 1000
        assert report.peak_throughput_rps > 200.0
        assert len(report.checks) == 4

    def test_overload_stress_verifier(self):
        verifier = OverloadStressVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.burst_document_count == 50000
        assert report.data_loss_count == 0
        assert len(report.checks) == 4

    def test_capacity_boundary_verifier(self):
        verifier = CapacityBoundaryVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.max_safe_docs_per_hour == 5000
        assert report.critical_limit_docs_per_hour == 8500
        assert len(report.checks) == 4

    def test_worker_scaling_verifier(self):
        verifier = WorkerScalingVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.max_workers_tested == 20
        assert report.scaling_linearity_pct == 92.5
        assert len(report.checks) == 4

    def test_database_stress_verifier(self):
        verifier = DatabaseStressVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.max_connections_tested == 1000
        assert report.p95_query_latency_ms < 25.0
        assert report.deadlocks_detected == 0
        assert len(report.checks) == 4

    def test_ai_provider_stress_verifier(self):
        verifier = AIProviderStressVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.burst_requests == 1000
        assert report.rate_limit_recovery_rate == 100.0
        assert len(report.checks) == 4

    def test_memory_stability_verifier(self):
        verifier = MemoryStabilityVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.soak_duration_hours == 72
        assert report.rss_growth_rate_mb_per_hour < 0.05
        assert len(report.checks) == 4

    def test_performance_recovery_verifier(self):
        verifier = PerformanceRecoveryVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.backlog_drain_time_sec <= 60.0
        assert report.mttr_seconds <= 60.0
        assert len(report.checks) == 4

    def test_performance_regression_gate_verifier(self):
        verifier = PerformanceRegressionGateVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.regressions_detected == 0
        assert report.gate_passed
        assert len(report.checks) == 3


class TestScoringAndExport:
    """Test the multi-dimensional 6-category scoring and file exporting."""

    def test_scoring_weights_and_tier(self):
        scorer = PerformanceStressScorer()
        verifiers = get_all_verifiers()
        reports = {}
        for v in verifiers:
            rep = v.verify()
            reports[v.verifier_id] = rep

        cert = scorer.score_reports(reports)
        assert cert.overall_score >= 95.0
        assert cert.certification_tier == CertificationTier.ENTERPRISE_PERFORMANCE_CERTIFIED
        assert cert.passed
        assert len(cert.category_scores) == 6

        total_weight = sum(c.weight for c in cert.category_scores)
        assert pytest.approx(total_weight, 0.001) == 1.0

    def test_exporter_manifests_and_hashes(self, temp_export_dir):
        runtime = PerformanceStressRuntime(export_dir=temp_export_dir)
        result = runtime.run_full_verification()

        assert result["passed"]
        assert len(result["exported_files"]) >= 12

        # Verify all files exist in temp_export_dir
        expected_files = [
            "performance_environment_report.json",
            "baseline_report.json",
            "load_test_report.json",
            "stress_test_report.json",
            "capacity_boundary_report.json",
            "worker_scaling_report.json",
            "database_performance_report.json",
            "ai_provider_stress_report.json",
            "memory_stability_report.json",
            "recovery_report.json",
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
        runtime = PerformanceStressRuntime(export_dir=temp_export_dir)
        set_runtime(runtime)
        client = TestClient(app)

        prefix = "/api/v1/verification/performance-stress"

        # 1. Health check
        res = client.get(f"{prefix}/health")
        assert res.status_code == 200
        assert res.json()["status"] == "HEALTHY"

        # 2. Trigger run
        res = client.post(f"{prefix}/run")
        assert res.status_code == 200
        data = res.json()
        assert data["passed"]
        assert data["score"] >= 95.0
        assert data["tier"] == "Enterprise Performance Certified"

        # 3. Get certification
        res = client.get(f"{prefix}/certification")
        assert res.status_code == 200
        assert res.json()["overall_score"] >= 95.0

        # 4. Get individual reports
        for r_type in ["baseline", "load", "stress", "boundary", "scaling", "database", "ai", "memory", "recovery", "regression"]:
            res = client.get(f"{prefix}/reports/{r_type}")
            assert res.status_code == 200
            assert "status" in res.json()
