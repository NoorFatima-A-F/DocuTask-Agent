"""Phase 3J.7: Enterprise Performance Bottleneck Discovery & Capacity Engineering — Test Suite.

Tests:
- Domain model instantiation
- Verifier registry (10 verifiers)
- Individual verifier execution (3J.7.1–3J.7.10)
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

from app.platform_verification.enterprise_performance_bottleneck.domain.models import (
    BaseVerificationReport,
    BottleneckVerificationManifest,
    CategoryScore,
    CheckResult,
    EnterpriseBottleneckCertificationReport,
    EnterprisePerformanceTier,
    PerformanceArchitectureReport,
    ResourceSaturationReport,
    ApplicationBottleneckReport,
    DatabaseBottleneckReport,
    QueueBottleneckReport,
    WorkerCapacityReport,
    AIProviderPerformanceReport,
    PerformanceRegressionReport,
    CapacityBoundaryReport,
    OptimizationRecommendationsReport,
    VerificationStatus,
)

PerformanceCertificationReport = EnterpriseBottleneckCertificationReport
PerformanceVerificationStatus = VerificationStatus
CertificationTier = EnterprisePerformanceTier

from app.platform_verification.enterprise_performance_bottleneck.verifiers import (
    get_all_verifiers,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.architecture_profiling_verifier import (
    PerformanceArchitectureVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.resource_saturation_verifier import (
    ResourceSaturationVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.application_bottleneck_verifier import (
    ApplicationBottleneckVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.database_bottleneck_verifier import (
    DatabaseBottleneckVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.queue_bottleneck_verifier import (
    QueueBottleneckVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.worker_capacity_verifier import (
    WorkerCapacityVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.ai_provider_verifier import (
    AIProviderPerformanceVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.regression_detection_verifier import (
    PerformanceRegressionVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.capacity_boundary_verifier import (
    CapacityBoundaryVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.optimization_recommendations_verifier import (
    OptimizationRecommendationsVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.scoring.bottleneck_discovery_scorer import (
    BottleneckDiscoveryScorer,
)
from app.platform_verification.enterprise_performance_bottleneck.exporter.bottleneck_discovery_exporter import (
    BottleneckDiscoveryExporter,
)
from app.platform_verification.enterprise_performance_bottleneck.runtime.bottleneck_discovery_runtime import (
    BottleneckDiscoveryRuntime,
)


# ────────────────────────────────────────────────────────────────────────────────
# 1. Domain Model Instantiation
# ────────────────────────────────────────────────────────────────────────────────

def test_domain_models_instantiation():
    """Verify all domain models can be instantiated with defaults."""
    report_classes = [
        BaseVerificationReport,
        PerformanceArchitectureReport,
        ResourceSaturationReport,
        ApplicationBottleneckReport,
        DatabaseBottleneckReport,
        QueueBottleneckReport,
        WorkerCapacityReport,
        AIProviderPerformanceReport,
        PerformanceRegressionReport,
        CapacityBoundaryReport,
        OptimizationRecommendationsReport,
        EnterpriseBottleneckCertificationReport,
        BottleneckVerificationManifest,
    ]
    for cls in report_classes:
        obj = cls()
        assert obj is not None, f"Failed to instantiate {cls.__name__}"

    check = CheckResult(name="Test", passed=True, details="OK")
    assert check.passed is True

    cat = CategoryScore(category="Test", weight=0.25, score=100.0, weighted_score=25.0, description="Test")
    assert cat.weighted_score == 25.0


# ────────────────────────────────────────────────────────────────────────────────
# 2. Verifier Registry
# ────────────────────────────────────────────────────────────────────────────────

def test_all_verifiers_registered():
    """Verify exactly 10 verifiers are registered in proper order."""
    verifiers = get_all_verifiers()
    assert len(verifiers) == 10

    expected_phases = [
        "3J.7.1", "3J.7.2", "3J.7.3", "3J.7.4", "3J.7.5",
        "3J.7.6", "3J.7.7", "3J.7.8", "3J.7.9", "3J.7.10",
    ]
    for v, expected in zip(verifiers, expected_phases):
        assert expected in v.verifier_id, f"Expected {expected} in {v.verifier_id}"
        assert v.phase_id == expected


# ────────────────────────────────────────────────────────────────────────────────
# 3. Individual Verifier Tests (3J.7.1–3J.7.10)
# ────────────────────────────────────────────────────────────────────────────────

def test_3j_7_1_architecture_profiling_verifier():
    verifier = PerformanceArchitectureVerifier()
    report = verifier.verify()
    assert isinstance(report, PerformanceArchitectureReport)
    assert report.status == VerificationStatus.PASSED
    assert report.services_count == 8
    assert report.dependencies_count == 12
    assert len(report.critical_path) == 5
    assert "API Gateway" in report.critical_path
    assert "AI Providers" in report.critical_path
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_7_2_resource_saturation_verifier():
    verifier = ResourceSaturationVerifier()
    report = verifier.verify()
    assert isinstance(report, ResourceSaturationReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.resource_metrics) == 4
    assert not report.cpu_saturation_detected
    assert not report.memory_saturation_detected
    assert not report.disk_saturation_detected
    assert not report.network_saturation_detected
    assert all(m.headroom_pct > 30.0 for m in report.resource_metrics)
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_7_3_application_bottleneck_verifier():
    verifier = ApplicationBottleneckVerifier()
    report = verifier.verify()
    assert isinstance(report, ApplicationBottleneckReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.bottlenecks) == 9
    assert not report.api_bottleneck_detected
    assert not report.agent_runtime_bottleneck_detected
    assert not report.worker_bottleneck_detected
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_7_4_database_bottleneck_verifier():
    verifier = DatabaseBottleneckVerifier()
    report = verifier.verify()
    assert isinstance(report, DatabaseBottleneckReport)
    assert report.status == VerificationStatus.PASSED
    assert report.slow_queries_count == 4
    assert len(report.slow_queries) == 4
    assert report.connection_utilization_pct == 82.0
    assert report.deadlocks_detected == 0
    assert not report.pool_exhaustion_detected
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_7_5_queue_bottleneck_verifier():
    verifier = QueueBottleneckVerifier()
    report = verifier.verify()
    assert isinstance(report, QueueBottleneckReport)
    assert report.status == VerificationStatus.PASSED
    assert report.processing_rate_jobs_min >= report.enqueue_rate_jobs_min
    assert not report.queue_growth_detected
    assert not report.worker_capacity_shortage
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_7_6_worker_capacity_verifier():
    verifier = WorkerCapacityVerifier()
    report = verifier.verify()
    assert isinstance(report, WorkerCapacityReport)
    assert report.status == VerificationStatus.PASSED
    assert report.capacity_model is not None
    assert report.capacity_model.single_worker_throughput_dpm == 25.0
    assert report.capacity_model.required_workers == 40
    assert report.capacity_model.surplus_deficit >= 0
    assert report.horizontal_scaling_validated
    assert report.max_effective_workers == 80
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_7_7_ai_provider_verifier():
    verifier = AIProviderPerformanceVerifier()
    report = verifier.verify()
    assert isinstance(report, AIProviderPerformanceReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.providers) == 2
    assert report.providers[0].provider_name == "Gemini Pro"
    assert report.providers[1].provider_name == "Gemini Flash"
    assert not report.worker_blocking_under_ai_stress
    assert len(report.optimization_recommendations) >= 3
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_7_8_regression_detection_verifier():
    verifier = PerformanceRegressionVerifier()
    report = verifier.verify()
    assert isinstance(report, PerformanceRegressionReport)
    assert report.status == VerificationStatus.PASSED
    assert report.baseline_version == "v1.0"
    assert report.current_version == "v1.1"
    assert len(report.comparisons) == 6
    assert report.regressions_found == 0
    assert report.within_tolerance
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_7_9_capacity_boundary_verifier():
    verifier = CapacityBoundaryVerifier()
    report = verifier.verify()
    assert isinstance(report, CapacityBoundaryReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.stages) == 5
    zones = [s.zone for s in report.stages]
    assert "Normal" in zones
    assert "Warning" in zones
    assert "Failure" in zones
    assert report.normal_capacity_max_users == 500
    assert report.warning_zone_start_users == 1000
    assert report.failure_zone_start_users == 5000
    assert report.operating_boundary_defined
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_7_10_optimization_recommendations_verifier():
    verifier = OptimizationRecommendationsVerifier()
    report = verifier.verify()
    assert isinstance(report, OptimizationRecommendationsReport)
    assert report.status == VerificationStatus.PASSED
    assert report.total_recommendations == 6
    assert report.high_priority_count >= 1
    assert report.architecture_changes >= 1
    assert report.database_optimizations >= 1
    assert report.ai_optimizations >= 1
    assert report.caching_opportunities >= 1
    assert all(r.evidence for r in report.recommendations)
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

    scorer = BottleneckDiscoveryScorer()
    cert = scorer.score_reports(reports)

    assert isinstance(cert, EnterpriseBottleneckCertificationReport)
    assert cert.overall_score == 100.0
    assert cert.certification_tier == EnterprisePerformanceTier.ENTERPRISE_PERFORMANCE_READY
    assert cert.passed is True
    assert len(cert.category_scores) == 6

    expected_weights = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]
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

        scorer = BottleneckDiscoveryScorer()
        cert = scorer.score_reports(reports)

        exporter = BottleneckDiscoveryExporter()
        manifest = exporter.export_all(reports, cert, output_dir=tmpdir)

        assert isinstance(manifest, BottleneckVerificationManifest)
        assert manifest.passed is True
        assert manifest.overall_score == 100.0
        assert len(manifest.file_hashes) > 10

        expected_files = [
            "architecture_profile.json",
            "resource_report.json",
            "bottleneck_report.json",
            "database_report.json",
            "queue_report.json",
            "worker_capacity_report.json",
            "ai_latency_report.json",
            "regression_report.json",
            "capacity_model.json",
            "optimization_report.json",
            "certification_report.json",
        ]
        for fname in expected_files:
            assert os.path.exists(os.path.join(tmpdir, fname)), f"Missing file: {fname}"

        expected_aliases = [
            "performance_architecture_map.json",
            "resource_saturation_report.json",
            "ai_performance_report.json",
            "capacity_boundary_report.json",
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
        runtime = BottleneckDiscoveryRuntime()
        result = runtime.run_full_verification(output_dir=tmpdir)

        assert "reports" in result
        assert "certification" in result
        assert "manifest" in result
        assert result["passed"] is True
        assert result["overall_score"] == 100.0
        assert result["tier"] == "Enterprise Performance Engineering Ready"
        assert len(result["reports"]) == 10

        cert = runtime.get_latest_certification()
        assert cert is not None
        assert cert.overall_score == 100.0


# ────────────────────────────────────────────────────────────────────────────────
# 7. REST API Endpoints
# ────────────────────────────────────────────────────────────────────────────────

def test_rest_api_endpoints():
    """Verify FastAPI router configuration and endpoint availability."""
    from app.platform_verification.enterprise_performance_bottleneck.api.bottleneck_discovery_api import router

    assert router.prefix == "/api/v1/bottleneck-discovery"
    route_paths = [r.path for r in router.routes]
    prefix = "/api/v1/bottleneck-discovery"
    assert f"{prefix}/health" in route_paths
    assert f"{prefix}/phases" in route_paths
    assert f"{prefix}/run" in route_paths
    assert f"{prefix}/reports/{{phase_id}}" in route_paths
    assert f"{prefix}/certification" in route_paths
    assert f"{prefix}/manifest" in route_paths
