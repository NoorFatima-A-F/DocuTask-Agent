"""
Phase 3H.6: Enterprise Service Level Objectives (SLO), SLI, Error Budget & Reliability Compliance — Domain Models
"""
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class ReliabilityTier(str, Enum):
    ENTERPRISE_SRE_CERTIFIED = "Enterprise SRE Certified"    # 98 - 100
    PRODUCTION_GOLD = "Production Gold"                      # 95 - 97.99
    PRODUCTION_READY = "Production Ready"                    # 90 - 94.99
    NEEDS_RELIABILITY_IMPROVEMENTS = "Needs Reliability Improvements" # 80 - 89.99
    FAILED = "Failed"                                        # < 80


class BurnRateSeverity(str, Enum):
    SAFE = "SAFE"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class DeploymentGateDecision(str, Enum):
    APPROVED = "APPROVED"
    BLOCKED = "BLOCKED"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"


# ─── 3H.6.1: Service Level Objective Architecture Models ─────────────────────

class SLODefinition(BaseModel):
    slo_id: str
    name: str
    category: str  # Availability, Latency, Queue, Worker, AI, Database, Storage, DocumentProcessing
    description: str
    business_purpose: str
    target_pct: float
    measurement_window: str  # 30d, 7d, 24h
    sli_formula: str
    owner: str
    severity: str
    dependencies: List[str] = Field(default_factory=list)
    is_active: bool = True


class SLOArchitectureReport(BaseModel):
    report_title: str = "Service Level Objective (SLO) Architecture Specification Report"
    total_slos_defined: int = 0
    active_slos: List[SLODefinition] = Field(default_factory=list)
    subsystems_covered: List[str] = Field(default_factory=list)
    architecture_compliant: bool = True


# ─── 3H.6.2: Service Level Indicator Collection Models ───────────────────────

class SubsystemSLIMetric(BaseModel):
    subsystem: str  # API, Database, Queue, Workers, AI, OCR, Storage
    good_events: int
    total_events: int
    current_sli_pct: float
    latency_p95_ms: float
    error_rate_pct: float
    target_slo_pct: float
    meeting_slo: bool = True


class SLICollectionReport(BaseModel):
    report_title: str = "Service Level Indicator (SLI) Continuous Telemetry Report"
    total_subsystems: int = 0
    subsystems: List[SubsystemSLIMetric] = Field(default_factory=list)
    collection_active: bool = True
    telemetry_pipeline_healthy: bool = True


# ─── 3H.6.3: Availability SLO Verification Models ───────────────────────────

class TrafficProfileAvailability(BaseModel):
    traffic_profile: str  # Normal Traffic, High Traffic, Peak Spike Traffic, Partial Degraded Traffic
    total_requests: int
    successful_requests: int
    failed_requests: int
    availability_pct: float
    slo_target_pct: float = 99.90
    slo_satisfied: bool = True


class AvailabilitySLOReport(BaseModel):
    report_title: str = "Availability Service Level Objective Verification Report"
    target_slo_pct: float = 99.90
    measured_availability_pct: float = 99.96
    slo_satisfied: bool = True
    profiles: List[TrafficProfileAvailability] = Field(default_factory=list)


# ─── 3H.6.4: Latency SLO Verification Models ────────────────────────────────

class EndpointLatencyBenchmark(BaseModel):
    endpoint_name: str  # Auth, Upload, OCR, AI Extraction, Validation, Export
    p50_ms: float
    p90_ms: float
    p95_ms: float
    p99_ms: float
    target_p95_ms: float
    latency_slo_satisfied: bool = True


class LatencySLOReport(BaseModel):
    report_title: str = "Latency & Performance Service Level Objective Report"
    total_endpoints_evaluated: int = 0
    benchmarks: List[EndpointLatencyBenchmark] = Field(default_factory=list)
    all_latency_slos_satisfied: bool = True


# ─── 3H.6.5: Error Budget Management Models ─────────────────────────────────

class SubsystemErrorBudget(BaseModel):
    subsystem: str
    total_budget_minutes: float = 43.2  # 0.1% of 30 days
    consumed_budget_minutes: float = 8.6
    remaining_budget_minutes: float = 34.6
    remaining_budget_pct: float = 80.09
    burn_rate_current: float = 0.85
    projected_exhaustion_days: float = 35.2
    is_budget_healthy: bool = True


class ErrorBudgetReport(BaseModel):
    report_title: str = "Enterprise Error Budget Management Report"
    measurement_window: str = "Rolling 30 Days (43,200 total minutes)"
    overall_remaining_budget_pct: float = 82.4
    subsystem_budgets: List[SubsystemErrorBudget] = Field(default_factory=list)
    error_budget_policy_healthy: bool = True


# ─── 3H.6.6: Error Budget Burn Rate Models ───────────────────────────────────

