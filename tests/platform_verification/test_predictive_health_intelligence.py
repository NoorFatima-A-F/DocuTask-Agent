"""Comprehensive Unit and Integration Test Suite for Phase 3H.3.4: Predictive Health Intelligence.

Tests cover all 15 core architectural components, domain models, algorithms, simulations,
scoring logic, and evidence generation.
"""

from __future__ import annotations

import json
from pathlib import Path


from app.platform_verification.predictive_health_intelligence.anomaly.health_anomaly_detector import (
    HealthAnomalyDetector,
)
from app.platform_verification.predictive_health_intelligence.baseline.health_baseline_manager import (
    HealthBaselineManager,
)
from app.platform_verification.predictive_health_intelligence.domain.models import (
    AccuracyReport,
    AIWorkflowHealthReport,
    AnomalyReport,
    BaselineReport,
    EarlyWarningCategory,
    EarlyWarningReport,
    PredictiveHealthScorecard,
    PredictiveHealthTier,
    RecommendationReport,
    RiskLevel,
    RiskPredictionReport,
    TelemetryItem,
    TelemetryReport,
)
from app.platform_verification.predictive_health_intelligence.early_warning.early_warning_system import (
    EarlyWarningSystem,
)
from app.platform_verification.predictive_health_intelligence.exporter.predictive_evidence_exporter import (
    PredictiveEvidenceExporter,
)
from app.platform_verification.predictive_health_intelligence.observability.predictive_metrics_exporter import (
    PredictiveMetricsExporter,
)
from app.platform_verification.predictive_health_intelligence.prediction.ai_workflow_predictor import (
    AIWorkflowHealthPredictor,
)
from app.platform_verification.predictive_health_intelligence.prediction.resource_exhaustion_predictor import (
    ResourceExhaustionPredictor,
)
from app.platform_verification.predictive_health_intelligence.recommendation.automated_action_verifier import (
    AutomatedActionVerifier,
)
from app.platform_verification.predictive_health_intelligence.recommendation.preventive_action_recommender import (
    PreventiveActionRecommender,
)
from app.platform_verification.predictive_health_intelligence.risk.health_risk_engine import (
    HealthRiskEngine,
)
from app.platform_verification.predictive_health_intelligence.runtime.predictive_health_runtime import (
    PredictiveHealthRuntime,
)
from app.platform_verification.predictive_health_intelligence.simulation.predictive_simulation_runner import (
    PredictiveSimulationRunner,
)
from app.platform_verification.predictive_health_intelligence.storage.timeseries_health_store import (
    TimeSeriesHealthStore,
)
from app.platform_verification.predictive_health_intelligence.telemetry.health_telemetry_collector import (
    HealthTelemetryCollector,
)
from app.platform_verification.predictive_health_intelligence.validation.false_positive_validator import (
    FalsePositiveValidator,
)


# ============================================================================
# Part 1: Telemetry Collector Tests
# ============================================================================
def test_telemetry_collector_ingest_and_report() -> None:
    collector = HealthTelemetryCollector()
    item = collector.record_metric("host.cpu_utilization", "worker", 45.0, "%", {"env": "prod"})
    assert item.metric == "host.cpu_utilization"
    assert item.value == 45.0
    assert item.service == "worker"

    report: TelemetryReport = collector.collect_comprehensive_telemetry()
    assert report.total_metrics_collected >= 15
    assert len(report.categories_covered) == 5
    assert report.schema_compliant is True
    assert report.passed is True


# ============================================================================
# Part 2: Time-series Health Store Tests
# ============================================================================
def test_timeseries_store_retention_and_stats() -> None:
    store = TimeSeriesHealthStore(max_points_per_metric=100)

    for i in range(10):
        item = TelemetryItem(
            metric="cpu",
            service="worker",
            value=10.0 + (i * 2.0),
            unit="%",
            timestamp="2026-09-15T00:00:00Z",
        )
        store.ingest_point(item)

    points = store.get_points("worker", "cpu")
    assert len(points) == 10
    stats = store.compute_statistics("worker", "cpu")
    assert stats["count"] == 10.0
    assert stats["latest"] == 28.0
    assert stats["slope"] > 0.0


# ============================================================================
# Part 3: Baseline Manager Tests
# ============================================================================
def test_baseline_manager_load_and_report() -> None:
    manager = HealthBaselineManager()
    report: BaselineReport = manager.get_baseline_report()
    assert report.total_profiles >= 6
    assert report.baseline_loaded is True
    assert report.passed is True
    service_names = {p.service for p in report.profiles}
    assert "worker" in service_names
    assert "database" in service_names
    assert "ai_provider" in service_names


# ============================================================================
# Part 4: Anomaly Detector Tests
# ============================================================================
def test_anomaly_detector_algorithms() -> None:
    detector = HealthAnomalyDetector()
    report: AnomalyReport = detector.detect_anomalies()
    assert report.total_anomalies_detected >= 3
    assert report.statistical_detection_active is True
    assert report.trend_detection_active is True
    assert report.passed is True
    methods = {a.detection_method for a in report.anomalies}
    assert "statistical_zscore" in methods
    assert "trend_slope" in methods
    assert "threshold" in methods


# ============================================================================
# Part 5: Risk Engine Tests
# ============================================================================
def test_health_risk_engine_evaluation() -> None:
    engine = HealthRiskEngine()
    report: RiskPredictionReport = engine.compute_risk_predictions()
    assert len(report.predictions) >= 4
    assert report.highest_probability >= 0.70
    assert report.overall_system_risk in (RiskLevel.HIGH, RiskLevel.MEDIUM)
    assert report.passed is True


