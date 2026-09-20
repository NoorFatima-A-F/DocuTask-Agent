"""
Phase 3H.5.5: Enterprise Health Self-Healing & Automated Recovery Framework - Domain Models
"""
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class FailureCategory(str, Enum):
    INFRASTRUCTURE = "Infrastructure"
    APPLICATION = "Application"
    DEPENDENCY = "Dependency"
    AI_PIPELINE = "AI Pipeline"


class RecoveryStrategyType(str, Enum):
    RESTART = "Restart"
    RETRY = "Retry"
    FAILOVER = "Failover"
    DEGRADATION = "Degradation"


class SelfHealingTier(str, Enum):
    AUTONOMOUS_RECOVERY_READY = "Autonomous Recovery Ready"
    PRODUCTION_RECOVERY_READY = "Production Recovery Ready"
    IMPROVEMENT_REQUIRED = "Improvement Required"
    FAILED = "Failed"


class FailureClassificationItem(BaseModel):
    failure_name: str
    category: FailureCategory
    root_cause_type: str
    severity: str
    recommended_strategy: RecoveryStrategyType
    classified_correctly: bool


class FailureClassificationReport(BaseModel):
    total_failures_classified: int
    categories_covered: List[str]
    classifications: List[FailureClassificationItem] = Field(default_factory=list)
    accuracy_percentage: float
    is_classification_valid: bool


class RecoveryPolicyRule(BaseModel):
    rule_id: str
    component: str
    failure_condition: str
    strategy: RecoveryStrategyType
    action_type: str
    severity: str
    max_retries: int
    circuit_breaker_active: bool


class RecoveryPolicyReport(BaseModel):
    total_policies_defined: int
    policies: List[RecoveryPolicyRule] = Field(default_factory=list)
    all_policies_valid: bool


class RecoveryExecutionOutcome(BaseModel):
    scenario: str
    target_component: str
    strategy_executed: RecoveryStrategyType
    execution_duration_ms: float
    action_succeeded: bool
    final_service_state: str


class RecoveryExecutionReport(BaseModel):
    total_executions_tested: int
    successful_executions: int
    execution_success_rate: float
    outcomes: List[RecoveryExecutionOutcome] = Field(default_factory=list)
    execution_verification_passed: bool


class HealthRecoveryReport(BaseModel):
    layer_name: str = "Layer 1 - Service Health Validation"
    liveness_status: str
    liveness_passed: bool
    readiness_status: str
    readiness_passed: bool
    all_health_passed: bool
    validation_timestamp: str


class DependencyItemHealth(BaseModel):
    name: str
    connection_healthy: bool
    query_or_ping_healthy: bool
    transaction_or_job_healthy: bool
    latency_ms: float
    status: str


class DependencyRestoreReport(BaseModel):
    layer_name: str = "Layer 2 - Dependency Restoration Validation"
    total_dependencies: int
    all_restored: bool
    dependencies: List[DependencyItemHealth] = Field(default_factory=list)


class WorkflowStepResult(BaseModel):
    step_name: str
    duration_ms: float
    success: bool


class WorkflowValidationReport(BaseModel):
    layer_name: str = "Layer 3 - Functional Document Workflow Recovery"
    document_id: str
    workflow_stages: List[WorkflowStepResult] = Field(default_factory=list)
    total_duration_ms: float
    extraction_verified: bool
    database_saved: bool
    business_workflow_passed: bool


class PerformanceRecoveryReport(BaseModel):
    layer_name: str = "Layer 4 - Performance Recovery Test"
    baseline_latency_ms: float
    recovered_latency_ms: float
    recovery_performance_ratio: float
    acceptable_threshold_ratio: float = 1.20  # <= 120% baseline
    performance_restored: bool


class StabilityWindowReport(BaseModel):
    layer_name: str = "Layer 5 - Stability Window Monitoring"
    window_5m_stable: bool
    window_30m_stable: bool
    window_1h_stable: bool
    repeated_crashes_detected: int = 0
    memory_leaks_detected: bool = False
    error_spikes_detected: bool = False
    queue_backlog_stable: bool = True
    overall_stability_passed: bool


class RecoveryValidationReport(BaseModel):
    validation_id: str
    layer1_health: HealthRecoveryReport
    layer2_dependency: DependencyRestoreReport
    layer3_workflow: WorkflowValidationReport
    layer4_performance: PerformanceRecoveryReport
    layer5_stability: StabilityWindowReport
    all_5_layers_passed: bool
    recovery_accepted: bool


class SelfHealingScorecard(BaseModel):
    recovery_detection_score: float = Field(..., ge=0.0, le=100.0)
    recovery_execution_score: float = Field(..., ge=0.0, le=100.0)
    validation_accuracy_score: float = Field(..., ge=0.0, le=100.0)
    business_workflow_recovery_score: float = Field(..., ge=0.0, le=100.0)
    evidence_quality_score: float = Field(..., ge=0.0, le=100.0)
    security_controls_score: float = Field(..., ge=0.0, le=100.0)
    composite_score: float = Field(..., ge=0.0, le=100.0)
    tier: SelfHealingTier
    certified_enterprise_ready: bool
