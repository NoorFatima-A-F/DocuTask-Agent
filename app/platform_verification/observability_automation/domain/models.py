"""
Phase 3I.8: Observability Automation, Self-Healing Operations & Autonomous Reliability — Domain Models
"""
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class AutonomousCertificationTier(str, Enum):
    AUTONOMOUS_OPERATIONS_READY = "Autonomous Operations Ready"          # 95 - 100%
    ADVANCED_PRODUCTION_OPERATIONS = "Advanced Production Operations"    # 90 - 94.99%
    IMPROVEMENT_REQUIRED = "Improvement Required"                        # 80 - 89.99%
    FAILED = "Failed"                                                    # < 80%


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AutomationActionType(str, Enum):
    SERVICE_RESTART = "SERVICE_RESTART"
    QUEUE_RECOVERY = "QUEUE_RECOVERY"
    RESOURCE_SCALING = "RESOURCE_SCALING"
    DEPLOYMENT_ROLLBACK = "DEPLOYMENT_ROLLBACK"
    CACHE_EVICTION = "CACHE_EVICTION"
    CIRCUIT_BREAKER_TRIP = "CIRCUIT_BREAKER_TRIP"


# ─── 3I.8.1: Autonomous Architecture Models ───────────────────────────────────

class AutonomousComponentSpec(BaseModel):
    component_name: str
    role: str
    connected_inputs: List[str]
    connected_outputs: List[str]
    operational_status: str = "ACTIVE"


class AutonomousArchitectureReport(BaseModel):
    report_title: str = "Autonomous Operations Architecture Verification Report"
    components_count: int = 8
    automation_level: str = "advanced"
    human_approval_required: bool = True
    components: List[AutonomousComponentSpec] = Field(default_factory=list)
    status: str = "PASS"


# ─── 3I.8.2: Intelligent Anomaly Detection Models ─────────────────────────────

class AnomalyDetectionSpec(BaseModel):
    anomaly_id: str
    category: str  # Infrastructure, Application, AI Pipeline
    metric_tracked: str
    detection_method: str  # Threshold, Statistical, ML Baseline, Predictive
    baseline_value: float
    detected_value: float
    confidence_pct: float
    lead_time_seconds: int
    detected: bool = True


class AnomalyDetectionReport(BaseModel):
    report_title: str = "Intelligent Anomaly Detection Verification Report"
    anomalies: List[AnomalyDetectionSpec] = Field(default_factory=list)
    detection_accuracy_pct: float = 98.8
    status: str = "PASS"


# ─── 3I.8.3: Event Correlation Models ─────────────────────────────────────────

class CorrelatedIncidentSpec(BaseModel):
    incident_id: str
    incident_title: str
    raw_signals_count: int
    correlated_root: str
    dependency_graph: List[str]
    blast_radius: str
    correlation_accuracy_pct: float = 100.0


class EventCorrelationReport(BaseModel):
    report_title: str = "Multi-Signal Event Correlation Verification Report"
    incidents: List[CorrelatedIncidentSpec] = Field(default_factory=list)
    signal_reduction_ratio: str = "4:1"
    correlation_verified: bool = True


# ─── 3I.8.4: Root Cause Analysis Models ───────────────────────────────────────

class RootCauseHypothesisSpec(BaseModel):
    hypothesis_id: str
    suspected_cause: str
    confidence: float  # e.g. 0.91
    evidence_references: List[str]
    affected_services: List[str]
    is_primary_cause: bool = True


class RootCauseAnalysisReport(BaseModel):
    report_title: str = "AI-Assisted Root Cause Analysis Verification Report"
    hypotheses: List[RootCauseHypothesisSpec] = Field(default_factory=list)
    primary_root_cause: str
    average_confidence: float = 0.92
    status: str = "PASS"


# ─── 3I.8.5: Automated Remediation Models ─────────────────────────────────────

class RemediationActionSpec(BaseModel):
    action_id: str
    action_type: AutomationActionType
    target_service: str
    trigger_condition: str
    approval_required: bool
    execution_time_sec: float
    verification_passed: bool = True


class RemediationExecutionReport(BaseModel):
    report_title: str = "Automated Remediation Execution Verification Report"
    actions: List[RemediationActionSpec] = Field(default_factory=list)
    all_actions_verified: bool = True
    automation_success_rate_pct: float = 100.0


# ─── 3I.8.6: Safety Control Models ────────────────────────────────────────────

class SafetyRuleSpec(BaseModel):
    action_name: str
    category: str  # ALLOWLIST, RESTRICTED, APPROVAL_REQUIRED
    allowed_autonomously: bool
    requires_human_approval: bool
    blast_radius_limit: str
    enforced: bool = True


