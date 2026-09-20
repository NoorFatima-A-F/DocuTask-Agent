"""
Comprehensive test suite for Enterprise Verification Metrics, Evaluation & Scoring Framework (PART 5).
"""
import pytest
from app.platform_verification.evaluation_engine import (
    MetricCategory,
    CertificationBand,
    QualityGateStatus,
    ComparisonTrend,
    RegressionCategory,
    Severity,
    MetricDefinition,
    MetricRegistry,
    StatisticalEngine,
    ScoringEngine,
    BenchmarkEngine,
    QualityGateEngine,
    QualityGateRule,
    IndependentAiEvaluator,
    ABTestingEngine,
    RegressionDetector,
    SampleSizeValidator,
    EvaluationPipeline,
    EvaluationPlatformRuntime,
    TrendPoint,
)


def test_metric_registry_and_explainability():
    registry = MetricRegistry()
    metrics = registry.list_all()
    assert len(metrics) >= 15

    # Check accuracy definition
    acc = registry.get("func_accuracy")
    assert acc.name == "Accuracy"
    assert acc.category == MetricCategory.FUNCTIONAL_CORRECTNESS
    assert acc.threshold == 95.0

    # Check explanation record
    exp = registry.get_explanation("func_accuracy")
    assert exp.name == "Accuracy"
    assert "Predictions" in exp.formula


def test_ab_testing_and_statistical_significance():
    runtime = EvaluationPlatformRuntime()

    model_a_acc = [91.0, 92.0, 91.5, 90.5, 92.0, 91.2, 91.8]
    model_b_acc = [96.0, 97.0, 96.5, 95.5, 97.2, 96.8, 96.4]

    ab_res = runtime.compare_ab("Gemini-1.5-Flash", model_a_acc, "Gemini-1.5-Pro", model_b_acc, "Extraction Accuracy")
    assert ab_res.is_significant is True
    assert ab_res.p_value < 0.01
    assert ab_res.winner == "Gemini-1.5-Pro"
    assert ab_res.delta_absolute > 0


def test_automated_regression_detection():
    runtime = EvaluationPlatformRuntime()

    candidate_results = [
        runtime.pipeline.agents[0].calculator.calculate({"correct_predictions": 85, "total_predictions": 100}, runtime.registry.get("func_accuracy")),
        runtime.pipeline.agents[1].calculator.calculate({"p95_latency_ms": 900.0}, runtime.registry.get("perf_p95_latency")),
    ]
    baseline_results = [
        runtime.pipeline.agents[0].calculator.calculate({"correct_predictions": 98, "total_predictions": 100}, runtime.registry.get("func_accuracy")),
        runtime.pipeline.agents[1].calculator.calculate({"p95_latency_ms": 400.0}, runtime.registry.get("perf_p95_latency")),
    ]

    alerts = runtime.detect_regressions(candidate_results, baseline_results)
    assert len(alerts) >= 2
    categories = [a.category for a in alerts]
    assert RegressionCategory.QUALITY in categories
    assert RegressionCategory.PERFORMANCE in categories


def test_sample_size_statistical_power_validation():
    runtime = EvaluationPlatformRuntime()

    # Small sample (insufficient)
    small_check = runtime.validate_sample_power(sample_size=20, confidence=0.95, margin_of_error=0.05)
    assert small_check.is_sufficient is False
    assert small_check.minimum_required >= 300

    # Large sample (sufficient)
    large_check = runtime.validate_sample_power(sample_size=1000, confidence=0.95, margin_of_error=0.05)
    assert large_check.is_sufficient is True
    assert large_check.statistical_power == 1.0


def test_scoring_engine_and_certification_bands():
    runtime = EvaluationPlatformRuntime()

    raw_data = {
        "true_positives": 98,
        "false_positives": 2,
        "false_negatives": 2,
        "true_negatives": 98,
        "total_predictions": 200,
        "correct_predictions": 196,
        "exact_matches": 190,
        "schema_valid_count": 200,
        "grounded_claims": 98,
        "faithful_facts": 98,
        "total_claims": 100,
        "hallucinated_claims": 2,
        "latencies_ms": [150.0, 180.0, 200.0, 190.0, 210.0],
        "throughput_rps": 150.0,
        "cost_per_doc_usd": 0.01,
        "total_runs": 1000,
        "successful_runs": 998,
        "failed_runs": 2,
        "recovered_count": 100,
        "total_faults_injected": 100,
        "critical_vulns": 0,
        "blocked_attacks": 100,
        "total_attacks": 100,
        "pii_leaks": 0,
        "evaluated_samples": 500,
    }

    report = runtime.evaluate_execution(raw_data, system_version="v2.5.0")
    assert report.overall_score.overall_score >= 90.0
    assert report.overall_score.certification_band in [
        CertificationBand.ENTERPRISE_CERTIFIED,
        CertificationBand.PRODUCTION_READY,
    ]
    assert report.quality_gate_decision.status == QualityGateStatus.PASSED

    # Dashboard Generation
    dashboard = runtime.generate_dashboards(report)
    assert dashboard.overall_score >= 90.0
    assert len(dashboard.metric_cards) >= 10


def test_metrics_api_endpoints():
    runtime = EvaluationPlatformRuntime()

    # GET metric
    m = runtime.api.get_metric("func_accuracy")
    assert m is not None
    assert m["name"] == "Accuracy"

    # POST compare
    cmp_res = runtime.api.post_compare("A", [90, 91, 92], "B", [95, 96, 97], "Accuracy")
    assert cmp_res["winner"] == "B"
    assert cmp_res["delta_abs"] > 0
