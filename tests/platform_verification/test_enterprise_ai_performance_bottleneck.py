"""Phase 3J.9: Enterprise AI Workload Performance Bottleneck Analysis & Capacity Verification — Test Suite.

Tests:
- Domain model instantiation
- Verifier registry (12 verifiers)
- Individual verifier execution (3J.9.1–3J.9.12)
- 6-category quality scorer
- SHA-256 exporter with manifest
- Runtime orchestrator
- REST API endpoints
"""

import json
import os
import sys
import tempfile


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from app.platform_verification.enterprise_ai_performance_bottleneck.domain.models import (
    AIModelPerformanceReport,
    AIPerformanceVerificationManifest,
    BaseVerificationReport,
    CapacityPlanReport,
    CategoryScore,
    CheckResult,
    DatabasePerformanceReport,
    EnterpriseAIPerformanceCertificationReport,
    EnterprisePerformanceTier,
    LatencyBreakdownReport,
    PerformanceArchitectureReport,
    PerformanceFailureReport,
    PerformanceObservabilityReport,
    PerformanceRegressionReport,
    QueueCapacityReport,
    ResourceBottleneckReport,
    ThroughputCapacityReport,
    VerificationStatus,
    WorkerScalingReport,
)

PerformanceCertificationReport = EnterpriseAIPerformanceCertificationReport
PerformanceVerificationStatus = VerificationStatus
CertificationTier = EnterprisePerformanceTier

