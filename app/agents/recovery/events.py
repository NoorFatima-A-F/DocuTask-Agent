"""
Recovery Domain Events.
Pub/Sub compatible domain events published to EventBus for failure telemetry and recovery auditability.
"""

from dataclasses import dataclass
from app.agents.events import AgentEvent


@dataclass(frozen=True)
class FailureDetectedEvent(AgentEvent):
    event_type: str = "FailureDetected"


@dataclass(frozen=True)
class FailureClassifiedEvent(AgentEvent):
    event_type: str = "FailureClassified"


@dataclass(frozen=True)
class RootCauseIdentifiedEvent(AgentEvent):
    event_type: str = "RootCauseIdentified"


@dataclass(frozen=True)
class RecoveryStartedEvent(AgentEvent):
    event_type: str = "RecoveryStarted"


@dataclass(frozen=True)
class RecoveryStrategySelectedEvent(AgentEvent):
    event_type: str = "RecoveryStrategySelected"


@dataclass(frozen=True)
class RecoveryPlannedEvent(AgentEvent):
    event_type: str = "RecoveryPlanned"


@dataclass(frozen=True)
class CheckpointRestoredEvent(AgentEvent):
    event_type: str = "CheckpointRestored"


@dataclass(frozen=True)
class ReplayStartedEvent(AgentEvent):
    event_type: str = "ReplayStarted"


@dataclass(frozen=True)
class ReplayCompletedEvent(AgentEvent):
    event_type: str = "ReplayCompleted"


@dataclass(frozen=True)
class RollbackStartedEvent(AgentEvent):
    event_type: str = "RollbackStarted"


@dataclass(frozen=True)
class RollbackCompletedEvent(AgentEvent):
    event_type: str = "RollbackCompleted"


@dataclass(frozen=True)
class CompensationStartedEvent(AgentEvent):
    event_type: str = "CompensationStarted"


@dataclass(frozen=True)
class CompensationCompletedEvent(AgentEvent):
    event_type: str = "CompensationCompleted"


@dataclass(frozen=True)
class StateReconciledEvent(AgentEvent):
    event_type: str = "StateReconciled"


@dataclass(frozen=True)
class DeadLetterCreatedEvent(AgentEvent):
    event_type: str = "DeadLetterCreated"


@dataclass(frozen=True)
class SelfHealingStartedEvent(AgentEvent):
    event_type: str = "SelfHealingStarted"


@dataclass(frozen=True)
class SelfHealingCompletedEvent(AgentEvent):
    event_type: str = "SelfHealingCompleted"


@dataclass(frozen=True)
class RecoverySucceededEvent(AgentEvent):
    event_type: str = "RecoverySucceeded"


@dataclass(frozen=True)
class RecoveryFailedEvent(AgentEvent):
    event_type: str = "RecoveryFailed"


@dataclass(frozen=True)
class EscalationTriggeredEvent(AgentEvent):
    event_type: str = "EscalationTriggered"


@dataclass(frozen=True)
class IncidentCreatedEvent(AgentEvent):
    event_type: str = "IncidentCreated"