# ============================================================================
# Part 6: Resource Exhaustion Predictor Tests
# ============================================================================
def test_resource_exhaustion_predictor() -> None:
    predictor = ResourceExhaustionPredictor()
    estimates = predictor.predict_exhaustion()
    assert len(estimates) >= 4
    resource_types = {e.resource_type for e in estimates}
    assert "memory_rss" in resource_types
    assert "queue_capacity" in resource_types
    assert "database_connections" in resource_types
    assert any(e.imminent_exhaustion for e in estimates)


# ============================================================================
# Part 7: AI Workflow Predictor Tests
# ============================================================================
def test_ai_workflow_predictor() -> None:
    predictor = AIWorkflowHealthPredictor()
    report: AIWorkflowHealthReport = predictor.predict_ai_health()
    assert report.model_latency_ms > 0.0
    assert report.confidence >= 0.85
    assert report.passed is True
    assert "gemini-2.0-flash" in report.details["model"]


# ============================================================================
# Part 8: Early Warning System Tests
# ============================================================================
def test_early_warning_system_generation() -> None:
    system = EarlyWarningSystem()
    report: EarlyWarningReport = system.generate_early_warnings()
    assert report.total_warnings == 5
    assert report.passed is True
    categories = {w.category for w in report.warnings}
    assert categories == set(EarlyWarningCategory)
    assert all(w.predicted_impact_time for w in report.warnings)


# ============================================================================
# Part 9 & 10: Preventive Action Recommender & Verifier Tests
# ============================================================================
def test_preventive_action_recommender_and_verifier() -> None:
    recommender = PreventiveActionRecommender()
    verifier = AutomatedActionVerifier()

    report: RecommendationReport = recommender.generate_recommendations()
    assert report.total_recommendations >= 4
    assert report.automation_pipeline_verified is True
    assert report.passed is True

    for rec in report.recommendations:
        result = verifier.verify_action_pipeline(rec)
        assert result["closed_loop_safe"] is True
        assert result["detection_verified"] is True
        assert result["policy_approved"] is True
        assert result["execution_verified"] is True
        assert result["post_action_verified"] is True


# ============================================================================
# Part 11: False Positive Validator Tests
# ============================================================================
def test_false_positive_validator_benchmarking() -> None:
    validator = FalsePositiveValidator()
    report: AccuracyReport = validator.evaluate_accuracy()
    assert report.metrics.precision >= 0.95
    assert report.metrics.recall >= 0.95
    assert report.metrics.false_positive_rate <= 0.05
    assert report.metrics.detection_delay_seconds <= 15.0
    assert report.benchmarks_met is True
    assert report.passed is True


# ============================================================================
# Part 12: Simulation Runner Tests
# ============================================================================
def test_predictive_simulation_runner() -> None:
    runner = PredictiveSimulationRunner()
    results = runner.run_simulations()
    assert results["total_scenarios"] == 3
    assert results["all_scenarios_passed"] is True
    assert results["passed"] is True


# ============================================================================
# Part 13: Observability Metrics Exporter Tests
# ============================================================================
def test_predictive_metrics_exporter_prometheus() -> None:
    exporter = PredictiveMetricsExporter()
    payload = exporter.generate_prometheus_payload()
    assert "health_risk_score" in payload
    assert "prediction_accuracy" in payload
    assert "anomaly_count" in payload
    assert "early_warning_count" in payload
    assert "failure_probability" in payload

    dashboard = exporter.get_dashboard_summary()
    assert dashboard["prometheus_compatible"] is True
    assert dashboard["grafana_dashboard_available"] is True


# ============================================================================
# Part 14: Evidence Exporter Tests
# ============================================================================
def test_evidence_exporter_all_manifests(tmp_path: Path) -> None:
    exporter = PredictiveEvidenceExporter(output_dir=tmp_path)
    runtime = PredictiveHealthRuntime(export_dir=tmp_path)
    results = runtime.run_full_verification()

    manifests = exporter.export_all(
        telemetry_report=results["telemetry_report"],
        baseline_report=results["baseline_report"],
        anomaly_report=results["anomaly_report"],
        risk_report=results["risk_report"],
        early_warning_report=results["early_warning_report"],
        recommendation_report=results["recommendation_report"],
        accuracy_report=results["accuracy_report"],
        scorecard=results["scorecard"],
    )

    assert len(manifests) == 8
    for name, path in manifests.items():
        assert path.exists()
        assert path.stat().st_size > 0
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert isinstance(data, dict)


# ============================================================================
# Part 15: Scoring Engine & Scorecard Certification Tests
# ============================================================================
def test_predictive_health_scorecard_certification() -> None:
    runtime = PredictiveHealthRuntime()
    results = runtime.run_full_verification()
    scorecard: PredictiveHealthScorecard = results["scorecard"]

    assert scorecard.overall_score >= 95.00
    assert scorecard.certification_tier == PredictiveHealthTier.ENTERPRISE_READY
    assert scorecard.certification_verdict == "CERTIFIED"
    assert scorecard.passed is True

    # Check 6 dimensions
    assert scorecard.telemetry_quality_score == 100.0
    assert scorecard.anomaly_detection_score == 100.0
    assert scorecard.prediction_accuracy_score == 100.0
    assert scorecard.early_warning_score == 100.0
    assert scorecard.preventive_actions_score == 100.0
    assert scorecard.observability_score == 100.0