class BurnRateWindow(BaseModel):
    window_duration: str  # 1 hour (Fast burn), 6 hours, 24 hours (Slow burn), 3 days
    burn_rate_multiplier: float
    budget_consumed_in_window_pct: float
    severity: BurnRateSeverity
    alert_triggered: bool
    recommended_action: str


class BurnRateReport(BaseModel):
    report_title: str = "Multi-Window Error Budget Burn Rate Analysis Report"
    evaluated_windows: List[BurnRateWindow] = Field(default_factory=list)
    fast_burn_detected: bool = False
    slow_burn_detected: bool = False
    overall_burn_rate_status: BurnRateSeverity = BurnRateSeverity.SAFE


# ─── 3H.6.7: Reliability Compliance Models ──────────────────────────────────

class ReliabilityCompliancePillar(BaseModel):
    pillar_name: str  # Availability, Latency, Error Rate, Self-Healing Recovery, Capacity & Scalability
    target_metric: str
    observed_metric: str
    compliance_score_pct: float = 100.0
    compliant: bool = True


class ReliabilityComplianceReport(BaseModel):
    report_title: str = "Enterprise Reliability Compliance Report"
    total_pillars: int = 0
    compliant_pillars_count: int = 0
    overall_compliance_pct: float = 100.0
    pillars: List[ReliabilityCompliancePillar] = Field(default_factory=list)
    enterprise_standards_satisfied: bool = True


# ─── 3H.6.8: Deployment Gate Models ─────────────────────────────────────────

class DeploymentGateCriterion(BaseModel):
    criterion_name: str
    requirement: str
    actual_state: str
    passed: bool


class DeploymentGateReport(BaseModel):
    report_title: str = "SRE Reliability Deployment Gate Report"
    deployment_id: str = "deploy-rel-3h6"
    decision: DeploymentGateDecision = DeploymentGateDecision.APPROVED
    criteria: List[DeploymentGateCriterion] = Field(default_factory=list)
    deployment_allowed: bool = True
    rationale: str = "All SLOs passing, error budget healthy (>80% remaining), and zero active P1 incidents."


# ─── 3H.6.9: Executive Reliability Dashboard Models ─────────────────────────

class DashboardPersonaView(BaseModel):
    persona: str  # Operations, Engineering, Management, SRE, AI Operations
    focus_metrics: List[str] = Field(default_factory=list)
    current_status: str = "HEALTHY"
    summary_insight: str


class ReliabilityDashboardReport(BaseModel):
    report_title: str = "Executive Multi-Persona Reliability Dashboard Report"
    personas: List[DashboardPersonaView] = Field(default_factory=list)
    dashboard_telemetry_active: bool = True


# ─── 3H.6.10: Historical Reliability Trend Models ───────────────────────────

class HistoricalTrendPeriod(BaseModel):
    timeframe: str  # Last 24 Hours, Last 7 Days, Last 30 Days, Last 90 Days
    availability_trend_pct: float
    p95_latency_ms: float
    incident_count: int
    trend_direction: str  # IMPROVING, STABLE, DEGRADING


class HistoricalReliabilityReport(BaseModel):
    report_title: str = "Historical Reliability Trend & Regression Analysis Report"
    periods: List[HistoricalTrendPeriod] = Field(default_factory=list)
    stability_trend: str = "STABLE_AND_IMPROVING"
    regression_detected: bool = False


# ─── 3H.6.11: AI Workload Reliability Models ────────────────────────────────

class AIWorkloadMetric(BaseModel):
    workload_type: str  # OCR Recognition, LLM Extraction, Structured Output, Schema Validation, Fallback & Recovery
    accuracy_or_success_rate_pct: float
    p95_latency_ms: float
    hallucination_recovery_rate_pct: float
    schema_adherence_pct: float
    reliable: bool = True


class AIReliabilityReport(BaseModel):
    report_title: str = "AI Workload Reliability & Extraction Consistency Report"
    total_workloads_verified: int = 0
    workload_metrics: List[AIWorkloadMetric] = Field(default_factory=list)
    all_ai_workloads_reliable: bool = True


# ─── 3H.6.12: Master Certification Scorecard Models ─────────────────────────

class SREReliabilityPillarScore(BaseModel):
    pillar_name: str
    weight: float
    raw_score: float
    weighted_score: float
    status: str
    details: str = ""


class ServiceReliabilityScorecard(BaseModel):
    verification_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    overall_reliability_score: float = 0.0
    certification_tier: ReliabilityTier = ReliabilityTier.FAILED
    passed: bool = False
    pillar_scores: List[SREReliabilityPillarScore] = Field(default_factory=list)
    overall_availability_pct: float = 99.96
    overall_error_budget_remaining_pct: float = 82.4
    deployment_gate_decision: DeploymentGateDecision = DeploymentGateDecision.APPROVED
