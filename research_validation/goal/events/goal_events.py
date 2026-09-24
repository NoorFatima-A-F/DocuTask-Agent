"""
Goal Lifecycle Events
=====================
Strongly typed domain events emitted during goal creation, validation, and status updates.
"""

from dataclasses import dataclass
from research_validation.goal.interfaces.event_bus import GoalIntelligenceDomainEvent


@dataclass(frozen=True)
class GoalCreatedEvent(GoalIntelligenceDomainEvent):
    """Emitted when a new Goal is registered in the system."""
    pass


@dataclass(frozen=True)
class GoalValidatedEvent(GoalIntelligenceDomainEvent):
    """Emitted when a Goal successfully passes all validation rules."""
    pass


@dataclass(frozen=True)
class GoalRejectedEvent(GoalIntelligenceDomainEvent):
    """Emitted when a Goal fails validation with specific error reasons."""
    pass


@dataclass(frozen=True)
class GoalUpdatedEvent(GoalIntelligenceDomainEvent):
    """Emitted when a Goal transitions version or status."""
    pass
