"""
AWM-PSDTIP Phase 13.10 - World Domain Events & State Machine
Immutable domain events and typing for the Autonomous World Modeling, Predictive Simulation & Digital Twin Intelligence Platform.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class RiskLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NEGLIGIBLE = "NEGLIGIBLE"


class HorizonScope(str, Enum):
    SHORT_TERM = "SHORT_TERM"      # Next 5-30 minutes / Next task
    MEDIUM_TERM = "MEDIUM_TERM"    # Next 1-24 hours / Next mission batch
    LONG_TERM = "LONG_TERM"        # Next 1-7 days / Cross-mission roadmap


class ScenarioType(str, Enum):
    BASELINE = "BASELINE"
    BURST_TRAFFIC = "BURST_TRAFFIC"
    RESOURCE_DEGRADATION = "RESOURCE_DEGRADATION"
    POLICY_MUTATION = "POLICY_MUTATION"
    SWARM_SCALING = "SWARM_SCALING"
    CHAOS_FAULT = "CHAOS_FAULT"


class CausalRelationType(str, Enum):
    DIRECT_CAUSE = "DIRECT_CAUSE"
    INDIRECT_CAUSE = "INDIRECT_CAUSE"
    CONFOUNDING = "CONFOUNDING"
    MEDIATING = "MEDIATING"
    CORRELATION_ONLY = "CORRELATION_ONLY"


class SimulationMode(str, Enum):
    DETERMINISTIC_REPLAY = "DETERMINISTIC_REPLAY"
    MONTE_CARLO = "MONTE_CARLO"
    COUNTERFACTUAL_BRANCH = "COUNTERFACTUAL_BRANCH"
    STRESS_TEST = "STRESS_TEST"


class PredictionStatus(str, Enum):
    PENDING = "PENDING"
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"


@dataclass(frozen=True)
class WorldDomainEvent:
    event_id: str = field(default_factory=lambda: f"wde-{uuid.uuid4().hex[:8]}")
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_type: str = "WorldDomainEvent"
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class WorldModelUpdated(WorldDomainEvent):
    event_type: str = "WorldModelUpdated"


@dataclass(frozen=True)
class DigitalTwinCreated(WorldDomainEvent):
    event_type: str = "DigitalTwinCreated"


@dataclass(frozen=True)
class PredictionStarted(WorldDomainEvent):
    event_type: str = "PredictionStarted"


@dataclass(frozen=True)
class PredictionCompleted(WorldDomainEvent):
    event_type: str = "PredictionCompleted"


@dataclass(frozen=True)
class ScenarioGenerated(WorldDomainEvent):
    event_type: str = "ScenarioGenerated"


@dataclass(frozen=True)
class ScenarioEvaluated(WorldDomainEvent):
    event_type: str = "ScenarioEvaluated"


@dataclass(frozen=True)
class CounterfactualCreated(WorldDomainEvent):
    event_type: str = "CounterfactualCreated"


@dataclass(frozen=True)
class CounterfactualRejected(WorldDomainEvent):
    event_type: str = "CounterfactualRejected"


@dataclass(frozen=True)
class RiskForecastGenerated(WorldDomainEvent):
    event_type: str = "RiskForecastGenerated"


@dataclass(frozen=True)
class FailureForecastGenerated(WorldDomainEvent):
    event_type: str = "FailureForecastGenerated"


@dataclass(frozen=True)
class OpportunityDetected(WorldDomainEvent):
    event_type: str = "OpportunityDetected"


@dataclass(frozen=True)
class CausalRelationshipLearned(WorldDomainEvent):
    event_type: str = "CausalRelationshipLearned"


@dataclass(frozen=True)
class BayesianBeliefUpdated(WorldDomainEvent):
    event_type: str = "BayesianBeliefUpdated"


@dataclass(frozen=True)
class TemporalGraphExpanded(WorldDomainEvent):
    event_type: str = "TemporalGraphExpanded"


@dataclass(frozen=True)
class SimulationStarted(WorldDomainEvent):
    event_type: str = "SimulationStarted"


@dataclass(frozen=True)
class SimulationCompleted(WorldDomainEvent):
    event_type: str = "SimulationCompleted"


@dataclass(frozen=True)
class FutureReplayGenerated(WorldDomainEvent):
    event_type: str = "FutureReplayGenerated"


@dataclass(frozen=True)
class ConfidenceIntervalCalculated(WorldDomainEvent):
    event_type: str = "ConfidenceIntervalCalculated"


@dataclass(frozen=True)
class PlanningForecastCompleted(WorldDomainEvent):
    event_type: str = "PlanningForecastCompleted"


@dataclass(frozen=True)
class PredictionValidated(WorldDomainEvent):
    event_type: str = "PredictionValidated"


@dataclass(frozen=True)
class PredictionRejected(WorldDomainEvent):
    event_type: str = "PredictionRejected"


@dataclass(frozen=True)
class GovernanceApprovedPrediction(WorldDomainEvent):
    event_type: str = "GovernanceApprovedPrediction"


@dataclass(frozen=True)
class GovernanceRejectedPrediction(WorldDomainEvent):
    event_type: str = "GovernanceRejectedPrediction"


@dataclass(frozen=True)
class WorldSnapshotArchived(WorldDomainEvent):
    event_type: str = "WorldSnapshotArchived"
