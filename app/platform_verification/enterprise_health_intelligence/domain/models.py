"""
Phase 3H.5: Enterprise Health Intelligence, Diagnosis & Automated Remediation - Domain Models
"""
from enum import Enum
from typing import Dict, List, Any
from pydantic import BaseModel, Field


class HealthEventType(str, Enum):
    SERVICE_DOWN = "SERVICE_DOWN"
    DEPENDENCY_FAILURE = "DEPENDENCY_FAILURE"
    HIGH_LATENCY = "HIGH_LATENCY"
    RESOURCE_EXHAUSTION = "RESOURCE_EXHAUSTION"
    QUEUE_OVERFLOW = "QUEUE_OVERFLOW"
    WORKER_FAILURE = "WORKER_FAILURE"
    AI_PROVIDER_FAILURE = "AI_PROVIDER_FAILURE"


class FailureCategory(str, Enum):
    INFRASTRUCTURE_FAILURE = "INFRASTRUCTURE_FAILURE"
    DEPENDENCY_FAILURE = "DEPENDENCY_FAILURE"
    APPLICATION_FAILURE = "APPLICATION_FAILURE"
    AI_SYSTEM_FAILURE = "AI_SYSTEM_FAILURE"


class RemediationRiskLevel(str, Enum):
    SAFE_AUTOMATIC = "SAFE_AUTOMATIC"
    RISKY_APPROVAL_REQUIRED = "RISKY_APPROVAL_REQUIRED"
    DANGEROUS_FORBIDDEN = "DANGEROUS_FORBIDDEN"


class IntelligenceCertificationTier(str, Enum):
    AUTONOMOUS_RELIABILITY_READY = "Autonomous Reliability Ready"
    PRODUCTION_RELIABILITY_READY = "Production Reliability Ready"
    IMPROVEMENT_REQUIRED = "Improvement Required"
    FAILED = "Failed"


class HealthEvent(BaseModel):
    id: str
    type: HealthEventType
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    component: str
    timestamp: str
    source: str
    metrics: Dict[str, Any]
    dependencies: List[str]
    status: str = "ACTIVE"


class HealthEventArchitectureReport(BaseModel):
    report_title: str = "Health Event Intelligence Architecture Report"
    total_events_captured: int
    pipeline_stages: List[str] = Field(
        default_factory=lambda: [
            "Event Collector",
            "Event Normalizer",
            "Correlation Engine",
            "Diagnosis Engine",
            "Remediation Engine",
            "Recovery Validator",
        ]
    )
    supported_event_types: List[str]
    events: List[HealthEvent] = Field(default_factory=list)
    architecture_valid: bool = True


class FailureClassificationItem(BaseModel):
    event_id: str
    failure_type: FailureCategory
    component: str
    confidence: float
    classified_correctly: bool = True


class FailureClassificationReport(BaseModel):
    report_title: str = "Failure Classification Report"
    total_classified_events: int
    classifications: List[FailureClassificationItem] = Field(default_factory=list)
    classification_accuracy_pct: float
    classification_valid: bool = True


class CorrelatedIncident(BaseModel):
    incident_id: str
    incident_name: str
    root_component: str
    severity: str
    raw_signals: List[str]
    temporal_window: str
    dependency_chain: List[str]
    incident_status: str = "RESOLVED"


class EventCorrelationReport(BaseModel):
    report_title: str = "Health Signal Correlation Report"
    total_raw_signals: int
    total_correlated_incidents: int
    noise_reduction_pct: float
    incidents: List[CorrelatedIncident] = Field(default_factory=list)
    correlation_valid: bool = True


class RCAResult(BaseModel):
    incident_id: str
    root_cause: str
    confidence: float
    evidence: List[str]
    affected_services: List[str]
    rca_status: str = "CONFIRMED"


class RCAReport(BaseModel):
    report_title: str = "Root Cause Analysis Report"
    total_rcas_performed: int
    results: List[RCAResult] = Field(default_factory=list)
    mean_confidence_score: float
    rca_valid: bool = True


class RemediationDecisionItem(BaseModel):
    decision_id: str
    target_component: str
    action: str
    risk_level: RemediationRiskLevel
    approval_required: bool
    reason: str
    decision_valid: bool = True


class RemediationDecisionReport(BaseModel):
    report_title: str = "Automated Remediation Decision Report"
    total_decisions: int
    decisions: List[RemediationDecisionItem] = Field(default_factory=list)
    safety_classification_enforced: bool = True


class RecoveryExecutionStep(BaseModel):
    scenario: str
    action_executed: str
    duration_ms: float
    service_state_post_action: str
    success: bool


class RecoveryExecutionReport(BaseModel):
    report_title: str = "Recovery Execution Report"
    total_recovery_scenarios: int
    steps: List[RecoveryExecutionStep] = Field(default_factory=list)
    recovery_success_rate_pct: float
    all_recoveries_successful: bool = True


class SelfHealingScenarioResult(BaseModel):
    scenario_name: str
    injected_failure: str
    detection_passed: bool
    diagnosis_passed: bool
    remediation_passed: bool
    health_validated: bool
    scenario_success: bool


class SelfHealingValidationReport(BaseModel):
    report_title: str = "Self-Healing Validation Report"
    automatic_recovery_success_rate: float
    mean_time_to_detection_seconds: float
    mean_time_to_recovery_seconds: float
    remediation_accuracy_pct: float
    false_recovery_rate_pct: float
    scenarios: List[SelfHealingScenarioResult] = Field(default_factory=list)
    self_healing_certified: bool = True


class RemediationSecurityReport(BaseModel):
    report_title: str = "Remediation Safety & Security Report"
    least_privilege_enforced: bool = True
    audit_trail_immutable: bool = True
    rollback_supported: bool = True
    forbidden_actions_blocked: bool = True
    security_score_pct: float = 100.0


class DashboardMetric(BaseModel):
    dashboard_name: str
    active_panels: int
    refresh_rate_seconds: int
    status: str = "ONLINE"


class HealthDashboardReport(BaseModel):
    report_title: str = "Health Intelligence Observability Report"
    dashboards: List[DashboardMetric] = Field(default_factory=list)
    all_dashboards_active: bool = True


class ChaosHealthResult(BaseModel):
    test_name: str
    fault_type: str
    detection_ms: float
    diagnosis_accuracy_pct: float
    recovery_succeeded: bool


class ChaosHealthReport(BaseModel):
    report_title: str = "Chaos Health Intelligence Report"
    tests: List[ChaosHealthResult] = Field(default_factory=list)
    all_chaos_tests_passed: bool = True


class HealthIntelligenceScorecard(BaseModel):
    failure_detection_score: float = Field(..., ge=0.0, le=100.0)
    diagnosis_accuracy_score: float = Field(..., ge=0.0, le=100.0)
    event_correlation_score: float = Field(..., ge=0.0, le=100.0)
    rca_quality_score: float = Field(..., ge=0.0, le=100.0)
    recovery_automation_score: float = Field(..., ge=0.0, le=100.0)
    safety_controls_score: float = Field(..., ge=0.0, le=100.0)
    composite_score: float = Field(..., ge=0.0, le=100.0)
    tier: IntelligenceCertificationTier
    certified_enterprise_ready: bool
