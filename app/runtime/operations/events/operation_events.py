"""
AOIS-HROP Phase 13.7 - Domain Events Layer
Immutable, replay-verifiable operational events for autonomous health, incidents, diagnostics, healing, recovery, and resilience.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class OperationalSeverity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IncidentStatus(str, Enum):
    DETECTED = "DETECTED"
    CORRELATED = "CORRELATED"
    DIAGNOSING = "DIAGNOSING"
    HEALING = "HEALING"
    RESOLVED = "RESOLVED"
    ESCALATED = "ESCALATED"


class HealingActionType(str, Enum):
    WORKER_RESTART = "WORKER_RESTART"
    WORKER_REPLACE = "WORKER_REPLACE"
    PLANNER_REPLAN = "PLANNER_REPLAN"
    PLANNER_ROLLBACK = "PLANNER_ROLLBACK"
    RESOURCE_REALLOCATE = "RESOURCE_REALLOCATE"
    MEMORY_REPAIR = "MEMORY_REPAIR"
    CONCURRENCY_ADJUST = "CONCURRENCY_ADJUST"
    CIRCUIT_BREAKER_TRIGGER = "CIRCUIT_BREAKER_TRIGGER"
    FALLBACK_MODEL_ENGAGE = "FALLBACK_MODEL_ENGAGE"


class SubsystemType(str, Enum):
    PLANNER = "PLANNER"
    WORKERS = "WORKERS"
    MEMORY = "MEMORY"
    OPTIMIZATION = "OPTIMIZATION"
    REPLAY = "REPLAY"
    LEARNING = "LEARNING"
    TRUTH = "TRUTH"
    TELEMETRY = "TELEMETRY"
    API = "API"
    DATABASE = "DATABASE"


@dataclass(frozen=True)
class OperationalBaseEvent:
    event_id: str = field(default_factory=lambda: f"op-evt-{uuid.uuid4().hex[:12]}")
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_type: str = "OperationalBaseEvent"
    subsystem: SubsystemType = SubsystemType.PLANNER
    mission_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RuntimeHeartbeatReceived(OperationalBaseEvent):
    event_type: str = "RuntimeHeartbeatReceived"
    heartbeat_seq: int = 0
    active_workers: int = 0
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    queue_depth: int = 0
    latency_p95_ms: float = 0.0


@dataclass(frozen=True)
class HealthEvaluated(OperationalBaseEvent):
    event_type: str = "HealthEvaluated"
    composite_score: float = 100.0  # 0 - 100
    subsystem_scores: Dict[str, float] = field(default_factory=dict)
    health_status: str = "HEALTHY"


@dataclass(frozen=True)
class HealthDegraded(OperationalBaseEvent):
    event_type: str = "HealthDegraded"
    previous_score: float = 100.0
    current_score: float = 0.0
    degradation_reason: str = ""
    degraded_components: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class IncidentDetected(OperationalBaseEvent):
    event_type: str = "IncidentDetected"
    incident_id: str = ""
    title: str = ""
    severity: OperationalSeverity = OperationalSeverity.MEDIUM
    error_code: str = ""
    affected_nodes: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class IncidentEscalated(OperationalBaseEvent):
    event_type: str = "IncidentEscalated"
    incident_id: str = ""
    previous_severity: OperationalSeverity = OperationalSeverity.MEDIUM
    new_severity: OperationalSeverity = OperationalSeverity.CRITICAL
    escalation_reason: str = ""


@dataclass(frozen=True)
class IncidentResolved(OperationalBaseEvent):
    event_type: str = "IncidentResolved"
    incident_id: str = ""
    resolution_summary: str = ""
    healing_duration_ms: float = 0.0
    verified_by: str = "AUTOMATED_HEALER"


@dataclass(frozen=True)
class DiagnosisCompleted(OperationalBaseEvent):
    event_type: str = "DiagnosisCompleted"
    incident_id: str = ""
    root_cause: str = ""
    confidence: float = 0.0
    causal_chain: List[str] = field(default_factory=list)
    recommended_action: HealingActionType = HealingActionType.WORKER_RESTART


@dataclass(frozen=True)
class HealingStarted(OperationalBaseEvent):
    event_type: str = "HealingStarted"
    healing_id: str = ""
    incident_id: str = ""
    action_type: HealingActionType = HealingActionType.WORKER_RESTART
    target_resource: str = ""


@dataclass(frozen=True)
class HealingCompleted(OperationalBaseEvent):
    event_type: str = "HealingCompleted"
    healing_id: str = ""
    incident_id: str = ""
    action_type: HealingActionType = HealingActionType.WORKER_RESTART
    success: bool = True
    recovery_time_ms: float = 0.0
    verification_hash: str = ""


@dataclass(frozen=True)
class RecoveryStarted(OperationalBaseEvent):
    event_type: str = "RecoveryStarted"
    recovery_id: str = ""
    checkpoint_id: Optional[str] = None
    target_mission_id: str = ""
    recovery_mode: str = "SNAPSHOT_ROLLBACK"


@dataclass(frozen=True)
class RecoveryCompleted(OperationalBaseEvent):
    event_type: str = "RecoveryCompleted"
    recovery_id: str = ""
    target_mission_id: str = ""
    restored_state_hash: str = ""
    elapsed_ms: float = 0.0


@dataclass(frozen=True)
class RecoveryFailed(OperationalBaseEvent):
    event_type: str = "RecoveryFailed"
    recovery_id: str = ""
    target_mission_id: str = ""
    failure_reason: str = ""
    fallback_engaged: bool = True


@dataclass(frozen=True)
class ChaosExperimentStarted(OperationalBaseEvent):
    event_type: str = "ChaosExperimentStarted"
    experiment_id: str = ""
    experiment_name: str = ""
    fault_type: str = "NETWORK_LATENCY_INJECTION"
    target_subsystem: str = ""


@dataclass(frozen=True)
class ChaosExperimentCompleted(OperationalBaseEvent):
    event_type: str = "ChaosExperimentCompleted"
    experiment_id: str = ""
    invariants_preserved: bool = True
    mttr_ms: float = 0.0
    resilience_passed: bool = True


@dataclass(frozen=True)
class ResilienceScoreCalculated(OperationalBaseEvent):
    event_type: str = "ResilienceScoreCalculated"
    resilience_score: float = 98.5  # 0 - 100
    mttr_seconds: float = 1.2
    mtbf_hours: float = 720.0
    availability_percentage: float = 99.99


@dataclass(frozen=True)
class FailurePredicted(OperationalBaseEvent):
    event_type: str = "FailurePredicted"
    prediction_id: str = ""
    predicted_failure_type: str = "CAPACITY_EXHAUSTION"
    probability: float = 0.85
    time_to_failure_sec: float = 120.0
    preventative_action: str = "SPAWN_BURST_WORKER"


@dataclass(frozen=True)
class RiskForecastGenerated(OperationalBaseEvent):
    event_type: str = "RiskForecastGenerated"
    composite_risk_index: float = 0.12  # 0.0 (low) - 1.0 (critical)
    financial_exposure_usd: float = 0.0
    sla_violation_probability: float = 0.01


@dataclass(frozen=True)
class AvailabilityUpdated(OperationalBaseEvent):
    event_type: str = "AvailabilityUpdated"
    window_days: int = 30
    availability_ratio: float = 0.9999
    unplanned_downtime_sec: float = 0.0


@dataclass(frozen=True)
class OperationalAuditGenerated(OperationalBaseEvent):
    event_type: str = "OperationalAuditGenerated"
    audit_id: str = ""
    frameworks_verified: List[str] = field(default_factory=lambda: ["SOC2", "ISO27001", "ISO42001", "NIST_AI_RMF"])
    compliance_score: float = 100.0
    merkle_root: str = ""


@dataclass(frozen=True)
class RuntimeRecovered(OperationalBaseEvent):
    event_type: str = "RuntimeRecovered"
    downtime_duration_ms: float = 0.0
    restored_invariants_count: int = 0
    state_verified: bool = True
