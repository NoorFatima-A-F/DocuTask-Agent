"""
Phase 3H.4.9: Enterprise Incident Recovery Verification Framework - Domain Models
"""
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class RecoveryState(str, Enum):
    RECOVERY_REQUIRED = "RECOVERY_REQUIRED"
    RECOVERY_PLANNING = "RECOVERY_PLANNING"
    RECOVERY_EXECUTING = "RECOVERY_EXECUTING"
    RECOVERY_VALIDATING = "RECOVERY_VALIDATING"
    SERVICE_RESTORED = "SERVICE_RESTORED"
    POST_RECOVERY_ANALYSIS = "POST_RECOVERY_ANALYSIS"
    RECOVERY_FAILED = "RECOVERY_FAILED"
    ROLLED_BACK = "ROLLED_BACK"


class RecoveryTier(str, Enum):
    ENTERPRISE_RECOVERY_READY = "Enterprise Recovery Ready"
    PRODUCTION_RECOVERY_READY = "Production Recovery Ready"
    IMPROVEMENT_REQUIRED = "Improvement Required"
    FAILED = "Failed"


class IncidentType(str, Enum):
    DATABASE_OUTAGE = "DATABASE_OUTAGE"
    REDIS_QUEUE_FAILURE = "REDIS_QUEUE_FAILURE"
    WORKER_POOL_CRASH = "WORKER_POOL_CRASH"
    STORAGE_OUTAGE = "STORAGE_OUTAGE"
    AI_PROVIDER_DEGRADATION = "AI_PROVIDER_DEGRADATION"
    API_SERVICE_LATENCY = "API_SERVICE_LATENCY"


class RecoveryActionStep(BaseModel):
    step_number: int
    name: str
    description: str
    command_or_rpc: str
    timeout_seconds: float = 30.0
    is_idempotent: bool = True
    rollback_step: Optional[str] = None
    executed: bool = False
    success: bool = False
    duration_ms: float = 0.0
    error_message: Optional[str] = None


class RecoveryPlan(BaseModel):
    plan_id: str
    incident_id: str
    incident_type: IncidentType
    target_component: str
    steps: List[RecoveryActionStep] = Field(default_factory=list)
    rollback_supported: bool = True
    requires_human_approval: bool = False
    safety_guardrails_passed: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RecoveryExecutionResult(BaseModel):
    execution_id: str
    incident_id: str
    plan_id: str
    state: RecoveryState
    steps_executed: int
    total_steps: int
    all_steps_succeeded: bool
    total_duration_ms: float
    retry_count: int = 0
    escalated_to_human: bool = False
    error: Optional[str] = None
    completed_at: datetime = Field(default_factory=datetime.utcnow)


class DependencyHealthCheck(BaseModel):
    dependency_name: str
    status: str
    latency_ms: float
    healthy: bool


class ApplicationFunctionalTestResult(BaseModel):
    test_name: str
    document_id: str
    upload_success: bool
    processing_success: bool
    extraction_success: bool
    duration_ms: float
    extracted_text_preview: str
    all_passed: bool


class HealthValidationReport(BaseModel):
    validation_id: str
    liveness_status: str
    liveness_passed: bool
    readiness_status: str
    readiness_passed: bool
    dependency_checks: List[DependencyHealthCheck] = Field(default_factory=list)
    functional_test: ApplicationFunctionalTestResult
    overall_health_validated: bool
    validation_timestamp: datetime = Field(default_factory=datetime.utcnow)


class RecoveryMetricsReport(BaseModel):
    mttd_seconds: float
    mtta_seconds: float
    mttr_seconds: float
    total_recovery_attempts: int
    successful_recoveries: int
    failed_recoveries: int
    recovery_success_rate: float
    target_mttr_met: bool


class FailureSimulationResult(BaseModel):
    scenario_name: str
    component_targeted: str
    failure_injected: str
    detection_verified: bool
    alert_triggered: bool
    recovery_executed: bool
    health_validated: bool
    total_downtime_seconds: float
    recovery_success: bool


class DataIntegrityReport(BaseModel):
    database_transactions_consistent: bool
    partial_writes_detected: int = 0
    queue_jobs_lost: int = 0
    queue_duplicate_executions: int = 0
    original_document_sha256: str
    recovered_document_sha256: str
    checksum_match: bool
    data_loss_prevented: bool


class RollbackVerificationReport(BaseModel):
    scenario: str
    original_version: str
    failed_target_version: str
    rollback_triggered_automatically: bool
    rollback_duration_ms: float
    configuration_restored: bool
    database_compatibility_preserved: bool
    service_restored_after_rollback: bool
    rollback_successful: bool


class RecoverySafetyReport(BaseModel):
    max_retries_enforced: bool
    restart_loop_prevented: bool
    destructive_operations_blocked: bool
    guardrails_active: bool
    escalation_on_exhaustion_verified: bool
    overall_safety_passed: bool


class PostmortemActionItem(BaseModel):
    action_id: str
    title: str
    category: str
    assigned_team: str
    priority: str
    jira_ticket: str


class PostIncidentImprovementReport(BaseModel):
    incident_id: str
    root_cause_summary: str
    timeline_events: List[Dict[str, Any]] = Field(default_factory=list)
    impact_summary: str
    detection_quality_score: float
    recovery_quality_score: float
    lessons_learned: List[str] = Field(default_factory=list)
    preventive_actions: List[PostmortemActionItem] = Field(default_factory=list)


class RecoveryScorecard(BaseModel):
    recovery_success_rate_score: float = Field(..., ge=0.0, le=100.0)
    recovery_speed_score: float = Field(..., ge=0.0, le=100.0)
    data_integrity_score: float = Field(..., ge=0.0, le=100.0)
    automation_safety_score: float = Field(..., ge=0.0, le=100.0)
    validation_quality_score: float = Field(..., ge=0.0, le=100.0)
    improvement_process_score: float = Field(..., ge=0.0, le=100.0)
    composite_score: float = Field(..., ge=0.0, le=100.0)
    tier: RecoveryTier
    certified_enterprise_ready: bool
