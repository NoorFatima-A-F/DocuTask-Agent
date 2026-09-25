"""
DocuTask Enterprise Verification Metrics, Evaluation & Scoring Framework Package.
"""
from app.platform_verification.evaluation_engine.domain.models import (
    MetricCategory,
    CertificationBand,
    QualityGateStatus,
    ComparisonTrend,
    RegressionCategory,
    Severity,
    MetricDefinition,
    MetricMetadata,
    MetricExplanation,
    ConfidenceInterval,
    StatisticalSummary,
    MetricResult,
    BenchmarkRecord,
    DimensionScore,
    OverallScore,
    QualityGateRule,
    QualityGateDecision,
    AIQualityAssessment,
    EvaluationRecommendation,
    EvaluationReport,
    TrendReport,
    TrendPoint,
    ABComparisonResult,
    RegressionAlert,
    SampleSizeValidationResult,
    MetricStoreRecord,
    MetricDashboardView,
    BenchmarkDashboardView,
    AiQualityDashboardView,
)
from app.platform_verification.evaluation_engine.core.metric_registry import MetricRegistry
from app.platform_verification.evaluation_engine.core.statistical_engine import StatisticalEngine
from app.platform_verification.evaluation_engine.core.scoring_engine import ScoringEngine
from app.platform_verification.evaluation_engine.core.benchmark_engine import BenchmarkEngine
from app.platform_verification.evaluation_engine.core.quality_gate import QualityGateEngine
from app.platform_verification.evaluation_engine.core.reporting_engine import ReportingEngine
from app.platform_verification.evaluation_engine.core.ai_evaluators import IndependentAiEvaluator
from app.platform_verification.evaluation_engine.core.pipeline import EvaluationPipeline
from app.platform_verification.evaluation_engine.core.ab_testing import ABTestingEngine
from app.platform_verification.evaluation_engine.core.regression_detector import RegressionDetector
from app.platform_verification.evaluation_engine.core.sample_size_validator import SampleSizeValidator
from app.platform_verification.evaluation_engine.core.metric_store import MetricStore
from app.platform_verification.evaluation_engine.core.dashboard_engine import MetricsDashboardEngine
from app.platform_verification.evaluation_engine.api.metrics_api import MetricsAPI
from app.platform_verification.evaluation_engine.runtime.evaluation_platform_runtime import EvaluationPlatformRuntime

__all__ = [
    "MetricCategory",
    "CertificationBand",
    "QualityGateStatus",
    "ComparisonTrend",
    "RegressionCategory",
    "Severity",
    "MetricDefinition",
    "MetricMetadata",
    "MetricExplanation",
    "ConfidenceInterval",
    "StatisticalSummary",
    "MetricResult",
    "BenchmarkRecord",
    "DimensionScore",
    "OverallScore",
    "QualityGateRule",
    "QualityGateDecision",
    "AIQualityAssessment",
    "EvaluationRecommendation",
    "EvaluationReport",
    "TrendReport",
    "TrendPoint",
    "ABComparisonResult",
    "RegressionAlert",
    "SampleSizeValidationResult",
    "MetricStoreRecord",
    "MetricDashboardView",
    "BenchmarkDashboardView",
    "AiQualityDashboardView",
    "MetricRegistry",
    "StatisticalEngine",
    "ScoringEngine",
    "BenchmarkEngine",
    "QualityGateEngine",
    "ReportingEngine",
    "IndependentAiEvaluator",
    "EvaluationPipeline",
    "ABTestingEngine",
    "RegressionDetector",
    "SampleSizeValidator",
    "MetricStore",
    "MetricsDashboardEngine",
    "MetricsAPI",
    "EvaluationPlatformRuntime",
]
