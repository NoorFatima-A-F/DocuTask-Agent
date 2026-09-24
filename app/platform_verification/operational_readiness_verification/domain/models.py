"""
Phase 3H.4.11: Enterprise Operational Readiness Scoring & Certification Framework - Domain Models
"""
from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


class MaturityLevel(str, Enum):
    LEVEL_0_UNKNOWN = "Level 0 - Unknown"
    LEVEL_1_BASIC_MONITORING = "Level 1 - Basic Monitoring"
    LEVEL_2_OBSERVABLE = "Level 2 - Observable"
    LEVEL_3_OPERATIONAL = "Level 3 - Operational"
    LEVEL_4_RELIABLE = "Level 4 - Reliable"
    LEVEL_5_ENTERPRISE = "Level 5 - Enterprise"


class CertificationStatus(str, Enum):
    ENTERPRISE_OBSERVABILITY_READY = "Enterprise Observability Ready"
    PRODUCTION_READY = "Production Ready"
    IMPROVEMENT_REQUIRED = "Improvement Required"
    FAILED_BLOCKED = "Failed / Blocked"


class RiskLevel(str, Enum):
    NEGLIGIBLE = "Negligible"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class MetricsCompletenessScore(BaseModel):
    application_metrics_coverage: float = Field(..., ge=0.0, le=100.0)
    agent_metrics_coverage: float = Field(..., ge=0.0, le=100.0)
    queue_metrics_coverage: float = Field(..., ge=0.0, le=100.0)
    infrastructure_metrics_coverage: float = Field(..., ge=0.0, le=100.0)
    score: float = Field(..., ge=0.0, le=100.0)
    passed: bool


class MonitoringAccuracyScore(BaseModel):
    detection_success_rate: float = Field(..., ge=0.0, le=100.0)
    mean_time_to_detect_seconds: float
    mttd_benchmark_met: bool
    monitored_components_coverage: float = Field(..., ge=0.0, le=100.0)
    score: float = Field(..., ge=0.0, le=100.0)
    passed: bool


class AlertReliabilityScore(BaseModel):
    precision_rate: float = Field(..., ge=0.0, le=100.0)
    recall_rate: float = Field(..., ge=0.0, le=100.0)
    auto_resolution_rate: float = Field(..., ge=0.0, le=100.0)
    false_positive_rate: float = Field(..., ge=0.0, le=100.0)
    score: float = Field(..., ge=0.0, le=100.0)
    passed: bool


class IncidentQualityScore(BaseModel):
    payload_completeness_rate: float = Field(..., ge=0.0, le=100.0)
    diagnostic_value_rate: float = Field(..., ge=0.0, le=100.0)
    runbook_attachment_rate: float = Field(..., ge=0.0, le=100.0)
    score: float = Field(..., ge=0.0, le=100.0)
    passed: bool


class DashboardUsabilityScore(BaseModel):
    system_dashboard_completeness: float = Field(..., ge=0.0, le=100.0)
    ai_workflow_dashboard_completeness: float = Field(..., ge=0.0, le=100.0)
    infrastructure_dashboard_completeness: float = Field(..., ge=0.0, le=100.0)
    agent_dashboard_completeness: float = Field(..., ge=0.0, le=100.0)
    score: float = Field(..., ge=0.0, le=100.0)
    passed: bool


class SecurityReadinessScore(BaseModel):
    log_sanitization_rate: float = Field(..., ge=0.0, le=100.0)
    metric_privacy_rate: float = Field(..., ge=0.0, le=100.0)
    trace_scrubbing_rate: float = Field(..., ge=0.0, le=100.0)
    rbac_enforcement_rate: float = Field(..., ge=0.0, le=100.0)
    transport_encryption_rate: float = Field(..., ge=0.0, le=100.0)
    score: float = Field(..., ge=0.0, le=100.0)
    passed: bool


class MaturityReport(BaseModel):
    level: MaturityLevel
    level_numeric: int
    criteria_met: List[str] = Field(default_factory=list)
    next_level_requirements: List[str] = Field(default_factory=list)


class RiskItem(BaseModel):
    risk_id: str
    category: str
    severity: RiskLevel
    description: str
    is_blocking: bool
    remediation_ref: str


class OperationalRiskReport(BaseModel):
    overall_risk: RiskLevel
    blocking_risks_count: int
    hard_gate_passed: bool
    evaluated_risks: List[RiskItem] = Field(default_factory=list)


class RemediationAction(BaseModel):
    action_id: str
    target_category: str
    priority: str
    issue_detected: str
    recommended_action: str
    impact: str


class RemediationReport(BaseModel):
    total_recommendations: int
    recommendations: List[RemediationAction] = Field(default_factory=list)


class CertificationResult(BaseModel):
    certification: CertificationStatus
    composite_score: float = Field(..., ge=0.0, le=100.0)
    risk_level: RiskLevel
    maturity_level: MaturityLevel
    release_approved: bool
    blocking_issues: List[str] = Field(default_factory=list)
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)


class OperationalReadinessScorecard(BaseModel):
    metrics_completeness: MetricsCompletenessScore
    monitoring_accuracy: MonitoringAccuracyScore
    alert_reliability: AlertReliabilityScore
    incident_quality: IncidentQualityScore
    dashboard_usability: DashboardUsabilityScore
    security_readiness: SecurityReadinessScore
    composite_score: float = Field(..., ge=0.0, le=100.0)
    maturity_report: MaturityReport
    risk_report: OperationalRiskReport
    certification_result: CertificationResult
    remediation_report: RemediationReport
