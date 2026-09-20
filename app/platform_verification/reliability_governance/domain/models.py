"""
Phase 3I.6: Observability Governance, SLO Engineering & Reliability Certification — Domain Models
"""
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class SLIType(str, Enum):
    AVAILABILITY = "AVAILABILITY"
    LATENCY = "LATENCY"
    AI_QUALITY = "AI_QUALITY"
    QUEUE_RELIABILITY = "QUEUE_RELIABILITY"


class ErrorBudgetAction(str, Enum):
    NORMAL_VELOCITY = "Normal Development Velocity"             # 0 - 50% consumed
    INCREASE_MONITORING = "Increase Monitoring & Review"         # 50 - 80% consumed
    PRIORITIZE_RELIABILITY = "Prioritize Reliability Engineering" # 80 - 100% consumed
    FREEZE_CHANGES = "Freeze Risky Deployments"                  # >= 100% consumed


class ReliabilityCertificationTier(str, Enum):
    ENTERPRISE_RELIABILITY_CERTIFIED = "Enterprise Reliability Certified" # 95 - 100
    PRODUCTION_RELIABILITY_READY = "Production Reliability Ready"         # 90 - 94.99
    IMPROVEMENT_REQUIRED = "Improvement Required"                         # 80 - 89.99
    FAILED = "Failed"                                                     # < 80


# ─── 3I.6.1 & 3I.6.2: Governance Architecture Models ──────────────────────────

class ServiceOwnershipBoundary(BaseModel):
    service_name: str
    owner_team: str
    on_call_rotation: str
    slos_assigned_count: int
    operational_status: str = "MANAGED"


class ReliabilityGovernanceReport(BaseModel):
    report_title: str = "Enterprise Reliability Governance Architecture Report"
    services_monitored: int = 8
    slo_defined: bool = True
    ownership_mapping: bool = True
    user_journey_reliability_model_active: bool = True
    ownership_boundaries: List[ServiceOwnershipBoundary] = Field(default_factory=list)
    status: str = "PASS"


# ─── 3I.6.3: SLI Models ───────────────────────────────────────────────────────

class SLIDefinitionSpec(BaseModel):
    sli_id: str
    name: str
    sli_type: SLIType
    formula: str
    good_events: int
    total_events: int
    current_value_pct: float
    measurement_window: str = "30-day rolling"


class SLIReport(BaseModel):
    report_title: str = "Service Level Indicators (SLI) Measurement Report"
    slis: List[SLIDefinitionSpec] = Field(default_factory=list)
    all_slis_measured: bool = True
    user_journey_coverage_pct: float = 100.0


# ─── 3I.6.4: SLO Models ───────────────────────────────────────────────────────

class SLODefinitionSpec(BaseModel):
    slo_id: str
    name: str
    sli_ref: str
    target_pct: float
    current_performance_pct: float
    compliant: bool = True
    owner: str


class SLOReport(BaseModel):
    report_title: str = "Service Level Objectives (SLO) Compliance Report"
    slos: List[SLODefinitionSpec] = Field(default_factory=list)
    all_slos_compliant: bool = True
    overall_compliance_pct: float = 100.0


# ─── 3I.6.5: Error Budget Models ──────────────────────────────────────────────

class ErrorBudgetSpec(BaseModel):
    slo_id: str
    slo_name: str
    target_pct: float
    total_budget_pct: float  # 100 - target
    consumed_budget_pct: float
    remaining_budget_pct: float
    burn_rate_1h: float
    burn_rate_6h: float
    burn_rate_24h: float
    recommended_action: ErrorBudgetAction


class ErrorBudgetReport(BaseModel):
    report_title: str = "SRE Error Budget & Burn Rate Governance Report"
    budgets: List[ErrorBudgetSpec] = Field(default_factory=list)
    deployment_freeze_required: bool = False
    average_remaining_budget_pct: float = 78.4


# ─── 3I.6.6: Reliability Dashboard Models ─────────────────────────────────────

class ReliabilityDashboardViewSpec(BaseModel):
    view_name: str  # System Health, SLO Status, AI Reliability, Infrastructure
    key_metrics_displayed: List[str]
    refresh_rate_sec: int = 15
    operational_status: str = "ACTIVE"