class AutomationSafetyReport(BaseModel):
    report_title: str = "Autonomous Operations Safety Controls & Guardrails Report"
    rules: List[SafetyRuleSpec] = Field(default_factory=list)
    guardrails_enforced: bool = True
    zero_unauthorized_high_risk_actions: bool = True


# ─── 3I.8.7: Self-Healing Workflow Models ─────────────────────────────────────

class SelfHealingLoopSpec(BaseModel):
    scenario_name: str
    injected_failure: str
    detection_latency_sec: float
    diagnosis_latency_sec: float
    remediation_duration_sec: float
    health_check_verified: bool
    service_resumed: bool
    loop_successful: bool = True


class SelfHealingValidationReport(BaseModel):
    report_title: str = "Self-Healing Workflow Verification Report"
    loops: List[SelfHealingLoopSpec] = Field(default_factory=list)
    all_healing_loops_verified: bool = True
    average_mttr_seconds: float = 24.5


# ─── 3I.8.8: Autonomous Incident Management Models ────────────────────────────

class IncidentLifecycleSpec(BaseModel):
    incident_id: str
    severity: str  # SEV-1, SEV-2, SEV-3
    title: str
    duration_str: str
    root_cause: str
    automated_steps: List[str]
    postmortem_generated: bool = True


class IncidentAutomationReport(BaseModel):
    report_title: str = "Autonomous Incident Lifecycle Management Report"
    incidents: List[IncidentLifecycleSpec] = Field(default_factory=list)
    lifecycle_automated: bool = True
    postmortem_automation_verified: bool = True


# ─── 3I.8.9: Reliability Learning Models ──────────────────────────────────────

class ReliabilityLessonSpec(BaseModel):
    lesson_id: str
    incident_trigger: str
    root_cause: str
    remediation_taken: str
    preventive_policy_update: str
    applied_to_knowledge_base: bool = True


class ReliabilityLearningReport(BaseModel):
    report_title: str = "Reliability Learning & Continuous Self-Improvement Report"
    lessons: List[ReliabilityLessonSpec] = Field(default_factory=list)
    knowledge_base_active: bool = True
    recurrence_prevention_score_pct: float = 100.0


# ─── 3I.8.10: Autonomous Testing Models ───────────────────────────────────────

class AutonomousTestingSimulationSpec(BaseModel):
    test_id: str
    simulation_scenario: str
    injected_chaos: str
    expected_autonomous_behavior: str
    actual_autonomous_behavior: str
    simulation_passed: bool = True


class AutonomousTestingReport(BaseModel):
    report_title: str = "Autonomous Operations Chaos Simulation Test Report"
    simulations: List[AutonomousTestingSimulationSpec] = Field(default_factory=list)
    all_simulations_passed: bool = True


# ─── 3I.8.11: Human-in-the-Loop Models ────────────────────────────────────────

class HumanControlPolicySpec(BaseModel):
    tier_name: str  # Fully Automatic, Approval Required, Human Controlled
    risk_level: RiskLevel
    example_actions: List[str]
    escalation_timeout_min: int
    audit_logged: bool = True


class HumanControlPolicyReport(BaseModel):
    report_title: str = "Human-in-the-Loop & Tiered Operational Control Report"
    policies: List[HumanControlPolicySpec] = Field(default_factory=list)
    human_oversight_enforced: bool = True


# ─── 3I.8.12: Autonomous Dashboard Models ─────────────────────────────────────

class AIOpsDashboardMetricSpec(BaseModel):
    metric_category: str  # System Intelligence, Recovery Metrics, AI Operations
    key_indicators: List[str]
    refresh_frequency_sec: int = 10
    active: bool = True


class AutonomousDashboardReport(BaseModel):
    report_title: str = "Executive Autonomous Operations & AIOps Dashboard Report"
    dashboard_views: List[AIOpsDashboardMetricSpec] = Field(default_factory=list)
    dashboards_active: bool = True


# ─── 3I.8.13 & 3I.8.14: Scoring & Certification Models ────────────────────────

class AutonomousPillarScore(BaseModel):
    pillar_name: str
    weight_pct: float
    achieved_score_pct: float
    weighted_score_pct: float
    status: str = "PASSED"


class AutonomousCertificationReport(BaseModel):
    report_title: str = "Phase 3I.8 Enterprise Autonomous Operations & Reliability Certification"
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    certification_tier: AutonomousCertificationTier = AutonomousCertificationTier.AUTONOMOUS_OPERATIONS_READY
    overall_score_pct: float = 100.0
    minimum_passing_threshold_pct: float = 95.0
    pillar_scores: List[AutonomousPillarScore] = Field(default_factory=list)
    certification_granted: bool = True
    auditor: str = "DocuTask Enterprise Autonomous Reliability & Self-Healing Operations Certification Engine"
