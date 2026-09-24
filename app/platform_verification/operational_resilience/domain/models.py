"""
Phase 3H.7: Enterprise Operational Resilience, Fault Tolerance & Self-Healing — Domain Models
"""
from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class CircuitBreakerState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class DegradationMode(str, Enum):
    FULL_OPERATION = "FULL_OPERATION"
    DB_READ_ONLY = "DB_READ_ONLY"
    AI_FALLBACK_CACHED = "AI_FALLBACK_CACHED"
    AI_OFFLINE_BUFFERED = "AI_OFFLINE_BUFFERED"
    OCR_NATIVE_PDF_FALLBACK = "OCR_NATIVE_PDF_FALLBACK"


class OperationalResilienceTier(str, Enum):
    ENTERPRISE_AUTONOMOUS_RESILIENCE = "Enterprise Autonomous Resilience"  # 98 - 100
    ENTERPRISE_RESILIENT = "Enterprise Resilient"                          # 95 - 97.99
    PRODUCTION_RESILIENT = "Production Resilient"                          # 90 - 94.99
    NEEDS_IMPROVEMENT = "Needs Improvement"                                # 80 - 89.99
    FAILED = "Failed"                                                      # < 80


# ─── 3H.7.1: Resilience Architecture Models ─────────────────────────────────

class ResilienceStrategyDefinition(BaseModel):
    strategy_id: str
    name: str
    purpose: str
    activation_condition: str
    dependencies: List[str] = Field(default_factory=list)
    recovery_action: str
    exit_condition: str
    observability_hooks: List[str] = Field(default_factory=list)
    automation_policy: str
    is_active: bool = True


class ResilienceArchitectureReport(BaseModel):
    report_title: str = "Enterprise Resilience Architecture & Strategy Specification Report"
    total_strategies_defined: int = 0
    strategies: List[ResilienceStrategyDefinition] = Field(default_factory=list)
    architecture_certified: bool = True


# ─── 3H.7.2: Circuit Breaker Models ─────────────────────────────────────────

class CircuitBreakerEvaluation(BaseModel):
    subsystem: str  # Gemini_AI, OCR_Engine, PostgreSQL, Redis, External_Webhooks
    state: CircuitBreakerState = CircuitBreakerState.CLOSED
    failure_rate_threshold_pct: float = 50.0
    trip_consecutive_failures: int = 5
    timeout_window_seconds: int = 30
    half_open_probe_requests: int = 3
    tripped_count: int = 0
    auto_reset_verified: bool = True
    is_operational: bool = True


class CircuitBreakerReport(BaseModel):
    report_title: str = "Enterprise Circuit Breaker Protection Report"
    total_circuit_breakers: int = 0
    breakers: List[CircuitBreakerEvaluation] = Field(default_factory=list)
    all_circuit_breakers_active: bool = True


# ─── 3H.7.3: Retry & Backoff Strategy Models ────────────────────────────────

class RetryPolicyEvaluation(BaseModel):
    operation_type: str  # DB_Query, Redis_Enqueue, LLM_Inference, OCR_Page, Storage_Upload
    max_retries: int = 3
    initial_backoff_ms: int = 200
    max_backoff_ms: int = 5000
    backoff_multiplier: float = 2.0
    jitter_applied: bool = True
    retry_budget_enforced: bool = True
    dlq_routing_verified: bool = True
    is_idempotent: bool = True


class RetryStrategyReport(BaseModel):
    report_title: str = "Bounded Exponential Backoff & Retry Strategy Report"
    total_retry_policies: int = 0
    policies: List[RetryPolicyEvaluation] = Field(default_factory=list)
    retry_governance_compliant: bool = True


# ─── 3H.7.4: Graceful Degradation Models ─────────────────────────────────────

class DegradationScenario(BaseModel):
    subsystem_failure: str
    degraded_mode: DegradationMode
    retained_functionality: str
    user_messaging_sanitized: bool = True
    audit_trail_recorded: bool = True
    recovery_transition_automatic: bool = True
    is_resilient: bool = True


class GracefulDegradationReport(BaseModel):
    report_title: str = "Graceful Degradation & Fallback Strategy Report"
    total_degradation_modes: int = 0
    scenarios: List[DegradationScenario] = Field(default_factory=list)
    graceful_degradation_verified: bool = True


# ─── 3H.7.5: Bulkhead Isolation Models ──────────────────────────────────────

class BulkheadIsolationPool(BaseModel):
    pool_name: str  # Ingress_Pool, OCR_Pool, AI_Inference_Pool, Validation_Pool, Export_Pool
    max_threads_or_workers: int
    queue_capacity: int
    isolated_from_other_pools: bool = True
    saturation_contained: bool = True


