"""
Phase 3H.5.7: Enterprise Reliability Intelligence, Health Scoring & Resilience Optimization - Domain Models
"""
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ErrorBudgetStatus(str, Enum):
    HEALTHY = "Healthy"
    WARNING = "Warning"
    CRITICAL = "Critical"
    EXHAUSTED = "Exhausted"


class HealthScoreTier(str, Enum):
    EXCELLENT_RELIABILITY = "Excellent Reliability"
    PRODUCTION_HEALTHY = "Production Healthy"
    RELIABILITY_RISK = "Reliability Risk"
    CRITICAL_IMPROVEMENT_REQUIRED = "Critical Improvement Required"


class SLOType(str, Enum):
    AVAILABILITY = "Availability"
    LATENCY = "Latency"
    PROCESSING = "Processing"
    RECOVERY = "Recovery"


class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class RecommendationPriority(str, Enum):
    P1_CRITICAL = "P1-Critical"
    P2_HIGH = "P2-High"
    P3_MEDIUM = "P3-Medium"


class GovernanceAction(str, Enum):
    ALLOW_DEPLOYMENT = "allow_deployment"
    BLOCK_DEPLOYMENT = "block_deployment"
    TRIGGER_AUTOSCALE = "trigger_autoscale"
    SCHEDULE_MAINTENANCE = "schedule_maintenance"


class ComponentTelemetryItem(BaseModel):
    component: str
    time_period: str = "24h"
    availability_pct: float
    error_count: int
    p95_latency_ms: float
    mttr_seconds: float
    failure_count: int
    llm_tokens_consumed: Optional[int] = None
    telemetry_valid: bool = True


class ReliabilityDataCollectionReport(BaseModel):
    report_title: str = "Reliability Data Collection Report"
    total_components_monitored: int
    telemetry_items: List[ComponentTelemetryItem] = Field(default_factory=list)
    collection_pipeline_healthy: bool


class ComponentReliabilityScore(BaseModel):
    component: str
    availability_score: float = Field(..., ge=0.0, le=100.0)
    performance_score: float = Field(..., ge=0.0, le=100.0)
    recovery_score: float = Field(..., ge=0.0, le=100.0)
    stability_score: float = Field(..., ge=0.0, le=100.0)
    composite_component_score: float = Field(..., ge=0.0, le=100.0)
    status: str = "HEALTHY"


class ComponentReliabilityScoreReport(BaseModel):
    report_title: str = "Component Reliability Score Report"
    total_components_scored: int
    component_scores: List[ComponentReliabilityScore] = Field(default_factory=list)
    mean_component_reliability_score: float


class SystemHealthCategoryScore(BaseModel):
    category: str
    weight: float
    raw_score: float
    weighted_score: float


class SystemReliabilityHealthReport(BaseModel):
    report_title: str = "System Reliability Health Report"
    overall_health_score: float = Field(..., ge=0.0, le=100.0)
    health_tier: HealthScoreTier
    category_breakdown: List[SystemHealthCategoryScore] = Field(default_factory=list)
    production_ready: bool


class SLOEvaluationItem(BaseModel):
    slo_type: SLOType
    slo_name: str
    target_threshold: str
    actual_value: str
    compliant: bool
    compliance_pct: float


class SLOComplianceReport(BaseModel):
    report_title: str = "SLO Compliance Report"
    total_slos_evaluated: int
    slos: List[SLOEvaluationItem] = Field(default_factory=list)
    overall_slo_compliance_pct: float
    all_slos_met: bool


class ErrorBudgetItem(BaseModel):
    service_name: str
    target_availability_pct: float = 99.9
    allowed_downtime_minutes_monthly: float = 43.2
    consumed_downtime_minutes: float
    remaining_downtime_minutes: float
    budget_consumed_pct: float
    burn_rate_ratio: float
    status: ErrorBudgetStatus


class ErrorBudgetReport(BaseModel):
    report_title: str = "Error Budget Management Report"
    service_budgets: List[ErrorBudgetItem] = Field(default_factory=list)
    overall_budget_healthy: bool
    budget_exhaustion_detected: bool = False


class ReliabilityRiskItem(BaseModel):
    risk_id: str
    component: str
    risk_type: str
    description: str
    risk_level: RiskLevel
    lead_time_to_impact: str
    probability_pct: float


class ReliabilityRiskReport(BaseModel):
    report_title: str = "Reliability Risk Analysis Report"
    total_risks_identified: int
    risks: List[ReliabilityRiskItem] = Field(default_factory=list)
    critical_risks_count: int
    risk_analysis_valid: bool


class ResilienceRecommendationItem(BaseModel):
    recommendation_id: str
    component: str
    category: str  # Architecture, Configuration, Scaling, Monitoring, Recovery, Security
    recommendation_text: str
    priority: RecommendationPriority
    expected_impact: str
    effort_estimate: str


class ResilienceRecommendationReport(BaseModel):
    report_title: str = "Resilience Recommendation Report"
    total_recommendations: int
    recommendations: List[ResilienceRecommendationItem] = Field(default_factory=list)
    high_priority_count: int


class ChaosScenarioResult(BaseModel):
    scenario_name: str
    injected_fault: str
    detection_time_ms: float
    recovery_time_seconds: float
    impact_contained: bool
    resilience_validated: bool


class ChaosValidationReport(BaseModel):
    report_title: str = "Chaos Reliability Validation Report"
    total_chaos_tests: int
    scenarios: List[ChaosScenarioResult] = Field(default_factory=list)
    all_chaos_tests_passed: bool


class ReliabilityTrendItem(BaseModel):
    horizon: str  # Daily, Weekly, Monthly
    start_reliability_score: float
    end_reliability_score: float
    score_change_pct: float
    mttr_trend_seconds: float
    slo_compliance_trend_pct: float
    trend_direction: str = "IMPROVING"


class ReliabilityTrendReport(BaseModel):
    report_title: str = "Reliability Trend Analysis Report"
    trends: List[ReliabilityTrendItem] = Field(default_factory=list)
    long_term_resilience_improving: bool


class GovernanceRuleResult(BaseModel):
    rule_name: str
    evaluated_condition: str
    triggered: bool
    action: GovernanceAction
    reason: str


class ReliabilityGovernanceReport(BaseModel):
    report_title: str = "Automated Reliability Governance Report"
    governance_rules: List[GovernanceRuleResult] = Field(default_factory=list)
    deployment_gate_approved: bool
    active_governance_actions: List[GovernanceAction] = Field(default_factory=list)


class ReliabilityScorecard(BaseModel):
    reliability_measurement_accuracy: float = Field(..., ge=0.0, le=100.0)
    health_scoring_quality: float = Field(..., ge=0.0, le=100.0)
    slo_management_score: float = Field(..., ge=0.0, le=100.0)
    error_budget_score: float = Field(..., ge=0.0, le=100.0)
    risk_prediction_score: float = Field(..., ge=0.0, le=100.0)
    recommendations_score: float = Field(..., ge=0.0, le=100.0)
    governance_score: float = Field(..., ge=0.0, le=100.0)
    composite_score: float = Field(..., ge=0.0, le=100.0)
    tier: str
    certified_enterprise_ready: bool
