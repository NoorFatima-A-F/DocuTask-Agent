"""Domain Models for Phase 5: Enterprise End-to-End Autonomous Workflow & Business Process Validation Framework."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List
from pydantic import BaseModel, Field


class VerificationStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"


class CertificationTier(str, Enum):
    ENTERPRISE_AUTONOMOUS_BUSINESS_READY = "Enterprise Autonomous Business Ready"
    HIGH_OPERATIONAL_MATURITY = "High Operational Maturity"
    CONDITIONALLY_CERTIFIED = "Conditionally Certified"
    CERTIFICATION_FAILED = "Certification Failed"


class CheckResult(BaseModel):
    check_id: str
    name: str
    status: VerificationStatus
    score: float = Field(ge=0.0, le=100.0)
    message: str
    details: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part A: Business Scenario Library
class BusinessScenarioSpec(BaseModel):
    scenario_id: str
    domain: str
    scenario_name: str
    document_types: List[str]
    complexity: str
    expected_sla_sec: float
    verified: bool


class ScenarioLibraryReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    total_domains: int
    total_scenarios: int
    scenarios: List[BusinessScenarioSpec] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part B: Complete Workflow Execution
class WorkflowExecutionStage(BaseModel):
    stage_number: int
    stage_name: str
    duration_ms: float
    success: bool
    state_hash: str


class CompleteWorkflowExecutionReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    total_stages: int
    e2e_duration_ms: float
    all_stages_passed: bool
    stages: List[WorkflowExecutionStage] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part C: Human-in-the-Loop
class HITLInteraction(BaseModel):
    interaction_id: str
    event_type: str
    human_role: str
    response_latency_sec: float
    outcome: str
    audit_logged: bool


class HumanInTheLoopReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    total_hitl_events: int
    approval_accuracy_pct: float
    timeout_handling_verified: bool
    interactions: List[HITLInteraction] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part D: Multi-Agent Business Collaboration
class AgentRolePerformance(BaseModel):
    role_name: str
    tasks_assigned: int
    tasks_completed: int
    consensus_agreements: int
    redundant_work_detected: bool


class MultiAgentBusinessCollaborationReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    total_agents_engaged: int
    collaboration_efficiency_pct: float
    consensus_accuracy_pct: float
    roles: List[AgentRolePerformance] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part E: Decision Quality
class DecisionQualityMetric(BaseModel):
    decision_type: str
    confidence_score: float
    evidence_backed: bool
    policy_compliant: bool
    stability_verified: bool


class DecisionQualityReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    overall_decision_accuracy_pct: float
    confidence_calibration_error: float
    decision_stability_pct: float
    metrics: List[DecisionQualityMetric] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part F: Business Rule Enforcement
class BusinessRulePolicy(BaseModel):
    rule_name: str
    policy_category: str
    threshold_value: str
    enforcement_passed: bool
    override_authorized: bool


class BusinessRuleEnforcementReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    total_rules_tested: int
    violations_prevented: int
    enforcement_success_rate_pct: float
    rules: List[BusinessRulePolicy] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part G: Exception Workflow
class ExceptionSimulation(BaseModel):
    exception_type: str
    fault_payload: str
    detected_properly: bool
    graceful_fallback: str
    recovered_successfully: bool


class ExceptionWorkflowReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    total_exceptions_simulated: int
    graceful_recovery_rate_pct: float
    unhandled_crashes_count: int
    simulations: List[ExceptionSimulation] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part H: Business KPI
class BusinessKPIData(BaseModel):
    kpi_name: str
    baseline_value: float
    achieved_value: float
    unit: str
    improvement_pct: float


class BusinessKPIReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    automation_rate_pct: float
    labor_reduction_pct: float
    speedup_multiplier: float
    sla_compliance_pct: float
    kpis: List[BusinessKPIData] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part I: Autonomous Recovery
class AutonomousRecoveryEvent(BaseModel):
    failure_mode: str
    checkpoint_restored: str
    continuation_successful: bool
    recovery_duration_sec: float


class AutonomousRecoveryReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    recovery_success_rate_pct: float
    data_loss_detected: bool
    avg_recovery_time_sec: float
    events: List[AutonomousRecoveryEvent] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part J: Organizational Workflow
class DepartmentalTransition(BaseModel):
    from_department: str
    to_department: str
    artifact_passed: str
    handshake_latency_ms: float
    context_preserved: bool


class OrganizationalWorkflowReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    total_departments_orchestrated: int
    cross_dept_handoff_success_rate_pct: float
    transitions: List[DepartmentalTransition] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part K: Long-Running Workflow
class LongRunningCheckpoint(BaseModel):
    checkpoint_id: str
    elapsed_time_simulated: str
    state_valid: bool
    resumed_cleanly: bool


class LongRunningWorkflowReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    max_duration_simulated: str
    checkpoint_integrity_pct: float
    resume_after_crash_verified: bool
    checkpoints: List[LongRunningCheckpoint] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part L: Explainability Validation
class ExplainabilityItem(BaseModel):
    item_type: str
    explanation_provided: bool
    evidence_citation_valid: bool
    policy_reference_linked: bool


class ExplainabilityValidationReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    explainability_coverage_pct: float
    citation_fidelity_score_pct: float
    items: List[ExplainabilityItem] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part M: Audit Trail Validation
class AuditLogEntry(BaseModel):
    audit_id: str
    action: str
    actor: str
    tamper_proof_hash: str
    reconstructable: bool


class AuditTrailValidationReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    total_audit_records: int
    provenance_reconstruction_pct: float
    tamper_detection_verified: bool
    audit_entries: List[AuditLogEntry] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part N: Compliance Validation
class ComplianceFrameworkAudit(BaseModel):
    framework_name: str
    controls_tested: int
    controls_passed: int
    compliance_status: str


class ComplianceValidationReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    overall_compliance_rate_pct: float
    frameworks: List[ComplianceFrameworkAudit] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part O: Cost Validation
class WorkflowCostBreakdown(BaseModel):
    cost_category: str
    cost_per_unit_usd: float
    total_cost_usd: float
    pct_of_total: float


class CostValidationReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    cost_per_document_usd: float
    cost_savings_vs_manual_pct: float
    cost_breakdown: List[WorkflowCostBreakdown] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part P: Workflow Optimization
class OptimizationMetric(BaseModel):
    target_area: str
    pre_optimization_value: float
    post_optimization_value: float
    gain_pct: float


class WorkflowOptimizationReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    overall_efficiency_gain_pct: float
    metrics: List[OptimizationMetric] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part Q: Business Value
class ValueRealizationSpec(BaseModel):
    metric_name: str
    annual_impact_usd: float
    hours_saved_annual: float
    roi_multiple: float


class BusinessValueReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    total_annual_roi_multiple: float
    total_labor_hours_saved: float
    financial_payback_months: float
    values: List[ValueRealizationSpec] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part R: Enterprise Dataset Validation
class DatasetVerificationDetail(BaseModel):
    dataset_name: str
    sample_count: int
    formats: List[str]
    extraction_accuracy_pct: float
    verified: bool


class EnterpriseDatasetReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    total_samples_evaluated: int
    cross_format_accuracy_pct: float
    datasets: List[DatasetVerificationDetail] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part S: Workflow Scalability
class ScalabilityTierTest(BaseModel):
    concurrency_level: int
    p95_latency_sec: float
    queue_backlog_peak: int
    resource_starvation_events: int
    throughput_wps: float


class WorkflowScalabilityReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    max_tested_concurrency: int
    fair_scheduling_verified: bool
    starvation_free_verified: bool
    tiers: List[ScalabilityTierTest] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Part T: Executive Readiness
class ExecutiveReadinessPillar(BaseModel):
    pillar_title: str
    assessment: str
    readiness_score_pct: float
    executive_approved: bool


class ExecutiveReadinessReport(BaseModel):
    verifier_id: str
    name: str
    status: VerificationStatus
    score: float
    overall_executive_readiness_pct: float
    unattended_operation_certified: bool
    governance_compliance_certified: bool
    pillars: List[ExecutiveReadinessPillar] = Field(default_factory=list)
    checks: List[CheckResult] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Overall Scoring & Certification Models
class CategoryScore(BaseModel):
    name: str
    weight: float
    score: float
    weighted_score: float
    checks_total: int
    checks_passed: int
    status: VerificationStatus


class AutonomousWorkflowQualityScore(BaseModel):
    overall_score: float = Field(ge=0.0, le=100.0)
    certification_tier: CertificationTier
    verification_status: VerificationStatus
    categories: List[CategoryScore] = Field(default_factory=list)
    calculated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AutonomousWorkflowQualityReport(BaseModel):
    project_name: str = "DocuTask Agent"
    phase: str = "Phase 5 - Enterprise End-to-End Autonomous Workflow & Business Process Validation"
    execution_id: str
    status: VerificationStatus
    score: AutonomousWorkflowQualityScore
    reports: Dict[str, Any] = Field(default_factory=dict)
    summary_markdown: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
