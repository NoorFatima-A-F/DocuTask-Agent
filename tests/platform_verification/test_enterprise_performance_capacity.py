"""Comprehensive Test Suite for Phase 3J.5 Enterprise Performance Baseline & Capacity Verification Framework."""

import json
import os
import shutil
import tempfile
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.platform_verification.enterprise_performance_capacity.api.performance_quality_api import (
    router,
)
from app.platform_verification.enterprise_performance_capacity.domain.models import (
    AIWorkloadReport,
    BaseVerificationReport,
    BottleneckAnalysisReport,
    CapacityPlanReport,
    ControlledLoadTestReport,
    DatabasePerformanceReport,
    EnduranceTestReport,
    EnterprisePerformanceCertificationReport,
    EnterprisePerformanceTier,
    LatencyBreakdownReport,
    LoadTestReport,
    PerformanceBaselineReport,
    PerformanceRegressionReport,
    PerformanceVerificationManifest,
    PerformanceVerificationStatus,
    QueuePerformanceReport,
    ResourceUtilizationReport,
    SpikeTestReport,
    StoragePerformanceReport,
    StressTestReport,
    ThroughputCapacityReport,
    VerificationStatus,
)
from app.platform_verification.enterprise_performance_capacity.exporter.performance_quality_exporter import (
    PerformanceQualityExporter,
)
from app.platform_verification.enterprise_performance_capacity.runtime.performance_quality_runtime import (
    PerformanceQualityRuntime,
)
from app.platform_verification.enterprise_performance_capacity.scoring.performance_quality_scorer import (
    PerformanceQualityScorer,
)
from app.platform_verification.enterprise_performance_capacity.verifiers import (
    get_all_verifiers,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.ai_workload_verifier import (
    AIWorkloadVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.bottleneck_analysis_verifier import (
    BottleneckAnalysisVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.capacity_planning_verifier import (
    CapacityPlanningVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.database_performance_verifier import (
    DatabasePerformanceVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.endurance_testing_verifier import (
    EnduranceTestingVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.latency_breakdown_verifier import (
    LatencyBreakdownVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.load_testing_verifier import (
    LoadTestingVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.performance_baseline_verifier import (
    PerformanceBaselineVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.performance_regression_verifier import (
    PerformanceRegressionVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.queue_performance_verifier import (
    QueuePerformanceVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.resource_utilization_verifier import (
    ResourceUtilizationVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.spike_testing_verifier import (
    SpikeTestingVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.storage_performance_verifier import (
    StoragePerformanceVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.stress_testing_verifier import (
    StressTestingVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.throughput_capacity_verifier import (
    ThroughputCapacityVerifier,
)


# ─── 1. Domain Models Tests ───────────────────────────────────────────────────

def test_domain_models_instantiation():
    base = BaseVerificationReport(
        verifier_id="VERIFY-TEST",
        phase_id="3J.5.TEST",
        phase_name="Test Phase",
        status=VerificationStatus.PASSED,
        score=100.0,
    )
    assert base.phase_id == "3J.5.TEST"
    assert base.status == VerificationStatus.PASSED

    cert = EnterprisePerformanceCertificationReport(
        verifier_id="VERIFY-3J.5.18-CERT",
        phase_id="3J.5.18",
        phase_name="Certification",
        overall_score=100.0,
        certification_tier=EnterprisePerformanceTier.ENTERPRISE_PERFORMANCE_READY,
    )
    assert cert.certification_tier == EnterprisePerformanceTier.ENTERPRISE_PERFORMANCE_READY
    assert cert.overall_score == 100.0


# ─── 2. All 15 Verifiers Individual Tests ─────────────────────────────────────

def test_all_verifiers_registered():
    verifiers = get_all_verifiers()
    assert len(verifiers) == 15
    phase_ids = [v.phase_id for v in verifiers]
    expected_ids = [
        "3J.5.1", "3J.5.2", "3J.5.3", "3J.5.4", "3J.5.6", "3J.5.7", "3J.5.8",
        "3J.5.9", "3J.5.10", "3J.5.11", "3J.5.12", "3J.5.13", "3J.5.14", "3J.5.15", "3J.5.16"
    ]
    assert phase_ids == expected_ids


def test_3j_5_1_baseline_verifier():
    v = PerformanceBaselineVerifier()
    rep = v.verify()
    assert isinstance(rep, PerformanceBaselineReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.score >= 95.0
    assert rep.baseline.api_latency_p95 == "42.0ms"
    assert rep.baseline.document_processing_time == "1.08s"
    assert rep.api_throughput_rps == 245.0


def test_3j_5_2_latency_breakdown_verifier():
    v = LatencyBreakdownVerifier()
    rep = v.verify()
    assert isinstance(rep, LatencyBreakdownReport)
    assert rep.status == VerificationStatus.PASSED
    assert len(rep.components) == 7
    total = sum(c.latency_ms for c in rep.components)
    assert total == 1085.0
    assert rep.total_processing_latency_ms == 1085.0
    assert rep.p95_sla_compliant is True


def test_3j_5_3_throughput_capacity_verifier():
    v = ThroughputCapacityVerifier()
    rep = v.verify()
    assert isinstance(rep, ThroughputCapacityReport)
    assert rep.status == VerificationStatus.PASSED
    assert len(rep.document_classes) == 3
    assert rep.total_completed_documents == 2000
    assert rep.total_failed_documents == 0
    assert rep.aggregate_throughput_docs_per_hour == 1200


def test_3j_5_4_load_testing_verifier():
    v = LoadTestingVerifier()
    rep = v.verify()
    assert isinstance(rep, ControlledLoadTestReport)
    assert rep.status == VerificationStatus.PASSED
    assert len(rep.profiles) == 3
    assert rep.max_concurrent_users == 1000
    assert rep.stability_duration_minutes == 30


def test_3j_5_6_stress_testing_verifier():
    v = StressTestingVerifier()
    rep = v.verify()
    assert isinstance(rep, StressTestReport)
    assert rep.status == VerificationStatus.PASSED
    assert len(rep.stress_levels) == 4
    assert rep.max_sustainable_users == 2000
    assert rep.breaking_point_characterized is True


def test_3j_5_7_spike_testing_verifier():
    v = SpikeTestingVerifier()
    rep = v.verify()
    assert isinstance(rep, SpikeTestReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.baseline_rate_dph == 100
    assert rep.peak_surge_dph == 10000
    assert rep.recovery_time_seconds == 38.0
    assert rep.dropped_requests_count == 0
    assert rep.absorption_verified is True


def test_3j_5_8_endurance_testing_verifier():
    v = EnduranceTestingVerifier()
    rep = v.verify()
    assert isinstance(rep, EnduranceTestReport)
    assert rep.status == VerificationStatus.PASSED
    assert len(rep.checkpoints) == 4
    assert rep.duration_hours == 72
    assert rep.memory_leak_detected is False
    assert rep.worker_degradation_detected is False


def test_3j_5_9_ai_workload_verifier():
    v = AIWorkloadVerifier()
    rep = v.verify()
    assert isinstance(rep, AIWorkloadReport)
    assert rep.status == VerificationStatus.PASSED
    assert len(rep.variance_samples) == 10
    assert rep.retry_percentage == 0.0
    assert rep.avg_ai_cost_per_doc_usd == 0.0012


def test_3j_5_10_queue_performance_verifier():
    v = QueuePerformanceVerifier()
    rep = v.verify()
    assert isinstance(rep, QueuePerformanceReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.consumer_rate_jobs_min >= rep.producer_rate_jobs_min
    assert rep.zero_job_loss_verified is True
    assert rep.peak_queue_depth == 480


def test_3j_5_11_database_performance_verifier():
    v = DatabasePerformanceVerifier()
    rep = v.verify()
    assert isinstance(rep, DatabasePerformanceReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.p95_query_latency_ms == 15.2
    assert rep.lock_contention_events == 0
    assert rep.slow_queries_count == 0


def test_3j_5_12_storage_performance_verifier():
    v = StoragePerformanceVerifier()
    rep = v.verify()
    assert isinstance(rep, StoragePerformanceReport)
    assert rep.status == VerificationStatus.PASSED
    assert len(rep.file_benchmarks) == 3
    assert rep.zero_corruption_verified is True
    assert rep.zero_timeout_verified is True


def test_3j_5_13_resource_utilization_verifier():
    v = ResourceUtilizationVerifier()
    rep = v.verify()
    assert isinstance(rep, ResourceUtilizationReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.avg_cpu_pct < 50.0
    assert rep.memory_growth_slope_mb_hr < 1.0


def test_3j_5_14_bottleneck_analysis_verifier():
    v = BottleneckAnalysisVerifier()
    rep = v.verify()
    assert isinstance(rep, BottleneckAnalysisReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.primary_bottleneck_identified == "AI Inference (Gemini API)"
    assert len(rep.categories) == 7


def test_3j_5_15_capacity_planning_verifier():
    v = CapacityPlanningVerifier()
    rep = v.verify()
    assert isinstance(rep, CapacityPlanReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.required_workers == 84
    assert rep.scaling_plan_feasible is True


def test_3j_5_16_performance_regression_verifier():
    v = PerformanceRegressionVerifier()
    rep = v.verify()
    assert isinstance(rep, PerformanceRegressionReport)
    assert rep.status == VerificationStatus.PASSED
    assert rep.regression_detected is False
    assert rep.pipeline_gate_passed is True


# ─── 3. Scorer Tests ─────────────────────────────────────────────────────────

def test_scorer_calculation():
    verifiers = get_all_verifiers()
    reports = {}
    for v in verifiers:
        reports[v.verifier_id] = v.verify()

    scorer = PerformanceQualityScorer()
    cert = scorer.score_reports(reports)

    assert cert.phase_id == "3J.5.18"
    assert len(cert.category_scores) == 6
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

        scorer = PerformanceQualityScorer()
        cert = scorer.score_reports(reports)

        exporter = PerformanceQualityExporter()
        manifest = exporter.export_all(reports, cert, output_dir=temp_dir)

        assert isinstance(manifest, PerformanceVerificationManifest)
        assert manifest.passed is True
        assert os.path.exists(os.path.join(temp_dir, "metadata.json"))
        assert os.path.exists(os.path.join(temp_dir, "certification_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "baseline_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "latency_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "throughput_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "load_test_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "stress_test_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "spike_test_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "endurance_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "ai_workload_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "queue_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "database_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "storage_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "resource_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "bottleneck_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "capacity_plan.json"))
        assert os.path.exists(os.path.join(temp_dir, "regression_report.json"))

        # Verify aliases
        assert os.path.exists(os.path.join(temp_dir, "performance_baseline_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "ai_pipeline_report.json"))
        assert os.path.exists(os.path.join(temp_dir, "resource_utilization_report.json"))

        assert len(manifest.file_hashes) >= 18
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ─── 5. Runtime Orchestrator Tests ───────────────────────────────────────────

def test_runtime_orchestrator():
    temp_dir = tempfile.mkdtemp()
    try:
        runtime = PerformanceQualityRuntime()
        rep = runtime.execute_verifier("3J.5.1")
        assert rep.verifier_id == "VERIFY-3J.5.1-PERF-BASELINE"

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
    resp = client.get("/api/v1/performance-verification/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"

    # Phases
    resp = client.get("/api/v1/performance-verification/phases")
    assert resp.status_code == 200
    phases = resp.json()
    assert len(phases) == 15

    # Run Suite
    resp = client.post("/api/v1/performance-verification/run")
    assert resp.status_code == 200
    data = resp.json()
    assert data["passed"] is True
    assert data["overall_score"] >= 95.0

    # Specific Report
    resp = client.get("/api/v1/performance-verification/reports/3J.5.1")
    assert resp.status_code == 200
    assert "baseline" in resp.json()

    # Specific Report 404
    resp = client.get("/api/v1/performance-verification/reports/3J.5.NONEXISTENT")
    assert resp.status_code == 404

    # Manifest
    resp = client.get("/api/v1/performance-verification/manifest")
    assert resp.status_code == 200
    assert "file_hashes" in resp.json()

    # Certification
    resp = client.get("/api/v1/performance-verification/certification")
    assert resp.status_code == 200
    assert resp.json()["certification_tier"] == "Enterprise Performance Ready"
