"""Comprehensive Test Suite for Phase 3J.6 Enterprise Performance Infrastructure Verification Framework."""

import json
import os
import shutil
import tempfile
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.platform_verification.enterprise_performance_infrastructure.api.performance_infrastructure_api import (
    router,
)
from app.platform_verification.enterprise_performance_infrastructure.domain.models import (
    APILatencyReport,
    BaseVerificationReport,
    CapacityBoundaryReport,
    CategoryScore,
    DatabasePerformanceReport,
    DegradationAnalysisReport,
    E2EWorkflowReport,
    EnterprisePerformanceCertificationReport,
    EnterprisePerformanceTier,
    MemoryStabilityReport,
    MonitoringIntegrationReport,
    PerformanceCertificationReport,
    PerformanceTestArchitectureReport,
    PerformanceVerificationManifest,
    PerformanceVerificationStatus,
    QueueCapacityReport,
    ResourceUtilizationReport,
    ThroughputScalingReport,
    VerificationStatus,
    WorkerEfficiencyReport,
    WorkloadModelReport,
)
from app.platform_verification.enterprise_performance_infrastructure.exporter.performance_infrastructure_exporter import (
    PerformanceInfrastructureExporter,
)
from app.platform_verification.enterprise_performance_infrastructure.runtime.performance_infrastructure_runtime import (
    PerformanceInfrastructureRuntime,
)
from app.platform_verification.enterprise_performance_infrastructure.scoring.performance_infrastructure_scorer import (
    PerformanceInfrastructureScorer,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers import (
    get_all_verifiers,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.test_architecture_verifier import (
    PerformanceTestArchitectureVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.workload_modeling_verifier import (
    WorkloadModelingVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.api_performance_verifier import (
    APIPerformanceVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.e2e_workflow_verifier import (
    E2EWorkflowVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.throughput_scaling_verifier import (
    ThroughputScalingVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.database_performance_verifier import (
    DatabasePerformanceVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.queue_capacity_verifier import (
    QueueCapacityVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.worker_efficiency_verifier import (
    WorkerEfficiencyVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.resource_utilization_verifier import (
    ResourceUtilizationVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.memory_stability_verifier import (
    MemoryStabilityVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.degradation_analysis_verifier import (
    DegradationAnalysisVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.capacity_boundary_verifier import (
    CapacityBoundaryVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.monitoring_integration_verifier import (
    MonitoringIntegrationVerifier,
)


# ─── 1. Domain Models Tests ───────────────────────────────────────────────────

def test_domain_models_instantiation():
    base = BaseVerificationReport(
        verifier_id="VERIFY-TEST",
        phase_id="3J.6.TEST",
        phase_name="Test Phase",
        status=VerificationStatus.PASSED,
        score=100.0,
    )
    assert base.phase_id == "3J.6.TEST"
    assert base.status == VerificationStatus.PASSED

    cert = EnterprisePerformanceCertificationReport(
        verifier_id="VERIFY-3J.6.14-CERT",
        phase_id="3J.6.14",
        phase_name="Certification",
        overall_score=100.0,
        certification_tier=EnterprisePerformanceTier.ENTERPRISE_PERFORMANCE_READY,
    )
    assert cert.certification_tier == EnterprisePerformanceTier.ENTERPRISE_PERFORMANCE_READY
    assert cert.overall_score == 100.0

    # Test aliases
    assert PerformanceVerificationStatus is VerificationStatus
    assert PerformanceCertificationReport is EnterprisePerformanceCertificationReport


# ─── 2. All 13 Verifiers Individual Tests ─────────────────────────────────────

def test_all_verifiers_registered():
    verifiers = get_all_verifiers()
    assert len(verifiers) == 13
    phase_ids = [v.phase_id for v in verifiers]
    expected_ids = [
        "3J.6.1", "3J.6.2", "3J.6.3", "3J.6.4", "3J.6.5", "3J.6.6", "3J.6.7",
        "3J.6.8", "3J.6.9", "3J.6.10", "3J.6.11", "3J.6.12", "3J.6.13",
    ]
    assert phase_ids == expected_ids


def test_3j_6_1_test_architecture_verifier():
    v = PerformanceTestArchitectureVerifier()
    rep = v.verify()
    assert isinstance(rep, PerformanceTestArchitectureReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.score >= 95.0
    assert rep.components_tested == 8
    assert rep.workload_models == 5
    assert rep.architecture_status == "READY"
    assert len(rep.components) == 8


def test_3j_6_2_workload_modeling_verifier():
    v = WorkloadModelingVerifier()
    rep = v.verify()
    assert isinstance(rep, WorkloadModelReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.score >= 95.0
    assert len(rep.profiles) == 5
    assert rep.all_profiles_passed is True
    # Verify profile names
    profile_names = [p.profile_name for p in rep.profiles]
    assert "Normal Business Hours" in profile_names
    assert "Peak Business Load" in profile_names


def test_3j_6_3_api_performance_verifier():
    v = APIPerformanceVerifier()
    rep = v.verify()
    assert isinstance(rep, APILatencyReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.score >= 95.0
    assert len(rep.endpoints) == 6
    assert rep.p95_upload_latency_ms == 42.0
    assert rep.all_endpoints_sla_compliant is True


def test_3j_6_4_e2e_workflow_verifier():
    v = E2EWorkflowVerifier()
    rep = v.verify()
    assert isinstance(rep, E2EWorkflowReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.score >= 95.0
    assert len(rep.stages) == 7
    assert rep.ai_inference_pct == 46.9
    assert rep.ocr_processing_pct == 33.2
    assert rep.total_processing_time_ms < 5000.0


def test_3j_6_5_throughput_scaling_verifier():
    v = ThroughputScalingVerifier()
    rep = v.verify()
    assert isinstance(rep, ThroughputScalingReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.score >= 95.0
    assert len(rep.scaling_curve) == 5
    assert rep.max_sustained_dph == 1200
    assert rep.linear_scaling_verified is True


def test_3j_6_6_database_performance_verifier():
    v = DatabasePerformanceVerifier()
    rep = v.verify()
    assert isinstance(rep, DatabasePerformanceReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.score >= 95.0
    assert rep.p95_query_latency_ms == 15.2
    assert rep.lock_contention_events == 0
    assert rep.slow_queries_count == 0
    assert rep.missing_indexes_count == 0


def test_3j_6_7_queue_capacity_verifier():
    v = QueueCapacityVerifier()
    rep = v.verify()
    assert isinstance(rep, QueueCapacityReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.score >= 95.0
    assert rep.processing_rate_jobs_min > rep.enqueue_rate_jobs_min
    assert rep.queue_saturation_detected is False
    assert rep.retry_rate_pct == 0.0


def test_3j_6_8_worker_efficiency_verifier():
    v = WorkerEfficiencyVerifier()
    rep = v.verify()
    assert isinstance(rep, WorkerEfficiencyReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.score >= 95.0
    assert len(rep.efficiency_tiers) == 4
    assert rep.optimal_worker_count == 10
    assert rep.bottleneck_detected == "None (Well balanced)"


def test_3j_6_9_resource_utilization_verifier():
    v = ResourceUtilizationVerifier()
    rep = v.verify()
    assert isinstance(rep, ResourceUtilizationReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.score >= 95.0
    assert rep.cpu_usage_avg_pct < 60.0
    assert rep.cpu_throttling_events == 0
    assert rep.network_packet_loss_pct == 0.0


def test_3j_6_10_memory_stability_verifier():
    v = MemoryStabilityVerifier()
    rep = v.verify()
    assert isinstance(rep, MemoryStabilityReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.score >= 95.0
    assert rep.duration_hours == 72
    assert len(rep.checkpoints) == 5
    assert rep.leak_detected is False
    assert rep.memory_growth_slope_mb_hr < 0.1


def test_3j_6_11_degradation_analysis_verifier():
    v = DegradationAnalysisVerifier()
    rep = v.verify()
    assert isinstance(rep, DegradationAnalysisReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.score >= 95.0
    assert len(rep.stages) == 5
    assert rep.controlled_degradation_verified is True
    assert rep.sudden_crash_detected is False


def test_3j_6_12_capacity_boundary_verifier():
    v = CapacityBoundaryVerifier()
    rep = v.verify()
    assert isinstance(rep, CapacityBoundaryReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.score >= 95.0
    assert rep.max_sustainable_dph >= 1000
    assert rep.max_concurrent_users >= 500
    assert rep.operating_envelope_defined is True


def test_3j_6_13_monitoring_integration_verifier():
    v = MonitoringIntegrationVerifier()
    rep = v.verify()
    assert isinstance(rep, MonitoringIntegrationReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.score >= 95.0
    assert rep.prometheus_integrated is True
    assert rep.grafana_integrated is True
    assert rep.opentelemetry_integrated is True
    assert len(rep.dashboards) == 4


# ─── 3. Scorer Tests ─────────────────────────────────────────────────────────

def test_scorer_calculation():
    verifiers = get_all_verifiers()
    reports = {}
    for v in verifiers:
        reports[v.verifier_id] = v.verify()

    scorer = PerformanceInfrastructureScorer()
    cert = scorer.score_reports(reports)

    assert cert.phase_id == "3J.6.14"
    assert len(cert.category_scores) == 5
    total_weights = sum(c.weight for c in cert.category_scores)
    assert abs(total_weights - 1.0) < 1e-6
    assert cert.overall_score >= 95.0
    assert cert.certification_tier == EnterprisePerformanceTier.ENTERPRISE_PERFORMANCE_READY
    assert cert.passed is True


# ─── 4. Exporter Tests ───────────────────────────────────────────────────────

def test_exporter_manifest_and_files():
    temp_dir = tempfile.mkdtemp()
    try:
        verifiers = get_all_verifiers()
        reports = {}
        for v in verifiers:
            reports[v.verifier_id] = v.verify()

        scorer = PerformanceInfrastructureScorer()
        cert = scorer.score_reports(reports)

        exporter = PerformanceInfrastructureExporter()
        manifest = exporter.export_all(reports, cert, output_dir=temp_dir)

        assert isinstance(manifest, PerformanceVerificationManifest)
        assert manifest.passed is True
        assert os.path.exists(os.path.join(temp_dir, "metadata.json"))
        assert os.path.exists(os.path.join(temp_dir, "certification_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "architecture_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "workload_model_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "api_latency_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "e2e_workflow_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "throughput_scaling_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "database_performance_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "queue_capacity_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "worker_efficiency_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "resource_utilization_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "memory_stability_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "degradation_analysis_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "capacity_boundary_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "monitoring_integration_report.json"))

        # Verify aliases
        assert os.path.exists(os.path.join(temp_dir, "test_architecture_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "system_resource_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "soak_test_report.json"))

        assert len(manifest.file_hashes) >= 16
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ─── 5. Runtime Orchestrator Tests ───────────────────────────────────────────

def test_runtime_orchestrator():
    temp_dir = tempfile.mkdtemp()
    try:
        runtime = PerformanceInfrastructureRuntime()
        rep = runtime.execute_verifier("3J.6.1")
        assert rep.verifier_id == "VERIFY-3J.6.1-PERF-TEST-ARCH"

        res = runtime.run_full_verification(output_dir=temp_dir)
        assert res["overall_score"] >= 95.0
        assert res["passed"] is True
        assert res["manifest"] is not None
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ─── 6. REST API Tests ───────────────────────────────────────────────────────

def test_rest_api_endpoints():
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    # Health
    resp = client.get("/api/v1/performance-infrastructure/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"

    # Phases
    resp = client.get("/api/v1/performance-infrastructure/phases")
    assert resp.status_code == 200
    phases = resp.json()
    assert len(phases) == 13

    # Run Suite
    resp = client.post("/api/v1/performance-infrastructure/run")
    assert resp.status_code == 200
    data = resp.json()
    assert data["passed"] is True
    assert data["overall_score"] >= 95.0

    # Specific Report
    resp = client.get("/api/v1/performance-infrastructure/reports/3J.6.1")
    assert resp.status_code == 200
    assert "components" in resp.json()

    # Specific Report 404
    resp = client.get("/api/v1/performance-infrastructure/reports/3J.6.NONEXISTENT")
    assert resp.status_code == 404

    # Manifest
    resp = client.get("/api/v1/performance-infrastructure/manifest")
    assert resp.status_code == 200
    assert "file_hashes" in resp.json()

    # Certification
    resp = client.get("/api/v1/performance-infrastructure/certification")
    assert resp.status_code == 200
    assert resp.json()["certification_tier"] == "Enterprise Performance Ready"
