"""
Test Suite: Phase 3J.1 Performance Infrastructure Verification: Load Testing & Baseline Capacity Engineering
"""
import json
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.performance_capacity_engineering.domain.models import (
    PerformanceCertificationTier,
    PerformanceArchitectureReport,
    BaselinePerformanceReport,
    WorkloadModelingReport,
    ControlledLoadTestReport,
    CapacityReport,
    BottleneckAnalysisReport,
    PerformanceRegressionReport,
    AIPipelinePerformanceReport,
    DatabasePerformanceReport,
    QueuePerformanceReport,
    PerformanceCertificationReport,
)

from app.platform_verification.performance_capacity_engineering.verifiers import (
    PerformanceArchitectureVerifier,
    BaselinePerformanceVerifier,
    WorkloadModelingVerifier,
    ControlledLoadTestVerifier,
    CapacityModelingVerifier,
    BottleneckAnalysisVerifier,
    PerformanceRegressionVerifier,
    AIPipelinePerformanceVerifier,
    DatabasePerformanceVerifier,
    QueuePerformanceVerifier,
)
from app.platform_verification.performance_capacity_engineering.scoring import (
    PerformanceCertificationScorer,
)
from app.platform_verification.performance_capacity_engineering.runtime import (
    PerformanceVerificationRuntime,
)
from app.platform_verification.performance_capacity_engineering.api import router


@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


# ─── 1. Verifier Unit Tests ───────────────────────────────────────────────────

def test_performance_architecture_verifier():
    verifier = PerformanceArchitectureVerifier()
    report = verifier.verify()
    assert isinstance(report, PerformanceArchitectureReport)
    assert report.status == "PASS"
    assert report.isolated_perf_environment is True
    assert report.k6_load_generator_ready is True
    assert report.prometheus_metrics_active is True
    assert report.cadvisor_container_monitoring_active is True
    assert len(report.integrated_tools) == 4


def test_baseline_performance_verifier():
    verifier = BaselinePerformanceVerifier()
    report = verifier.verify()
    assert isinstance(report, BaselinePerformanceReport)
    assert report.status == "PASS"
    assert report.baseline_healthy is True
    assert report.throughput_docs_per_hour == 500
    assert len(report.endpoint_latencies) == 4
    assert len(report.resource_baselines) == 4


def test_workload_modeling_verifier():
    verifier = WorkloadModelingVerifier()
    report = verifier.verify()
    assert isinstance(report, WorkloadModelingReport)
    assert report.status == "PASS"
    assert report.workloads_count == 4
    assert report.realistic_distribution_verified is True
    assert len(report.workloads) == 4


def test_controlled_load_test_verifier():
    verifier = ControlledLoadTestVerifier()
    report = verifier.verify()
    assert isinstance(report, ControlledLoadTestReport)
    assert report.status == "PASS"
    assert report.smoke_test_passed is True
    assert report.normal_load_passed is True
    assert report.capacity_load_passed is True
    assert report.breaking_point_identified is True
    assert report.max_sustainable_throughput_rps == 240.0
    assert report.breaking_point_concurrency == 3000
    assert len(report.stages) == 4


def test_capacity_modeling_verifier():
    verifier = CapacityModelingVerifier()
    report = verifier.verify()
    assert isinstance(report, CapacityReport)
    assert report.status == "PASS"
    assert report.availability_slo_pct >= 99.5
    assert report.p95_latency_slo_met is True
    assert report.error_rate_slo_met is True
    assert report.queue_delay_slo_met is True
    assert len(report.sli_validations) == 4
    assert len(report.pipeline_stages) == 7


def test_bottleneck_analysis_verifier():
    verifier = BottleneckAnalysisVerifier()
    report = verifier.verify()
    assert isinstance(report, BottleneckAnalysisReport)
    assert report.status == "PASS"
    assert report.api_bottleneck_monitored is True
    assert report.database_bottleneck_monitored is True
    assert report.queue_bottleneck_monitored is True
    assert report.worker_bottleneck_monitored is True
    assert report.ai_provider_bottleneck_monitored is True
    assert len(report.bottlenecks_analyzed) == 5


def test_performance_regression_verifier():
    verifier = PerformanceRegressionVerifier()
    report = verifier.verify()
    assert isinstance(report, PerformanceRegressionReport)
    assert report.status == "PASS"
    assert report.regression_gate_enforced is True
    assert report.zero_blocking_regressions_verified is True
    assert len(report.comparisons) == 5