from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers import (
    get_all_verifiers,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.architecture_modeling_verifier import (
    PerformanceArchitectureModelingVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.latency_profiling_verifier import (
    LatencyProfilingVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.throughput_capacity_verifier import (
    ThroughputCapacityVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.resource_bottleneck_verifier import (
    ResourceBottleneckVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.database_performance_verifier import (
    DatabasePerformanceVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.queue_capacity_verifier import (
    QueueCapacityVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.worker_scaling_verifier import (
    WorkerScalingVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.ai_model_performance_verifier import (
    AIModelPerformanceVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.performance_regression_verifier import (
    PerformanceRegressionVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.capacity_planning_verifier import (
    CapacityPlanningVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.performance_failure_verifier import (
    PerformanceFailureSimulationVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.performance_observability_verifier import (
    PerformanceObservabilityVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.scoring.ai_performance_scorer import (
    AIPerformanceScorer,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.exporter.ai_performance_exporter import (
    AIPerformanceExporter,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.runtime.ai_performance_runtime import (
    AIPerformanceRuntime,
)


# ────────────────────────────────────────────────────────────────────────────────
# 1. Domain Model Instantiation
# ────────────────────────────────────────────────────────────────────────────────

def test_domain_models_instantiation():
    """Verify all 3J.9 domain models can be instantiated with defaults."""
    report_classes = [
        BaseVerificationReport,
        PerformanceArchitectureReport,
        LatencyBreakdownReport,
        ThroughputCapacityReport,
        ResourceBottleneckReport,
        DatabasePerformanceReport,
        QueueCapacityReport,
        WorkerScalingReport,
        AIModelPerformanceReport,
        PerformanceRegressionReport,
        CapacityPlanReport,
        PerformanceFailureReport,
        PerformanceObservabilityReport,
        EnterpriseAIPerformanceCertificationReport,
        AIPerformanceVerificationManifest,
    ]
    for cls in report_classes:
        obj = cls()
        assert obj is not None, f"Failed to instantiate {cls.__name__}"

    check = CheckResult(name="Test", passed=True, details="OK")
    assert check.passed is True

    cat = CategoryScore(category="Test", weight=0.20, score=100.0, weighted_score=20.0, description="Test")
    assert cat.weighted_score == 20.0


# ────────────────────────────────────────────────────────────────────────────────
# 2. Verifier Registry
# ────────────────────────────────────────────────────────────────────────────────

def test_all_verifiers_registered():
    """Verify exactly 12 verifiers are registered in proper order."""
    verifiers = get_all_verifiers()
    assert len(verifiers) == 12

    expected_phases = [
        "3J.9.1", "3J.9.2", "3J.9.3", "3J.9.4", "3J.9.5", "3J.9.6",
        "3J.9.7", "3J.9.8", "3J.9.9", "3J.9.10", "3J.9.11", "3J.9.12",
    ]
    for v, expected in zip(verifiers, expected_phases):
        assert expected in v.verifier_id, f"Expected {expected} in {v.verifier_id}"
        assert v.phase_id == expected


# ────────────────────────────────────────────────────────────────────────────────
# 3. Individual Verifier Tests (3J.9.1–3J.9.12)
# ────────────────────────────────────────────────────────────────────────────────

def test_3j_9_1_architecture_modeling_verifier():
    verifier = PerformanceArchitectureModelingVerifier()
    report = verifier.verify()
    assert isinstance(report, PerformanceArchitectureReport)
    assert report.status == VerificationStatus.PASSED
    assert report.components_count == 12
    assert report.dependencies_count == 18
    assert report.critical_paths_count == 5
    assert len(report.component_capacities) == 12
    assert report.architecture_analyzed
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_9_2_latency_profiling_verifier():
    verifier = LatencyProfilingVerifier()
    report = verifier.verify()
    assert isinstance(report, LatencyBreakdownReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.stages) == 6
    assert report.total_latency_ms < 5000.0
    assert report.ai_latency_percentage > 50.0
    assert report.ocr_latency_percentage > 30.0
    assert report.sla_compliant
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_9_3_throughput_capacity_verifier():
    verifier = ThroughputCapacityVerifier()
    report = verifier.verify()
    assert isinstance(report, ThroughputCapacityReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.workload_tiers) == 4
    assert report.max_sustainable_dph == 4800
    assert report.saturation_threshold_dph == 6000
    assert report.peak_success_rate_pct == 100.0
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_9_4_resource_bottleneck_verifier():
    verifier = ResourceBottleneckVerifier()
    report = verifier.verify()
    assert isinstance(report, ResourceBottleneckReport)
    assert report.status == VerificationStatus.PASSED
    assert not report.cpu_metrics.bottleneck_detected
    assert not report.memory_metrics.bottleneck_detected
    assert not report.disk_metrics.bottleneck_detected
    assert not report.network_metrics.bottleneck_detected
    assert report.soak_72h_stable
    assert not report.memory_leak_detected
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_9_5_database_performance_verifier():
    verifier = DatabasePerformanceVerifier()
    report = verifier.verify()
    assert isinstance(report, DatabasePerformanceReport)
    assert report.status == VerificationStatus.PASSED
    assert report.active_connections == 42
    assert report.cache_hit_ratio_pct >= 99.0
    assert report.deadlocks_detected == 0
    assert report.missing_indexes_count == 0
    assert len(report.slow_queries) == 3
    assert all(q.index_used for q in report.slow_queries)
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_9_6_queue_capacity_verifier():
    verifier = QueueCapacityVerifier()
    report = verifier.verify()
    assert isinstance(report, QueueCapacityReport)
    assert report.status == VerificationStatus.PASSED
    assert report.processing_rate_jpm > report.enqueue_rate_jpm
    assert report.queue_drain_time_sec < 300.0
    assert report.data_loss_count == 0
    assert report.queue_stable_under_spike
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_9_7_worker_scaling_verifier():
    verifier = WorkerScalingVerifier()
    report = verifier.verify()
    assert isinstance(report, WorkerScalingReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.scaling_points) == 4
    assert report.scaling_linearity_pct > 80.0
    assert report.optimal_worker_count == 40
    assert not report.shared_resource_bottleneck_detected
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_9_8_ai_model_performance_verifier():
    verifier = AIModelPerformanceVerifier()
    report = verifier.verify()
    assert isinstance(report, AIModelPerformanceReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.models) == 2
    assert report.models[0].model_name == "Gemini 1.5 Pro"
    assert report.models[1].model_name == "Gemini 1.5 Flash"
    assert report.ai_latency_percentage == 55.0
    assert report.ocr_latency_percentage == 30.0
    assert report.db_latency_percentage == 15.0
    assert report.gemini_quota_safe
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_9_9_performance_regression_verifier():
    verifier = PerformanceRegressionVerifier()
    report = verifier.verify()
    assert isinstance(report, PerformanceRegressionReport)
    assert report.status == VerificationStatus.PASSED
    assert report.baseline_version == "v1.0"
    assert report.current_version == "v1.1"
    assert len(report.comparisons) == 5
    assert report.regressions_detected == 0
    assert report.deployment_approved
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_9_10_capacity_planning_verifier():
    verifier = CapacityPlanningVerifier()
    report = verifier.verify()
    assert isinstance(report, CapacityPlanReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.projections) == 3
    assert report.projections[1].target_docs_per_day == 100000
    assert report.projections[2].target_docs_per_day == 500000
    assert report.capacity_model_validated
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_9_11_performance_failure_verifier():
    verifier = PerformanceFailureSimulationVerifier()
    report = verifier.verify()
    assert isinstance(report, PerformanceFailureReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.scenarios) == 4
    assert all(s.passed for s in report.scenarios)
    assert all(s.data_loss == 0 for s in report.scenarios)
    assert report.worker_saturation_handled
    assert report.db_slowdown_graceful
    assert report.ai_slowdown_handled
    assert report.memory_pressure_alerted
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_9_12_performance_observability_verifier():
    verifier = PerformanceObservabilityVerifier()
    report = verifier.verify()
    assert isinstance(report, PerformanceObservabilityReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.signals) == 10
    assert all(s.collected for s in report.signals)
    assert all(s.dashboard_mapped for s in report.signals)
    assert report.golden_signals_active
    assert report.ai_telemetry_integrated
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


# ────────────────────────────────────────────────────────────────────────────────
# 4. 6-Category Quality Scorer
# ────────────────────────────────────────────────────────────────────────────────

def test_scorer_calculation():
    """Verify 6-category weighted scoring with expected weights."""
    verifiers = get_all_verifiers()
    reports = {}
    for v in verifiers:
        reports[v.verifier_id] = v.verify()

    scorer = AIPerformanceScorer()
    cert = scorer.score_reports(reports)

    assert isinstance(cert, EnterpriseAIPerformanceCertificationReport)
    assert cert.overall_score == 100.0
    assert cert.certification_tier == EnterprisePerformanceTier.ENTERPRISE_PERFORMANCE_READY
    assert cert.passed is True
    assert len(cert.category_scores) == 6

    expected_weights = [0.20, 0.20, 0.20, 0.15, 0.15, 0.10]
    for cat, w in zip(cert.category_scores, expected_weights):
        assert cat.weight == w, f"{cat.category} weight mismatch: {cat.weight} != {w}"
        assert cat.score == 100.0

    total_weight = sum(c.weight for c in cert.category_scores)
    assert abs(total_weight - 1.0) < 0.01


# ────────────────────────────────────────────────────────────────────────────────
# 5. SHA-256 Exporter
# ────────────────────────────────────────────────────────────────────────────────

def test_exporter_manifest_and_files():
    """Verify exporter generates all reports with SHA-256 integrity manifest."""
    with tempfile.TemporaryDirectory() as tmpdir:
        verifiers = get_all_verifiers()
        reports = {v.verifier_id: v.verify() for v in verifiers}

        scorer = AIPerformanceScorer()
        cert = scorer.score_reports(reports)

        exporter = AIPerformanceExporter()
        manifest = exporter.export_all(reports, cert, output_dir=tmpdir)

        assert isinstance(manifest, AIPerformanceVerificationManifest)
        assert manifest.passed is True
        assert manifest.overall_score == 100.0
        assert len(manifest.file_hashes) > 12

        expected_files = [
            "architecture_report.json",
            "latency_report.json",
            "throughput_report.json",
            "bottleneck_report.json",
            "database_report.json",
            "queue_report.json",
            "worker_report.json",
            "ai_report.json",
            "regression_report.json",
            "capacity_report.json",
            "failure_report.json",
            "observability_report.json",
            "certification_report.json",
        ]
        for fname in expected_files:
            assert os.path.exists(os.path.join(tmpdir, fname)), f"Missing file: {fname}"

        expected_aliases = [
            "performance_architecture_report.json",
            "latency_breakdown_report.json",
            "throughput_capacity_report.json",
            "resource_bottleneck_report.json",
            "database_performance_report.json",
            "queue_capacity_report.json",
            "worker_scaling_report.json",
            "ai_performance_report.json",
            "performance_regression_report.json",
            "capacity_plan_report.json",
            "performance_failure_report.json",
            "performance_observability_report.json",
        ]
        for alias in expected_aliases:
            assert os.path.exists(os.path.join(tmpdir, alias)), f"Missing alias: {alias}"

        assert os.path.exists(os.path.join(tmpdir, "metadata.json"))
        with open(os.path.join(tmpdir, "metadata.json"), "r") as f:
            meta = json.load(f)
        assert "file_hashes" in meta
        assert len(meta["file_hashes"]) == len(manifest.file_hashes)


# ────────────────────────────────────────────────────────────────────────────────
# 6. Runtime Orchestrator
# ────────────────────────────────────────────────────────────────────────────────

def test_runtime_orchestrator():
    """Verify runtime runs all verifiers, scores, and exports."""
    with tempfile.TemporaryDirectory() as tmpdir:
        runtime = AIPerformanceRuntime()
        result = runtime.run_full_verification(output_dir=tmpdir)

        assert "reports" in result
        assert "certification" in result
        assert "manifest" in result
        assert result["passed"] is True
        assert result["overall_score"] == 100.0
        assert result["tier"] == "Enterprise Performance Ready"
        assert len(result["reports"]) == 12

        cert = runtime.get_latest_certification()
        assert cert is not None
        assert cert.overall_score == 100.0


# ────────────────────────────────────────────────────────────────────────────────
# 7. REST API Endpoints
# ────────────────────────────────────────────────────────────────────────────────

def test_rest_api_endpoints():
    """Verify FastAPI router configuration and endpoint availability."""
    from app.platform_verification.enterprise_ai_performance_bottleneck.api.ai_performance_api import router

    assert router.prefix == "/api/v1/ai-performance"
    route_paths = [r.path for r in router.routes]
    prefix = "/api/v1/ai-performance"
    assert f"{prefix}/health" in route_paths
    assert f"{prefix}/phases" in route_paths
    assert f"{prefix}/run" in route_paths
    assert f"{prefix}/reports/{{phase_id}}" in route_paths
    assert f"{prefix}/certification" in route_paths
    assert f"{prefix}/manifest" in route_paths
