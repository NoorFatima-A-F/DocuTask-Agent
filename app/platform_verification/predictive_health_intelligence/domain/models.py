"""
Domain Models for Predictive Health Intelligence & Early Failure Detection (Part 3H.3.4).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List


class RiskLevel(str, Enum):
    LOW = "LOW"             # 0 - 30%
    MEDIUM = "MEDIUM"       # 31 - 70%
    HIGH = "HIGH"           # 71 - 90%
    CRITICAL = "CRITICAL"   # 91 - 100%


class AnomalySeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class EarlyWarningCategory(str, Enum):
    RESOURCE_RISK = "RESOURCE_RISK"
    DEPENDENCY_RISK = "DEPENDENCY_RISK"
    PERFORMANCE_RISK = "PERFORMANCE_RISK"
    AI_FAILURE_RISK = "AI_FAILURE_RISK"
    CAPACITY_RISK = "CAPACITY_RISK"


class PreventiveActionType(str, Enum):
    SCALE_WORKERS = "SCALE_WORKERS"
    EXPAND_DB_POOL = "EXPAND_DB_POOL"
    ENABLE_FALLBACK_PROVIDER = "ENABLE_FALLBACK_PROVIDER"
    THROTTLE_INGESTION = "THROTTLE_INGESTION"
    PAUSE_NON_CRITICAL_JOBS = "PAUSE_NON_CRITICAL_JOBS"
    RESTART_LEAKING_WORKER = "RESTART_LEAKING_WORKER"


class PredictiveHealthTier(str, Enum):
    FAILED = "Failed"                                         # < 80
    NEEDS_IMPROVEMENT = "Improvement Required"               # 80 - 89
    PRODUCTION_READY = "Production Ready"                     # 90 - 94
    ENTERPRISE_READY = "Predictive Reliability Ready"          # 95 - 100


@dataclass
class TelemetryItem:
    metric: str
    service: str
    value: float
    unit: str
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TelemetryReport:
    total_metrics_collected: int
    categories_covered: List[str]
    schema_compliant: bool
    passed: bool
    sample_telemetry: List[TelemetryItem] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BaselineProfile:
    service: str
    metric: str
    nominal_min: float
    nominal_max: float
    warning_threshold: float
    critical_threshold: float


@dataclass
class BaselineReport:
    total_profiles: int
    profiles: List[BaselineProfile]
    baseline_loaded: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnomalyItem:
    metric: str
    service: str
    observed_value: float
    expected_range: str
    severity: AnomalySeverity
    confidence: float
    detection_method: str  # threshold, statistical_zscore, trend_slope, pattern
    timestamp: str


@dataclass
class AnomalyReport:
    total_anomalies_detected: int
    anomalies: List[AnomalyItem]
    statistical_detection_active: bool
    trend_detection_active: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RiskPredictionItem:
    service: str
    failure_probability: float  # 0.0 - 1.0
    risk_level: RiskLevel
    estimated_time_horizon: str  # e.g. "within 30 minutes"
    primary_risk_driver: str
    timestamp: str


@dataclass
class RiskPredictionReport:
    overall_system_risk: RiskLevel
    highest_probability: float
    predictions: List[RiskPredictionItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResourceExhaustionEstimate:
    resource_type: str  # memory, queue, storage, db_connections
    current_utilization_pct: float
    growth_rate_per_minute: float
    estimated_time_to_exhaustion_minutes: float
    imminent_exhaustion: bool
    confidence: float


@dataclass
class AIWorkflowHealthReport:
    model_latency_ms: float
    error_rate_pct: float
    token_spike_detected: bool
    extraction_quality_score: float
    degradation_predicted: bool
    confidence: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EarlyWarningAlert:
    alert_id: str
    category: EarlyWarningCategory
    severity: str
    service: str
    message: str
    predicted_impact_time: str
    suggested_action: str
    timestamp: str


@dataclass
class EarlyWarningReport:
    total_warnings: int
    warnings: List[EarlyWarningAlert]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PreventiveRecommendation:
    recommendation_id: str
    action_type: PreventiveActionType
    target_service: str
    rationale: str
    expected_risk_reduction_pct: float
    automated_executable: bool
    requires_approval: bool


@dataclass
class RecommendationReport:
    total_recommendations: int
    recommendations: List[PreventiveRecommendation]
    automation_pipeline_verified: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AccuracyMetrics:
    precision: float
    recall: float
    false_positive_rate: float
    detection_delay_seconds: float
    passed: bool


@dataclass
class AccuracyReport:
    metrics: AccuracyMetrics
    benchmarks_met: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PredictiveHealthScorecard:
    telemetry_quality_score: float       # Weight 20%
    anomaly_detection_score: float       # Weight 20%
    prediction_accuracy_score: float     # Weight 20%
    early_warning_score: float           # Weight 15%
    preventive_actions_score: float      # Weight 15%
    observability_score: float           # Weight 10%
    overall_score: float                 # Composite 0 - 100
    certification_tier: PredictiveHealthTier
    certification_verdict: str           # CERTIFIED / REJECTED
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)
