"""
Unit and Integration Tests for Phase 3J.4: Resource Utilization & Capacity Engineering Verification Framework.
"""

import os
import shutil
import tempfile
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.platform_verification.resource_capacity_engineering.api.resource_capacity_api import (
    router,
    set_runtime,
)
from app.platform_verification.resource_capacity_engineering.collectors import (
    get_all_collectors,
)
from app.platform_verification.resource_capacity_engineering.domain.models import (
    ResourceCertificationTier,
    VerificationStatus,
)
from app.platform_verification.resource_capacity_engineering.runtime.resource_capacity_runtime import (
    ResourceCapacityRuntime,
)
from app.platform_verification.resource_capacity_engineering.scoring.resource_capacity_scorer import (
    ResourceCapacityScorer,
)
from app.platform_verification.resource_capacity_engineering.verifiers import (
    AIResourceProfileVerifier,
    AutoscalingReadinessVerifier,
    CapacityModelingVerifier,
    ContainerResourcePolicyVerifier,
    CPUUtilizationVerifier,
    DatabaseCapacityVerifier,
    MemoryLeakVerifier,
    QueueCapacityVerifier,
    ResourceAlertingVerifier,
    ResourceProfilingVerifier,
    WorkerCapacityVerifier,
    get_all_verifiers,
)


@pytest.fixture
def temp_export_dir():
    temp_dir = tempfile.mkdtemp(prefix="resource_test_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestResourceCollectors:
    """Test all 6 telemetry collectors."""

    def test_collectors(self):
        collectors = get_all_collectors()
        assert len(collectors) == 6
        for c in collectors:
            data = c.collect()
            assert isinstance(data, dict)
            assert "status" in data


class TestIndividualVerifiers:
    """Test all 11 individual verifiers."""

    def test_resource_profiling_verifier(self):
        verifier = ResourceProfilingVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.services) == 5
        assert len(report.checks) == 4

    def test_container_resource_policy_verifier(self):
        verifier = ContainerResourcePolicyVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.unlimited_containers_detected == 0
        assert len(report.checks) == 4

    def test_cpu_utilization_verifier(self):
        verifier = CPUUtilizationVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.saturation_headroom_pct >= 25.0
        assert len(report.checks) == 4

    def test_memory_leak_verifier(self):
        verifier = MemoryLeakVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.growth_slope_mb_per_hour < 0.05
        assert len(report.timeline) == 4
        assert len(report.checks) == 4

    def test_worker_capacity_verifier(self):
        verifier = WorkerCapacityVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.optimal_worker_count == 10
        assert len(report.scaling_curve) == 4
        assert len(report.checks) == 4

    def test_queue_capacity_verifier(self):
        verifier = QueueCapacityVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.drain_time_seconds < 60.0
        assert report.processing_rate_docs_min > report.input_rate_docs_min
        assert len(report.checks) == 4

    def test_database_capacity_verifier(self):
        verifier = DatabaseCapacityVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.deadlocks_count == 0
        assert report.p95_query_time_ms < 20.0
        assert len(report.checks) == 4

    def test_ai_resource_profile_verifier(self):
        verifier = AIResourceProfileVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.primary_bottleneck == "gemini_api"
        assert len(report.stages) == 4
        assert len(report.checks) == 4

    def test_capacity_modeling_verifier(self):
        verifier = CapacityModelingVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.max_documents_per_hour >= 50000
        assert report.recommended_workers == 12
        assert len(report.checks) == 4

    def test_autoscaling_readiness_verifier(self):
        verifier = AutoscalingReadinessVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.scaling_reaction_time_secs <= 30.0
        assert len(report.signals) == 3
        assert len(report.checks) == 4

    def test_resource_alerting_verifier(self):
        verifier = ResourceAlertingVerifier()
        report = verifier.verify()
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert report.alert_pipeline_healthy
        assert len(report.alert_rules) == 4
        assert len(report.checks) == 4


class TestScoringAndExport:
    """Test 6-category weighted scoring and JSON evidence exporting."""

    def test_scoring_weights_and_tier(self):
        scorer = ResourceCapacityScorer()
        verifiers = get_all_verifiers()
        reports = {}
        for v in verifiers:
            rep = v.verify()
            reports[v.verifier_id] = rep

        cert = scorer.score_reports(reports)
        assert cert.overall_score >= 95.0
        assert cert.certification_tier == ResourceCertificationTier.ENTERPRISE_CAPACITY_READY
        assert cert.passed
        assert len(cert.category_scores) == 6

        total_weight = sum(c.weight for c in cert.category_scores)
        assert pytest.approx(total_weight, 0.001) == 1.0

    def test_exporter_manifests_and_hashes(self, temp_export_dir):
        runtime = ResourceCapacityRuntime(export_dir=temp_export_dir)
        result = runtime.run_full_verification()

        assert result["passed"]
        assert len(result["exported_files"]) >= 12

        expected_files = [
            "resource_profile.json",
            "container_resource_policy_report.json",
            "cpu_capacity.json",
            "memory_analysis.json",
            "worker_capacity.json",
            "queue_capacity.json",
            "database_capacity.json",
            "ai_profile.json",
            "capacity_model.json",
            "scaling_report.json",
            "alert_report.json",
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
        runtime = ResourceCapacityRuntime(export_dir=temp_export_dir)
        set_runtime(runtime)
        client = TestClient(app)

        prefix = "/api/v1/verification/resource-capacity"

        # 1. Health check
        res = client.get(f"{prefix}/health")
        assert res.status_code == 200
        assert res.json()["status"] == "HEALTHY"
        assert res.json()["phase"] == "3J.4"

        # 2. Trigger run
        res = client.post(f"{prefix}/run")
        assert res.status_code == 200
        data = res.json()
        assert data["passed"]
        assert data["score"] >= 95.0
        assert data["tier"] == "Enterprise Capacity Ready"

        # 3. Get certification
        res = client.get(f"{prefix}/certification")
        assert res.status_code == 200
        assert res.json()["overall_score"] >= 95.0

        # 4. Get individual reports
        for r_type in ["profile", "policy", "cpu", "memory", "worker", "queue", "database", "ai", "model", "scaling", "alert"]:
            res = client.get(f"{prefix}/reports/{r_type}")
            assert res.status_code == 200
            assert "status" in res.json()
