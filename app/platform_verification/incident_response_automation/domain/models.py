"""Domain Models for Phase 3H.3.6: Incident Response Automation & Self-Healing Verification Framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class IncidentSeverity(str, Enum):
    SEV_1 = "SEV-1"  # Complete platform or critical dependency outage
    SEV_2 = "SEV-2"  # Major service degradation affecting throughput/accuracy
    SEV_3 = "SEV-3"  # Limited impact / non-critical component failure
    SEV_4 = "SEV-4"  # Minor anomaly or transient warning


class IncidentCategory(str, Enum):
    INFRASTRUCTURE_FAILURE = "Infrastructure Failure"
    APPLICATION_FAILURE = "Application Failure"
    DATABASE_FAILURE = "Database Failure"
    QUEUE_FAILURE = "Queue Failure"
    AI_PROVIDER_FAILURE = "AI Provider Failure"
    SECURITY_EVENT = "Security Event"
    PERFORMANCE_DEGRADATION = "Performance Degradation"


class IncidentStatus(str, Enum):
    DETECTED = "DETECTED"
    CLASSIFIED = "CLASSIFIED"
    REMEDIATING = "REMEDIATING"
    RECOVERED = "RECOVERED"
    VERIFIED = "VERIFIED"
    CLOSED = "CLOSED"
    ESCALATED = "ESCALATED"


class ActionRiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IncidentAutomationTier(str, Enum):
    FAILED = "Failed"                                               # < 80
    NEEDS_IMPROVEMENT = "Improvement Required"                     # 80 - 89
    PRODUCTION_AUTOMATION_READY = "Production Incident Automation Ready"  # 90 - 94
    AUTONOMOUS_INCIDENT_RESPONSE_READY = "Autonomous Incident Response Ready"  # 95 - 100


@dataclass
class IncidentArchitectureReport:
    incident_engine_active: bool
    detection_layer_isolated: bool
    automation_enabled: bool
    rollback_supported: bool
    audit_logging_active: bool
    subsystems: List[str]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DetectedIncidentSignal:
    signal_id: str
    source: str
    signal_type: str  # metric_threshold, error_log_pattern, trace_anomaly, alert_firing
    detected_at: str
    latency_seconds: float
    description: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IncidentDetectionReport:
    total_signals_detected: int
    avg_detection_latency_seconds: float
    precision_pct: float
    recall_pct: float
    false_positive_rate_pct: float
    false_negative_rate_pct: float
    detected_signals: List[DetectedIncidentSignal]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IncidentClassificationItem:
    incident_id: str
    category: IncidentCategory
    severity: IncidentSeverity
    affected_services: List[str]
    estimated_business_impact: str
    confidence_score: float


@dataclass
class IncidentClassificationReport:
    total_classified_incidents: int
    classification_accuracy_pct: float
    classified_items: List[IncidentClassificationItem]
    severity_breakdown: Dict[str, int]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RunbookStepResult:
    step_number: int
    action: str
    command: str
    status: str  # SUCCESS / FAILED / SKIPPED
    duration_ms: float


@dataclass
class RunbookExecutionReport:
    runbook_id: str
    name: str
    target_service: str
    risk_level: str
    total_steps: int
    successful_steps: int
    step_results: List[RunbookStepResult]
    execution_time_seconds: float
    post_checks_passed: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SelfHealingTestResult:
    test_id: str
    name: str
    target_service: str
    failure_injected: str
    detected: bool
    remediation_executed: bool
    health_verified: bool
    mttr_seconds: float
    tasks_lost: int
    passed: bool


@dataclass
class SelfHealingReport:
    total_self_healing_tests: int
    successful_recoveries: int
    avg_mttr_seconds: float
    zero_task_loss_verified: bool
    test_results: List[SelfHealingTestResult]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RecoveryPolicyRule:
    action_name: str
    target_service: str
    risk_level: ActionRiskLevel
    auto_execute: bool
    approval_required: bool
    blocked: bool
    rationale: str


@dataclass
class RecoveryPolicyReport:
    total_policy_rules: int
    auto_executable_actions: int
    approval_gated_actions: int
    blocked_dangerous_actions: int
    rules: List[RecoveryPolicyRule]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CausalChainNode:
    sequence_order: int
    source_component: str
    signal_observed: str
    timestamp: str


@dataclass
class IncidentCorrelationReport:
    incident_id: str
    title: str
    causal_chain: List[CausalChainNode]
    metric_correlation_active: bool
    trace_correlation_active: bool
    log_correlation_active: bool
    root_cause_identified: str
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IncidentKnowledgeItem:
    knowledge_id: str
    pattern_signature: str
    incident_type: str
    root_cause: str
    recommended_solution: str
    preventive_guardrail: str
    success_rate_pct: float
    times_applied: int


@dataclass
class IncidentKnowledgeReport:
    total_knowledge_entries: int
    knowledge_base_active: bool
    query_retrieval_tested: bool
    entries: List[IncidentKnowledgeItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PostmortemTimelineItem:
    timestamp: str
    phase: str
    event_description: str


@dataclass
class PostmortemReport:
    incident_id: str
    title: str
    severity: IncidentSeverity
    timeline: List[PostmortemTimelineItem]
    mttd_seconds: float
    mttr_seconds: float
    mttf_hours: float
    impact_summary: str
    root_cause_analysis: str
    remediation_steps_taken: List[str]
    preventive_action_items: List[str]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SecurityAuditCheck:
    check_id: str
    name: str
    threat_vector_protected: str
    passed: bool
    evidence: str


@dataclass
class IncidentSecurityReport:
    total_security_audits: int
    unauthorized_execution_blocked: bool
    rbac_enforced: bool
    audit_trails_immutable: bool
    checks: List[SecurityAuditCheck]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CICDPipelineReport:
    pipeline_id: str
    stages_executed: List[str]
    failure_injected: str
    automated_recovery_verified: bool
    certification_generated: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IncidentQualityScorecard:
    detection_accuracy_score: float       # Weight 20%
    recovery_automation_score: float      # Weight 20%
    safety_controls_score: float          # Weight 20%
    incident_diagnosis_score: float       # Weight 15%
    operational_learning_score: float     # Weight 15%
    security_score: float                 # Weight 10%
    overall_score: float                  # Composite 0 - 100
    certification_tier: IncidentAutomationTier
    certification_verdict: str            # CERTIFIED / REJECTED
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)
