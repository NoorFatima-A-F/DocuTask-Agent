"""
AMRS-RSIP Phase 13.9 - Meta-Reasoning Domain Events Layer
Immutable, replay-verifiable operational events for strategic observation, meta-reasoning, recursive reflection, capability discovery, policy evolution, and self-improvement cycles.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class ReflectionTier(str, Enum):
    LEVEL_1_MISSION = "LEVEL_1_MISSION"
    LEVEL_2_PLANNER = "LEVEL_2_PLANNER"
    LEVEL_3_SWARM = "LEVEL_3_SWARM"
    LEVEL_4_LEARNING = "LEVEL_4_LEARNING"
    LEVEL_5_ARCHITECTURE = "LEVEL_5_ARCHITECTURE"
    LEVEL_6_POLICY = "LEVEL_6_POLICY"
    LEVEL_7_SELF = "LEVEL_7_SELF"


class ImprovementStatus(str, Enum):
    PROPOSED = "PROPOSED"
    IN_EXPERIMENT = "IN_EXPERIMENT"
    VERIFIED = "VERIFIED"
    GOVERNANCE_PENDING = "GOVERNANCE_PENDING"
    APPROVED = "APPROVED"
    DEPLOYED = "DEPLOYED"
    ROLLED_BACK = "ROLLED_BACK"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class MetaBaseEvent:
    event_id: str = field(default_factory=lambda: f"meta-evt-{uuid.uuid4().hex[:12]}")
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_type: str = "MetaBaseEvent"
    mission_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StrategicObservationRecorded(MetaBaseEvent):
    event_type: str = "StrategicObservationRecorded"
    observation_type: str = "METRIC_ANOMALY"
    target_subsystem: str = "PLANNER"
    metric_name: str = "avg_latency_ms"
    observed_value: float = 0.0
    baseline_value: float = 0.0


@dataclass(frozen=True)
class MetaReasoningInitiated(MetaBaseEvent):
    event_type: str = "MetaReasoningInitiated"
    goal_id: str = ""
    abstraction_level: str = "SYSTEMIC"
    hypothesis_count: int = 0


@dataclass(frozen=True)
class BottleneckDetected(MetaBaseEvent):
    event_type: str = "BottleneckDetected"
    bottleneck_id: str = ""
    component: str = ""
    severity: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL
    impact_description: str = ""
    estimated_overhead_ms: float = 0.0


@dataclass(frozen=True)
class RecursiveReflectionCompleted(MetaBaseEvent):
    event_type: str = "RecursiveReflectionCompleted"
    reflection_tier: ReflectionTier = ReflectionTier.LEVEL_1_MISSION
    depth_level: int = 1
    insights_generated: int = 0
    confidence_score: float = 1.0


@dataclass(frozen=True)
class StrategicPlanGenerated(MetaBaseEvent):
    event_type: str = "StrategicPlanGenerated"
    plan_id: str = ""
    horizon_scope: str = "MULTI_HOUR"  # MULTI_HOUR, MULTI_DAY, MULTI_WEEK
    milestone_count: int = 0
    estimated_efficiency_gain_pct: float = 0.0


@dataclass(frozen=True)
class ExperimentScheduled(MetaBaseEvent):
    event_type: str = "ExperimentScheduled"
    experiment_id: str = ""
    control_strategy: str = ""
    treatment_strategy: str = ""
    sample_size: int = 10


@dataclass(frozen=True)
class ExperimentConcluded(MetaBaseEvent):
    event_type: str = "ExperimentConcluded"
    experiment_id: str = ""
    p_value: float = 0.01
    statistically_significant: bool = True
    winning_strategy: str = ""
    performance_gain_pct: float = 0.0


@dataclass(frozen=True)
class CapabilityDiscovered(MetaBaseEvent):
    event_type: str = "CapabilityDiscovered"
    capability_id: str = ""
    name: str = ""
    synthesized_from: List[str] = field(default_factory=list)
    reusability_score: float = 0.95


@dataclass(frozen=True)
class PolicyEvolutionProposed(MetaBaseEvent):
    event_type: str = "PolicyEvolutionProposed"
    proposal_id: str = ""
    policy_category: str = "RESOURCE_ALLOCATION"
    rationale: str = ""
    sha256_spec_hash: str = ""


@dataclass(frozen=True)
class ArchitectureOptimized(MetaBaseEvent):
    event_type: str = "ArchitectureOptimized"
    optimization_id: str = ""
    redundancy_removed_count: int = 0
    latency_reduction_ms: float = 0.0


@dataclass(frozen=True)
class SelfImprovementCycleCompleted(MetaBaseEvent):
    event_type: str = "SelfImprovementCycleCompleted"
    cycle_id: str = ""
    status: ImprovementStatus = ImprovementStatus.VERIFIED
    composite_gain_score: float = 0.0


@dataclass(frozen=True)
class GovernanceApproved(MetaBaseEvent):
    event_type: str = "GovernanceApproved"
    proposal_id: str = ""
    approver_id: str = "EXECUTIVE_GOVERNOR"
    signature: str = ""


@dataclass(frozen=True)
class GovernanceRejected(MetaBaseEvent):
    event_type: str = "GovernanceRejected"
    proposal_id: str = ""
    reason: str = ""


@dataclass(frozen=True)
class RollbackExecuted(MetaBaseEvent):
    event_type: str = "RollbackExecuted"
    cycle_id: str = ""
    reason: str = ""
    target_checkpoint_hash: str = ""
