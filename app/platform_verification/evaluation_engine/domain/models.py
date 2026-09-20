"""
Domain models for Enterprise Verification Metrics, Evaluation & Scoring Framework (PART 5).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union


class MetricCategory(str, Enum):
    FUNCTIONAL_CORRECTNESS = "functional_correctness"
    AI_QUALITY = "ai_quality"
    PERFORMANCE = "performance"
    RELIABILITY = "reliability"
    SECURITY = "security"
    ROBUSTNESS = "robustness"


class CertificationBand(str, Enum):
    ENTERPRISE_CERTIFIED = "Enterprise Certified"  # 95-100
    PRODUCTION_READY = "Production Ready"          # 90-94
    CONDITIONALLY_READY = "Conditionally Ready"    # 80-89
    DEVELOPMENT_QUALITY = "Development Quality"    # 70-79
    NOT_READY = "Not Ready"                        # Below 70


class QualityGateStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    CONDITIONAL = "CONDITIONAL"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class ComparisonTrend(str, Enum):
    IMPROVED = "IMPROVED"
    REGRESSED = "REGRESSED"
    STABLE = "STABLE"


class RegressionCategory(str, Enum):
    QUALITY = "QUALITY"
    PERFORMANCE = "PERFORMANCE"
    COST = "COST"


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass(frozen=True)
class MetricDefinition:
    """Standardized metric definition entity."""
    id: str
    name: str
    category: MetricCategory
    description: str
    formula: str
    source: str
    calculation_method: str
    threshold: float
    weight: float
    version: str = "1.0.0"
    owner: str = "platform_verification_team"
    is_higher_better: bool = True
    unit: str = "percentage"
    min_value: float = 0.0
    max_value: float = 100.0


@dataclass(frozen=True)
class MetricMetadata:
    """Metric metadata schema for export and serialization."""
    id: str
    name: str
    category: str
    description: str
    formula: str
    source: str
    version: str
    threshold: float
    weight: float
    owner: str


@dataclass(frozen=True)
class MetricExplanation:
    """Metric explainability record."""
    name: str
    formula: str
    purpose: str
    interpretation: str
    limitations: str


@dataclass(frozen=True)
class ConfidenceInterval:
    """Statistical confidence interval."""
    metric_name: str
    value: float
    confidence_level: float  # e.g., 0.95
    lower_bound: float
    upper_bound: float
    sample_size: int
    method: str = "wilson_score"

    @property
    def interval_str(self) -> str:
        return f"{self.lower_bound:.2f}% - {self.upper_bound:.2f}% (conf: {int(self.confidence_level * 100)}%)"


@dataclass(frozen=True)
class StatisticalSummary:
    """Statistical evaluation summary for a metric dataset."""
    mean: float
    median: float
    variance: float
    std_dev: float
    min_value: float
    max_value: float
    p50: float
    p90: float
    p95: float
    p99: float
    sample_size: int
    confidence_interval: Optional[ConfidenceInterval] = None


@dataclass
class MetricResult:
    """Calculated metric evaluation result."""
    metric_id: str
    metric_name: str
    category: MetricCategory
    raw_value: float
    normalized_score: float  # 0 to 100
    unit: str
    passed: bool
    threshold: float
    confidence_interval: Optional[ConfidenceInterval] = None
    statistical_summary: Optional[StatisticalSummary] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    calculated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ABComparisonResult:
    """A/B test comparison result between two variants (models, prompts, configs)."""
    variant_a: str
    variant_b: str
    metric_name: str
    value_a: float
    value_b: float
    delta_absolute: float
    delta_percentage: float
    t_statistic: float
    p_value: float
    is_significant: bool
    winner: str
    analysis: str


@dataclass
class RegressionAlert:
    """Automated regression notification when a threshold is breached."""
    alert_id: str
    metric_id: str
    metric_name: str
    category: RegressionCategory
    baseline_value: float
    candidate_value: float
    delta_percentage: float
    threshold_percentage: float
    severity: Severity
    message: str
    detected_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class SampleSizeValidationResult:
    """Statistical power and minimum sample size validation result."""
    sample_size: int
    is_sufficient: bool
    minimum_required: int
    confidence_level: float
    margin_of_error_pct: float
    statistical_power: float
    recommendation: str


@dataclass
class MetricStoreRecord:
    """Persistent storage entry for a metric calculation result."""
    record_id: str
    metric_id: str
    execution_id: str
    value: float
    normalized_score: float
    unit: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkRecord:
    """Benchmark comparison against baseline or prior version."""
    system_version: str
    baseline: str
    dataset: str
    metric: str
    result: float
    baseline_result: float
    difference: float
    percentage_change: float
    trend: ComparisonTrend
    analysis: str
    compared_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class DimensionScore:
    """Weighted score for a specific metric dimension."""
    dimension: MetricCategory
    score: float
    weight: float
    weighted_score: float
    metrics: List[MetricResult] = field(default_factory=list)
    passed: bool = True


@dataclass
class OverallScore:
    """Standardized composite quality score and certification classification."""
    overall_score: float
    certification_band: CertificationBand
    dimensions: Dict[MetricCategory, DimensionScore] = field(default_factory=dict)
    total_metrics: int = 0
    passed_metrics: int = 0
    certified_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(frozen=True)
class QualityGateRule:
    """Operational quality gate threshold rule."""
    rule_id: str
    metric_id: str
    condition: str  # "gte", "lte", "gt", "lt", "eq"
    target_value: float
    severity: Severity = Severity.CRITICAL
    required: bool = True
    description: str = ""


@dataclass
class QualityGateDecision:
    """Outcome of quality gate evaluation."""
    status: QualityGateStatus
    passed_rules: List[str] = field(default_factory=list)
    failed_rules: List[str] = field(default_factory=list)
    total_rules: int = 0
    blocking_failures: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    evaluated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class AIQualityAssessment:
    """Detailed multi-facet AI evaluation results."""
    grounding_score: float
    faithfulness_score: float
    hallucination_rate: float
    completeness_score: float
    consistency_score: float
    context_utilization_score: float
    citation_accuracy: float
    reasoning_quality_score: float
    safety_score: float
    detailed_critique: str = ""


@dataclass
class EvaluationRecommendation:
    """Actionable improvement recommendation."""
    recommendation_id: str
    category: MetricCategory
    severity: Severity
    message: str
    suggested_action: str


@dataclass
class EvaluationReport:
    """Complete enterprise evaluation report."""
    report_id: str
    execution_id: str
    system_version: str
    timestamp: str
    overall_score: OverallScore
    quality_gate_decision: QualityGateDecision
    metric_results: List[MetricResult] = field(default_factory=list)
    benchmark_comparisons: List[BenchmarkRecord] = field(default_factory=list)
    recommendations: List[EvaluationRecommendation] = field(default_factory=list)
    evidence_links: List[str] = field(default_factory=list)


@dataclass
class TrendPoint:
    timestamp: str
    version: str
    value: float


@dataclass
class TrendReport:
    """Historical trend report for a specific metric."""
    metric_id: str
    metric_name: str
    points: List[TrendPoint] = field(default_factory=list)
    slope: float = 0.0
    trend: ComparisonTrend = ComparisonTrend.STABLE
    variance: float = 0.0


@dataclass
class MetricDashboardView:
    title: str
    overall_score: float
    certification_band: str
    metric_cards: List[Dict[str, Any]]
    recent_alerts: List[Dict[str, Any]]


@dataclass
class BenchmarkDashboardView:
    title: str
    candidate_version: str
    baseline_version: str
    comparison_cards: List[Dict[str, Any]]
    regression_count: int
    improvement_count: int


@dataclass
class AiQualityDashboardView:
    title: str
    grounding_score: float
    faithfulness_score: float
    hallucination_rate: float
    completeness_score: float
    consistency_score: float
    safety_score: float
    radar_chart_data: Dict[str, float]