class BulkheadReport(BaseModel):
    report_title: str = "Bulkhead Resource Isolation & Fault Containment Report"
    total_isolated_pools: int = 0
    pools: List[BulkheadIsolationPool] = Field(default_factory=list)
    fault_containment_verified: bool = True


# ─── 3H.7.6: Adaptive Load Shedding Models ───────────────────────────────────

class LoadSheddingDecision(BaseModel):
    traffic_priority_level: str  # Critical Document Ingestion, Interactive Status Probe, Background Batch OCR, Telemetry Export
    decision_under_stress: str  # ACCEPTED, THROTTLED, DROPPED_GRACEFULLY
    admission_control_active: bool = True
    critical_path_preserved: bool = True


class LoadSheddingReport(BaseModel):
    report_title: str = "Adaptive Load Shedding & Overload Protection Report"
    cpu_pressure_threshold_pct: float = 85.0
    memory_pressure_threshold_pct: float = 90.0
    decisions: List[LoadSheddingDecision] = Field(default_factory=list)
    overload_protection_active: bool = True


# ─── 3H.7.7: Self-Healing & Stale Lock Models ────────────────────────────────

class SelfHealingScenarioItem(BaseModel):
    recovery_type: str  # Worker Restart, Redis Sentinel Reconnect, DB Pool Recycle, Stale Lock Eviction, Orphan Task Recovery
    trigger_event: str
    automated_resolution: str
    resolution_latency_seconds: float
    verification_passed: bool = True


class SelfHealingReport(BaseModel):
    report_title: str = "Automated Self-Healing & State Recovery Report"
    total_scenarios_verified: int = 0
    scenarios: List[SelfHealingScenarioItem] = Field(default_factory=list)
    stale_lock_cleanup_active: bool = True
    orphan_task_recovery_active: bool = True
    zero_manual_intervention_required: bool = True


# ─── 3H.7.8: Chaos Resilience Models ─────────────────────────────────────────

class ChaosFaultExperiment(BaseModel):
    experiment_id: str
    fault_type: str  # Network Latency (500ms), DNS Failure, Worker SIGKILL, DB Abrupt Reset, Redis Partition, AI Timeout (10s)
    service_continuity_maintained: bool = True
    degraded_mode_activated: bool = True
    recovery_duration_seconds: float
    zero_data_loss_verified: bool = True


class ChaosResilienceReport(BaseModel):
    report_title: str = "Chaos Engineering & Fault Injection Resilience Report"
    total_chaos_experiments: int = 0
    passed_experiments_count: int = 0
    experiments: List[ChaosFaultExperiment] = Field(default_factory=list)
    chaos_resilience_certified: bool = True


# ─── 3H.7.9: Business Continuity Models ─────────────────────────────────────

class BusinessContinuityCheck(BaseModel):
    workflow_stage: str  # Document Ingestion, Queue Buffering, Async Extraction, Final Artifact Storage
    documents_preserved_during_outage: bool = True
    offline_buffering_active: bool = True
    resumable_after_reconnection: bool = True
    operator_reconciliation_available: bool = True


class BusinessContinuityReport(BaseModel):
    report_title: str = "Business Continuity & Workflow Preservation Report"
    total_stages_audited: int = 0
    checks: List[BusinessContinuityCheck] = Field(default_factory=list)
    zero_document_loss_guaranteed: bool = True


# ─── 3H.7.10: Resilience Metrics Models ──────────────────────────────────────

class ResilienceMetricItem(BaseModel):
    metric_name: str
    metric_type: str
    value: float
    unit: str
    description: str


class ResilienceMetricsReport(BaseModel):
    report_title: str = "Resilience Observability & Continuous Telemetry Report"
    metrics: List[ResilienceMetricItem] = Field(default_factory=list)
    telemetry_pipeline_operational: bool = True


# ─── 3H.7.11: Master Certification Scorecard Models ─────────────────────────

class OperationalResiliencePillarScore(BaseModel):
    pillar_name: str
    weight: float
    raw_score: float
    weighted_score: float
    status: str
    details: str = ""


class OperationalResilienceScorecard(BaseModel):
    verification_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    overall_resilience_score: float = 0.0
    certification_tier: OperationalResilienceTier = OperationalResilienceTier.FAILED
    passed: bool = False
    pillar_scores: List[OperationalResiliencePillarScore] = Field(default_factory=list)
    automatic_recovery_rate_pct: float = 100.0
    business_continuity_guaranteed: bool = True
