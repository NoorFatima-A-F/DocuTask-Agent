"""
Phase 3H.5.6: Enterprise Failure Learning, Root Cause Analysis & Recovery Optimization - Domain Models
"""
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class FailureSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AutonomyLevel(str, Enum):
    FULLY_AUTOMATIC = "fully_automatic"
    APPROVAL_REQUIRED = "approval_required"
    MANUAL_ONLY = "manual_only"


class KnowledgeCategory(str, Enum):
    INFRASTRUCTURE = "infrastructure_failures"
    APPLICATION = "application_failures"
    AI_PIPELINE = "ai_failures"
    DEPENDENCY = "dependency_failures"
    SECURITY = "security_failures"


class IntelligenceTier(str, Enum):
    ADAPTIVE_RELIABILITY_INTELLIGENCE_READY = "Adaptive Reliability Intelligence Ready"
    ADVANCED_SELF_HEALING_READY = "Advanced Self-Healing Ready"
    IMPROVEMENT_REQUIRED = "Improvement Required"
    FAILED = "Failed"


class FailureEvent(BaseModel):
    id: str
    component: str
    failure_type: str
    severity: FailureSeverity
    timestamp: str
    metrics_snapshot: Dict[str, Any]
    logs: List[str]
    recovery_action: str
    recovery_duration_ms: float
    recovery_succeeded: bool


class FailureEventReport(BaseModel):
    report_title: str = "Failure Event Collection Report"
    total_events_collected: int
    categories_monitored: List[str]
    events: List[FailureEvent] = Field(default_factory=list)
    collection_pipeline_healthy: bool


class RCARecord(BaseModel):
    incident_id: str
    component: str
    symptom: str
    temporal_correlation: str
    dependency_correlation: str
    resource_correlation: str
    identified_root_cause: str
    confidence_score: float  # e.g., 0.98 (98%)
    rca_status: str = "CONFIRMED"


class RootCauseReport(BaseModel):
    report_title: str = "Root Cause Analysis Report"
    total_incidents_analyzed: int
    rca_records: List[RCARecord] = Field(default_factory=list)
    mean_rca_accuracy_pct: float
    rca_pipeline_valid: bool


class FailurePatternItem(BaseModel):
    pattern_id: str
    pattern_name: str
    component: str
    frequency_count: int
    increasing_frequency_detected: bool
    hidden_degradation_detected: bool
    impact_level: str
    last_seen_timestamp: str


class PatternAnalysisReport(BaseModel):
    report_title: str = "Failure Pattern Recognition Report"
    total_patterns_detected: int
    patterns: List[FailurePatternItem] = Field(default_factory=list)
    repeated_patterns_identified: int
    pattern_recognition_accuracy_pct: float


class IncidentKnowledgeItem(BaseModel):
    knowledge_id: str
    incident_type: str
    category: KnowledgeCategory
    root_cause: str
    successful_recovery: str
    prevention_strategy: str
    times_applied: int = 1
    effectiveness_pct: float = 100.0


class KnowledgeBaseReport(BaseModel):
    report_title: str = "Incident Knowledge Base Report"
    total_knowledge_articles: int
    categories_covered: List[str]
    knowledge_items: List[IncidentKnowledgeItem] = Field(default_factory=list)
    retention_and_retrieval_healthy: bool


class RecoveryOptimizationItem(BaseModel):
    scenario: str
    component: str
    previous_strategy: str
    previous_mttr_seconds: float
    optimized_strategy: str
    optimized_mttr_seconds: float
    mttr_reduction_pct: float
    cost_and_overhead_reduction: str


class RecoveryOptimizationReport(BaseModel):
    report_title: str = "Recovery Optimization Report"
    total_optimizations_evaluated: int
    optimizations: List[RecoveryOptimizationItem] = Field(default_factory=list)
    average_mttr_reduction_pct: float
    recovery_success_rate_pct: float


class PolicyComparisonItem(BaseModel):
    policy_id: str
    component: str
    trigger_condition: str
    legacy_action: str
    improved_action: str
    retry_limit: int
    circuit_breaker_enabled: bool
    safety_validated: bool
    rollback_supported: bool


class PolicyImprovementReport(BaseModel):
    report_title: str = "Self-Healing Policy Improvement Report"
    total_policies_refined: int
    policy_updates: List[PolicyComparisonItem] = Field(default_factory=list)
    all_policies_safety_approved: bool


class PreventionSignalItem(BaseModel):
    signal_id: str
    target_component: str
    early_warning_trigger: str
    predicted_failure_risk: str
    proactive_action_executed: str
    failure_prevented: bool


class FailurePreventionReport(BaseModel):
    report_title: str = "Failure Prevention Verification Report"
    total_early_warnings_evaluated: int
    prevention_signals: List[PreventionSignalItem] = Field(default_factory=list)
    prevention_rate_pct: float
    early_detection_successful: bool


class AutonomyMatrixItem(BaseModel):
    action_name: str
    target_subsystem: str
    autonomy_level: AutonomyLevel
    rationale: str
    risk_tier: str


class AutonomyMatrixReport(BaseModel):
    report_title: str = "Human-in-the-Loop Autonomy Level Matrix"
    matrix_entries: List[AutonomyMatrixItem] = Field(default_factory=list)
    safety_governance_enforced: bool


class ScenarioSimulationResult(BaseModel):
    scenario_id: str
    scenario_name: str
    injected_failure: str
    pattern_detected: bool
    rca_identified: str
    knowledge_extracted: bool
    policy_adapted: bool
    simulation_passed: bool


class SimulationReport(BaseModel):
    report_title: str = "Failure Simulation & Learning Test Report"
    total_scenarios_simulated: int
    results: List[ScenarioSimulationResult] = Field(default_factory=list)
    all_scenarios_passed: bool


class ReliabilityMetrics(BaseModel):
    mttr_seconds: float
    mttd_seconds: float
    failure_recurrence_rate_pct: float
    recovery_success_rate_pct: float
    prevention_rate_pct: float


class FailureLearningScorecard(BaseModel):
    failure_analysis_accuracy: float = Field(..., ge=0.0, le=100.0)
    root_cause_score: float = Field(..., ge=0.0, le=100.0)
    knowledge_retention_score: float = Field(..., ge=0.0, le=100.0)
    recovery_optimization_score: float = Field(..., ge=0.0, le=100.0)
    prevention_capability_score: float = Field(..., ge=0.0, le=100.0)
    safety_controls_score: float = Field(..., ge=0.0, le=100.0)
    composite_score: float = Field(..., ge=0.0, le=100.0)
    tier: IntelligenceTier
    certified_enterprise_ready: bool
