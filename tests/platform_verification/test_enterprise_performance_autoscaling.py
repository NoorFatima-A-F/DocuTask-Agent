"""Phase 3J.8: Enterprise Autoscaling & Elastic Capacity Verification — Test Suite.

Tests:
- Domain model instantiation
- Verifier registry (14 verifiers)
- Individual verifier execution (3J.8.1–3J.8.14)
- 6-category quality scorer
- SHA-256 exporter with manifest
- Runtime orchestrator
- REST API endpoints
"""

import json
import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from app.platform_verification.enterprise_performance_autoscaling.domain.models import (
    AIScalingReport,
    APIScalingReport,
    AutoscalingArchitectureReport,
    AutoscalingVerificationManifest,
    BaseVerificationReport,
    CategoryScore,
    CheckResult,
    CloudScalingReport,
    CostScalingReport,
    DatabaseScalingImpactReport,
    EnterpriseAutoscalingCertificationReport,
    EnterprisePerformanceTier,
    K8sScalingReadinessReport,
    QueueAutoscalingReport,
    ScaleDownSafetyReport,
    ScaleUpValidationReport,
    ScalingFailureReport,
    ScalingMetricsReport,
    ScalingPolicyReport,
    VerificationStatus,
    WorkerScalingReport,
)

PerformanceCertificationReport = EnterpriseAutoscalingCertificationReport
PerformanceVerificationStatus = VerificationStatus
CertificationTier = EnterprisePerformanceTier