class ReliabilityDashboardReport(BaseModel):
    report_title: str = "Executive Reliability Dashboard Verification Report"
    views: List[ReliabilityDashboardViewSpec] = Field(default_factory=list)
    dashboards_verified: bool = True


# ─── 3I.6.7: Reliability Trend Models ─────────────────────────────────────────

class TrendIndicatorSpec(BaseModel):
    metric_name: str
    timeframe: str  # weekly, monthly
    historical_baseline: float
    current_observation: float
    trend_direction: str  # STABLE, IMPROVING, DEGRADING
    degradation_detected: bool = False


class ReliabilityTrendReport(BaseModel):
    report_title: str = "Reliability Trend & Gradual Degradation Analysis Report"
    trends: List[TrendIndicatorSpec] = Field(default_factory=list)
    gradual_degradation_detected: bool = False
    trend_stability_pct: float = 100.0


# ─── 3I.6.8 & 3I.6.9: Production Gate & Change Management Models ──────────────

class ReadinessGateCheckSpec(BaseModel):
    gate_name: str
    category: str  # Reliability, Security, Performance, Observability
    minimum_threshold_pct: float
    evaluated_score_pct: float
    gate_status: str = "PASSED"


class ProductionGateReport(BaseModel):
    report_title: str = "Production Readiness Gate & Change Management Report"
    gates: List[ReadinessGateCheckSpec] = Field(default_factory=list)
    pre_vs_post_slo_regression_detected: bool = False
    deployment_approved: bool = True


# ─── 3I.6.10: Regression Testing Models ───────────────────────────────────────

class RegressionTestSpec(BaseModel):
    test_scenario: str
    baseline_value: float
    candidate_value: float
    allowed_variance_pct: float
    actual_variance_pct: float
    regression_detected: bool = False
    status: str = "PASSED"


class ReliabilityRegressionReport(BaseModel):
    report_title: str = "Automated Release Reliability Regression Report"
    regression_tests: List[RegressionTestSpec] = Field(default_factory=list)
    all_tests_passed: bool = True
    zero_regression_verified: bool = True


# ─── 3I.6.11: Observability Data Quality Models ───────────────────────────────

class TelemetryQualityAuditSpec(BaseModel):
    telemetry_type: str  # Metrics, Logs, Traces
    completeness_pct: float
    accuracy_pct: float
    freshness_latency_sec: float
    status: str = "VERIFIED"


class TelemetryQualityReport(BaseModel):
    report_title: str = "Observability Telemetry Data Quality Report"
    audits: List[TelemetryQualityAuditSpec] = Field(default_factory=list)
    data_quality_score_pct: float = 100.0


# ─── 3I.6.12: Reliability Automation Models ───────────────────────────────────

class AutomationRuleSpec(BaseModel):
    rule_name: str
    condition: str
    automated_response: str
    validated: bool = True


class ReliabilityAutomationReport(BaseModel):
    report_title: str = "Reliability Automation & Enforcement Report"
    rules: List[AutomationRuleSpec] = Field(default_factory=list)
    automation_enforced: bool = True


# ─── 3I.6.13 & 3I.6.14: Scoring & Certification Models ────────────────────────

class ReliabilityPillarScore(BaseModel):
    pillar_name: str
    weight_pct: float
    achieved_score_pct: float
    weighted_score_pct: float
    status: str = "PASSED"


class ReliabilityCertificationReport(BaseModel):
    report_title: str = "Phase 3I.6 Enterprise Observability Governance & Reliability Certification"
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    certification_tier: ReliabilityCertificationTier = ReliabilityCertificationTier.ENTERPRISE_RELIABILITY_CERTIFIED
    overall_score_pct: float = 100.0
    minimum_passing_threshold_pct: float = 95.0
    pillar_scores: List[ReliabilityPillarScore] = Field(default_factory=list)
    certification_granted: bool = True
    auditor: str = "DocuTask Enterprise Observability Governance & SRE Reliability Certification Engine"
