"""
Mission Lifecycle Events
========================
Strongly typed domain events emitted during each phase of mission construction,
state transitions, risk evaluation, and budget estimation.
"""

from dataclasses import dataclass
from research_validation.goal.interfaces.event_bus import GoalIntelligenceDomainEvent


@dataclass(frozen=True)
class MissionCreatedEvent(GoalIntelligenceDomainEvent):
    """Emitted when a new Mission entity is instantiated."""
    pass


@dataclass(frozen=True)
class MissionStateTransitionEvent(GoalIntelligenceDomainEvent):
    """Emitted whenever the Mission FSM transitions to a new state."""
    pass


@dataclass(frozen=True)
class CapabilityAnalysisCompletedEvent(GoalIntelligenceDomainEvent):
    """Emitted when capability discovery and gap analysis finishes."""
    pass


@dataclass(frozen=True)
class DependencyAnalysisCompletedEvent(GoalIntelligenceDomainEvent):
    """Emitted when dependency graph validation and cycle checking finishes."""
    pass


@dataclass(frozen=True)
class RiskCalculatedEvent(GoalIntelligenceDomainEvent):
    """Emitted when multidimensional risk assessment finishes."""
    pass


@dataclass(frozen=True)
class BudgetEstimatedEvent(GoalIntelligenceDomainEvent):
    """Emitted when resource and execution budget estimations are finalized."""
    pass


@dataclass(frozen=True)
class MissionReadyForObservationEvent(GoalIntelligenceDomainEvent):
    """Emitted when the Mission reaches READY_FOR_OBSERVATION and is ready for Stage 2."""
    pass


@dataclass(frozen=True)
class MissionCompletedEvent(GoalIntelligenceDomainEvent):
    pass


@dataclass(frozen=True)
class MissionFailedEvent(GoalIntelligenceDomainEvent):
    pass


@dataclass(frozen=True)
class MissionArchivedEvent(GoalIntelligenceDomainEvent):
    pass