from app.platform_verification.enterprise_performance_autoscaling.verifiers import (
    get_all_verifiers,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.architecture_verifier import (
    AutoscalingArchitectureVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.scaling_metrics_verifier import (
    ScalingMetricsVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.worker_scaling_verifier import (
    WorkerScalingVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.queue_autoscaling_verifier import (
    QueueAutoscalingVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.api_scaling_verifier import (
    APIScalingVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.scaling_policy_verifier import (
    ScalingPolicyVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.scale_up_verifier import (
    ScaleUpVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.scale_down_safety_verifier import (
    ScaleDownSafetyVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.database_scaling_limit_verifier import (
    DatabaseScalingImpactVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.ai_scaling_verifier import (
    AIScalingVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.kubernetes_scaling_readiness_verifier import (
    K8sScalingReadinessVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.cloud_scaling_compatibility_verifier import (
    CloudScalingCompatibilityVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.cost_scaling_verifier import (
    CostScalingVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.scaling_failure_verifier import (
    ScalingFailureSimulationVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.scoring.autoscaling_scorer import (
    AutoscalingScorer,
)
from app.platform_verification.enterprise_performance_autoscaling.exporter.autoscaling_exporter import (
    AutoscalingExporter,
)
from app.platform_verification.enterprise_performance_autoscaling.runtime.autoscaling_runtime import (
    AutoscalingRuntime,
)


# ────────────────────────────────────────────────────────────────────────────────
# 1. Domain Model Instantiation
# ────────────────────────────────────────────────────────────────────────────────

def test_domain_models_instantiation():
    """Verify all 3J.8 domain models can be instantiated with defaults."""
    report_classes = [
        BaseVerificationReport,
        AutoscalingArchitectureReport,
        ScalingMetricsReport,
        WorkerScalingReport,
        QueueAutoscalingReport,
        APIScalingReport,
        ScalingPolicyReport,
        ScaleUpValidationReport,
        ScaleDownSafetyReport,
        DatabaseScalingImpactReport,
        AIScalingReport,
        K8sScalingReadinessReport,
        CloudScalingReport,
        CostScalingReport,
        ScalingFailureReport,
        EnterpriseAutoscalingCertificationReport,
        AutoscalingVerificationManifest,
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
    """Verify exactly 14 verifiers are registered in proper order."""
    verifiers = get_all_verifiers()
    assert len(verifiers) == 14

    expected_phases = [
        "3J.8.1", "3J.8.2", "3J.8.3", "3J.8.4", "3J.8.5",
        "3J.8.6", "3J.8.7", "3J.8.8", "3J.8.9", "3J.8.10",
        "3J.8.11", "3J.8.12", "3J.8.13", "3J.8.14",
    ]
    for v, expected in zip(verifiers, expected_phases):
        assert expected in v.verifier_id, f"Expected {expected} in {v.verifier_id}"
        assert v.phase_id == expected


# ────────────────────────────────────────────────────────────────────────────────
# 3. Individual Verifier Tests (3J.8.1–3J.8.14)
# ────────────────────────────────────────────────────────────────────────────────

def test_3j_8_1_architecture_verifier():
    verifier = AutoscalingArchitectureVerifier()
    report = verifier.verify()
    assert isinstance(report, AutoscalingArchitectureReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.scalable_components) >= 4
    assert report.scaling_strategy == "horizontal"
    assert report.metrics_collector_ready
    assert report.scaling_controller_ready
    assert report.health_validator_ready
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_8_2_scaling_metrics_verifier():
    verifier = ScalingMetricsVerifier()
    report = verifier.verify()
    assert isinstance(report, ScalingMetricsReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.worker_metrics) >= 4
    assert len(report.api_metrics) >= 3
    assert len(report.database_metrics) >= 3
    assert report.all_metrics_configured
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_8_3_worker_scaling_verifier():
    verifier = WorkerScalingVerifier()
    report = verifier.verify()
    assert isinstance(report, WorkerScalingReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.scaling_stages) == 5
    assert report.initial_workers == 2
    assert report.final_workers == 10
    assert report.queue_recovery_verified
    assert report.duplicate_prevention_verified
    assert report.graceful_shutdown_verified
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_8_4_queue_autoscaling_verifier():
    verifier = QueueAutoscalingVerifier()
    report = verifier.verify()
    assert isinstance(report, QueueAutoscalingReport)
    assert report.status == VerificationStatus.PASSED
    assert report.spike_queue_depth == 10000
    assert report.queue_growth_detected
    assert report.workers_scaled_up
    assert report.queue_drained
    assert report.scale_up_delay_sec < 15.0
    assert report.recovery_time_sec < 300.0
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_8_5_api_scaling_verifier():
    verifier = APIScalingVerifier()
    report = verifier.verify()
    assert isinstance(report, APIScalingReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.scaling_stages) == 3
    assert report.stateless_verified
    assert report.session_handling_verified
    assert report.load_distribution_verified
    assert report.no_local_state_dependency
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_8_6_scaling_policy_verifier():
    verifier = ScalingPolicyVerifier()
    report = verifier.verify()
    assert isinstance(report, ScalingPolicyReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.scenarios) == 4
    assert all(s.correct for s in report.scenarios)
    assert report.false_scaling_prevented
    assert report.cooldown_period_sec == 300
    assert report.stabilization_window_sec == 120
    assert report.scaling_limits_enforced
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_8_7_scale_up_verifier():
    verifier = ScaleUpVerifier()
    report = verifier.verify()
    assert isinstance(report, ScaleUpValidationReport)
    assert report.status == VerificationStatus.PASSED
    assert report.demand_after_dpm == 5000.0
    assert report.reaction_time_sec < 20.0
    assert report.latency_recovered
    assert report.throughput_increased
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_8_8_scale_down_safety_verifier():
    verifier = ScaleDownSafetyVerifier()
    report = verifier.verify()
    assert isinstance(report, ScaleDownSafetyReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.stages) == 5
    assert report.peak_workers == 50
    assert report.final_workers == 5
    assert report.lost_documents == 0
    assert report.partial_results == 0
    assert report.duplicate_processing == 0
    assert report.graceful_drain_verified
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_8_9_database_scaling_limit_verifier():
    verifier = DatabaseScalingImpactVerifier()
    report = verifier.verify()
    assert isinstance(report, DatabaseScalingImpactReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.snapshots) == 5
    assert not report.database_collapse_detected
    assert report.connection_pool_sufficient
    assert report.max_safe_workers_for_db == 80
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_8_10_ai_scaling_verifier():
    verifier = AIScalingVerifier()
    report = verifier.verify()
    assert isinstance(report, AIScalingReport)
    assert report.status == VerificationStatus.PASSED
    assert report.workers_after == 100
    assert report.rate_limit_respected
    assert report.quota_respected
    assert report.latency_increase_pct < 15.0
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_8_11_kubernetes_scaling_readiness_verifier():
    verifier = K8sScalingReadinessVerifier()
    report = verifier.verify()
    assert isinstance(report, K8sScalingReadinessReport)
    assert report.status == VerificationStatus.PASSED
    assert report.hpa_compatible
    assert report.metrics_api_compatible
    assert report.custom_metrics_supported
    assert report.resource_requests_defined
    assert report.resource_limits_defined
    assert report.readiness_probes_configured
    assert report.deployment_manifests_valid
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_8_12_cloud_scaling_compatibility_verifier():
    verifier = CloudScalingCompatibilityVerifier()
    report = verifier.verify()
    assert isinstance(report, CloudScalingReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.platforms) == 3
    assert all(p.compatible for p in report.platforms)
    assert report.stateless_services_verified
    assert report.externalized_storage_verified
    assert report.externalized_state_verified
    assert report.container_portable
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_8_13_cost_scaling_verifier():
    verifier = CostScalingVerifier()
    report = verifier.verify()
    assert isinstance(report, CostScalingReport)
    assert report.status == VerificationStatus.PASSED
    assert report.cost_per_document_usd < 0.01
    assert report.cost_reduction_from_scaling_pct > 50.0
    assert not report.always_on_waste_detected
    assert len(report.checks) == 4
    assert all(c.passed for c in report.checks)


def test_3j_8_14_scaling_failure_verifier():
    verifier = ScalingFailureSimulationVerifier()
    report = verifier.verify()
    assert isinstance(report, ScalingFailureReport)
    assert report.status == VerificationStatus.PASSED
    assert len(report.failure_scenarios) == 4
    assert all(s.passed for s in report.failure_scenarios)
    assert report.controller_failure_handled
    assert report.worker_creation_failure_handled
    assert report.resource_limit_handled
    assert report.cloud_capacity_failure_handled
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

    scorer = AutoscalingScorer()
    cert = scorer.score_reports(reports)

    assert isinstance(cert, EnterpriseAutoscalingCertificationReport)
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

        scorer = AutoscalingScorer()
        cert = scorer.score_reports(reports)

        exporter = AutoscalingExporter()
        manifest = exporter.export_all(reports, cert, output_dir=tmpdir)

        assert isinstance(manifest, AutoscalingVerificationManifest)
        assert manifest.passed is True
        assert manifest.overall_score == 100.0
        assert len(manifest.file_hashes) > 14

        expected_files = [
            "autoscaling_architecture.json",
            "scaling_metrics.json",
            "worker_scaling.json",
            "queue_scaling.json",
            "api_scaling.json",
            "scaling_policy.json",
            "scale_up_report.json",
            "scale_down_report.json",
            "database_scaling_limit.json",
            "ai_scaling_report.json",
            "kubernetes_scaling_readiness.json",
            "cloud_scaling_compatibility.json",
            "cost_analysis.json",
            "failure_simulation.json",
            "certification_report.json",
        ]
        for fname in expected_files:
            assert os.path.exists(os.path.join(tmpdir, fname)), f"Missing file: {fname}"

        expected_aliases = [
            "autoscaling_architecture_report.json",
            "scaling_metrics_report.json",
            "worker_scaling_report.json",
            "queue_autoscaling_report.json",
            "api_scaling_report.json",
            "scaling_policy_report.json",
            "scale_up_validation_report.json",
            "scale_down_safety_report.json",
            "database_scaling_limit_report.json",
            "kubernetes_scaling_readiness_report.json",
            "cloud_scaling_compatibility_report.json",
            "scaling_cost_efficiency_report.json",
            "scaling_failure_report.json",
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
        runtime = AutoscalingRuntime()
        result = runtime.run_full_verification(output_dir=tmpdir)

        assert "reports" in result
        assert "certification" in result
        assert "manifest" in result
        assert result["passed"] is True
        assert result["overall_score"] == 100.0
        assert result["tier"] == "Enterprise Elastic Scaling Ready"
        assert len(result["reports"]) == 14

        cert = runtime.get_latest_certification()
        assert cert is not None
        assert cert.overall_score == 100.0


# ────────────────────────────────────────────────────────────────────────────────
# 7. REST API Endpoints
# ────────────────────────────────────────────────────────────────────────────────

def test_rest_api_endpoints():
    """Verify FastAPI router configuration and endpoint availability."""
    from app.platform_verification.enterprise_performance_autoscaling.api.autoscaling_api import router

    assert router.prefix == "/api/v1/autoscaling"
    route_paths = [r.path for r in router.routes]
    prefix = "/api/v1/autoscaling"
    assert f"{prefix}/health" in route_paths
    assert f"{prefix}/phases" in route_paths
    assert f"{prefix}/run" in route_paths
    assert f"{prefix}/reports/{{phase_id}}" in route_paths
    assert f"{prefix}/certification" in route_paths
    assert f"{prefix}/manifest" in route_paths
