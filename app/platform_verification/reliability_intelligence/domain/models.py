"""Domain Models for Phase 3H.3.7: Reliability Engineering Intelligence & Continuous Improvement."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ReliabilityMaturityTier(str, Enum):
    FAILED = "Failed"                                         # < 80
    NEEDS_IMPROVEMENT = "Improvement Required"               # 80 - 89
    ENTERPRISE_RELIABILITY_READY = "Enterprise Reliability Ready"  # 90 - 94
    RELIABILITY_ENGINEERING_MATURE = "Reliability Engineering Mature"  # 95 - 100


class SLIType(str, Enum):
    AVAILABILITY = "AVAILABILITY"
    LATENCY = "LATENCY"
    SUCCESS_RATE = "SUCCESS_RATE"
    QUEUE_RELIABILITY = "QUEUE_RELIABILITY"
    RECOVERY_MTTR = "RECOVERY_MTTR"


class ErrorBudgetRisk(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL_EXHAUSTED = "CRITICAL_EXHAUSTED"


class RecommendationPriority(str, Enum):
    P0_CRITICAL = "P0_CRITICAL"
    P1_HIGH = "P1_HIGH"
    P2_MEDIUM = "P2_MEDIUM"
    P3_LOW = "P3_LOW"


@dataclass
class SLIDefinition:
    sli_id: str
    name: str
    sli_type: SLIType
    service: str
    formula: str
    target_threshold: str
    current_value: float
    unit: str
    compliant: bool


@dataclass
class ReliabilityModelReport:
    total_slis_defined: int
    measurement_coverage_pct: float
    slis: List[SLIDefinition]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SLOTargetItem:
    slo_id: str
    name: str
    service: str
    target_pct: float
    actual_pct: float
    measurement_window: str
    met: bool


@dataclass
class SLOVerificationReport:
    total_slos_tracked: int
    slos_met_count: int
    slo_compliance_pct: float
    slos: List[SLOTargetItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ErrorBudgetItem:
    slo_id: str
    service: str
    total_budget_pct: float
    consumed_budget_pct: float
    remaining_budget_pct: float
    burn_rate_1h: float
    risk_level: ErrorBudgetRisk
    policy_recommendation: str


@dataclass
class ErrorBudgetReport:
    total_budgets_tracked: int
    budgets: List[ErrorBudgetItem]
    deployment_freeze_active: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FailurePatternItem:
    pattern_id: str
    component: str
    failure_signature: str
    frequency_30d: int
    trend: str  # INCREASING / STEADY / DECREASING
    primary_cause: str
    recommended_mitigation: str


@dataclass
class FailurePatternReport:
    total_patterns_identified: int
    highest_risk_component: str
    recurring_failures_detected: int
    patterns: List[FailurePatternItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RootCauseAnalysisItem:
    incident_id: str
    service: str
    symptom: str
    root_cause: str
    causal_hops: List[str]
    confidence_score: float


@dataclass
class RootCauseReport:
    total_analyses: int
    avg_confidence_score: float
    analyses: List[RootCauseAnalysisItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ServiceRiskScoreItem:
    service: str
    availability_score: float      # Weight 25%
    failure_rate_score: float      # Weight 20%
    recovery_time_score: float     # Weight 20%
    incident_frequency_score: float# Weight 15%
    capacity_risk_score: float     # Weight 10%
    security_risk_score: float     # Weight 10%
    composite_score: float         # 0 - 100
    risk_tier: str                 # LOW / MEDIUM / HIGH


@dataclass
class ReliabilityRiskReport:
    total_services_evaluated: int
    avg_composite_score: float
    service_scores: List[ServiceRiskScoreItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CapacityForecastItem:
    resource_type: str
    service: str
    current_utilization_pct: float
    growth_slope_per_day: float
    projected_days_to_exhaustion: float
    exhaustion_risk: str  # LOW / MEDIUM / HIGH / CRITICAL


@dataclass
class CapacityIntelligenceReport:
    total_resources_monitored: int
    high_risk_exhaustion_count: int
    forecasts: List[CapacityForecastItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChangeImpactItem:
    release_version: str
    deployment_timestamp: str
    pre_deploy_availability_pct: float
    post_deploy_availability_pct: float
    pre_deploy_error_rate_pct: float
    post_deploy_error_rate_pct: float
    pre_deploy_p95_latency_ms: float
    post_deploy_p95_latency_ms: float
    regression_detected: bool


@dataclass
class ChangeImpactReport:
    total_releases_analyzed: int
    regressions_detected: int
    releases: List[ChangeImpactItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChaosExperimentGain:
    experiment_id: str
    target_failure: str
    pre_optimization_mttr_seconds: float
    post_optimization_mttr_seconds: float
    improvement_pct: float
    architectural_hardening: str


@dataclass
class ChaosLearningReport:
    total_experiments_tracked: int
    avg_mttr_improvement_pct: float
    experiments: List[ChaosExperimentGain]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReliabilityRecommendation:
    rec_id: str
    priority: RecommendationPriority
    target_component: str
    action_title: str
    reason: str
    expected_impact: str
    status: str  # OPEN / IN_PROGRESS / IMPLEMENTED


@dataclass
class ReliabilityRecommendationReport:
    total_recommendations: int
    p0_count: int
    p1_count: int
    recommendations: List[ReliabilityRecommendation]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContinuousImprovementItem:
    cycle_name: str
    review_period: str
    incident_count: int
    mttr_trend_pct: float
    slo_attainment_pct: float
    completed_action_items: int


@dataclass
class ContinuousImprovementReport:
    total_cycles_reviewed: int
    improvement_velocity_active: bool
    cycles: List[ContinuousImprovementItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReliabilitySecurityCheck:
    check_id: str
    name: str
    sanitization_verified: bool
    rbac_enforced: bool
    passed: bool
    details: str


@dataclass
class ReliabilitySecurityReport:
    total_checks: int
    pii_or_secrets_exposed: bool
    access_control_active: bool
    checks: List[ReliabilitySecurityCheck]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReliabilityMaturityScorecard:
    slo_management_score: float        # Weight 20%
    reliability_analytics_score: float # Weight 20%
    failure_intelligence_score: float  # Weight 20%
    capacity_prediction_score: float   # Weight 15%
    improvement_automation_score: float# Weight 15%
    security_score: float              # Weight 10%
    overall_score: float               # Composite 0 - 100
    certification_tier: ReliabilityMaturityTier
    certification_verdict: str         # CERTIFIED / REJECTED
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)