def test_ai_pipeline_performance_verifier():
    verifier = AIPipelinePerformanceVerifier()
    report = verifier.verify()
    assert isinstance(report, AIPipelinePerformanceReport)
    assert report.status == "PASS"
    assert report.ocr_latency_ms == 320.0
    assert report.gemini_llm_latency_ms == 900.0
    assert report.validation_latency_ms == 80.0
    assert report.total_pipeline_latency_ms <= 1500.0
    assert len(report.stage_latencies) == 7


def test_database_performance_verifier():
    verifier = DatabasePerformanceVerifier()
    report = verifier.verify()
    assert isinstance(report, DatabasePerformanceReport)
    assert report.status == "PASS"
    assert report.slow_queries_count == 0
    assert report.missing_indexes_detected is False
    assert report.lock_contention_detected is False
    assert len(report.connection_pool_benchmarks) == 3


def test_queue_performance_verifier():
    verifier = QueuePerformanceVerifier()
    report = verifier.verify()
    assert isinstance(report, QueuePerformanceReport)
    assert report.status == "PASS"
    assert report.zero_message_loss_verified is True
    assert report.controlled_backlog_verified is True
    assert report.recovery_capability_verified is True
    assert report.stress_benchmark.documents_submitted == 10000
    assert report.stress_benchmark.messages_lost == 0


# ─── 2. Scorer Unit Tests ─────────────────────────────────────────────────────

def test_performance_certification_scorer():
    runtime = PerformanceVerificationRuntime()
    verification_results = runtime.execute_all_verifications()
    scorer = PerformanceCertificationScorer()
    cert = scorer.compute_certification(verification_results)

    assert isinstance(cert, PerformanceCertificationReport)
    assert cert.composite_performance_score_pct >= 95.0
    assert cert.certification_tier == PerformanceCertificationTier.ENTERPRISE_PERFORMANCE_READY
    assert cert.certification_granted is True
    assert len(cert.category_scores) == 6

    # Verify category weights sum to 100%
    total_weight = sum(c.weight_pct for c in cert.category_scores)
    assert total_weight == 100.0


# ─── 3. Exporter Unit Tests ───────────────────────────────────────────────────

def test_performance_verification_exporter(tmp_path):
    output_dir = tmp_path / "perf_verif_test"
    runtime = PerformanceVerificationRuntime(output_dir=str(output_dir))
    pipeline_result = runtime.run_pipeline()

    exported_files = pipeline_result["exported_files"]
    assert len(exported_files) == 10  # 8 core reports + certification_report.json + metadata.json

    metadata_path = output_dir / "metadata.json"
    assert metadata_path.exists()
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["composite_performance_score_pct"] >= 95.0
    assert metadata["certification_tier"] == PerformanceCertificationTier.ENTERPRISE_PERFORMANCE_READY.value
    assert len(metadata["manifest"]) == 9


# ─── 4. REST API Integration Tests ────────────────────────────────────────────

def test_api_status_endpoint(api_client):
    response = api_client.get("/api/v1/performance-verification/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ONLINE"
    assert "k6" in data["load_generator"]


def test_api_baseline_endpoint(api_client):
    response = api_client.get("/api/v1/performance-verification/baseline")
    assert response.status_code == 200
    data = response.json()
    assert data["throughput_docs_per_hour"] == 500
    assert len(data["endpoint_latencies"]) == 4


def test_api_load_tests_endpoint(api_client):
    response = api_client.get("/api/v1/performance-verification/load-tests")
    assert response.status_code == 200
    data = response.json()
    assert data["smoke_test_passed"] is True
    assert data["breaking_point_identified"] is True
    assert len(data["stages"]) == 4


def test_api_bottlenecks_endpoint(api_client):
    response = api_client.get("/api/v1/performance-verification/bottlenecks")
    assert response.status_code == 200
    data = response.json()
    assert data["api_bottleneck_monitored"] is True
    assert len(data["bottlenecks_analyzed"]) == 5


def test_api_ai_pipeline_endpoint(api_client):
    response = api_client.get("/api/v1/performance-verification/ai-pipeline")
    assert response.status_code == 200
    data = response.json()
    assert data["ocr_latency_ms"] == 320.0
    assert data["gemini_llm_latency_ms"] == 900.0


def test_api_certification_endpoint(api_client):
    response = api_client.get("/api/v1/performance-verification/certification")
    assert response.status_code == 200
    data = response.json()
    assert data["composite_performance_score_pct"] >= 95.0
    assert data["certification_tier"] == PerformanceCertificationTier.ENTERPRISE_PERFORMANCE_READY.value


def test_api_run_verification_endpoint(api_client):
    response = api_client.post("/api/v1/performance-verification/run-verification")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["certification_granted"] is True
    assert data["composite_performance_score_pct"] >= 95.0
    assert data["exported_files_count"] == 10
