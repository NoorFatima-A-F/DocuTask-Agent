"""
Planning Domain Events.
Pub/Sub compatible domain events for plan lifecycle state changes and notifications.
"""

from dataclasses import dataclass
from app.agents.events import AgentEvent


@dataclass(frozen=True)
class PlanRequestedEvent(AgentEvent):
    event_type: str = "PlanRequested"


@dataclass(frozen=True)
class PlanCreatedEvent(AgentEvent):
    event_type: str = "PlanCreated"


@dataclass(frozen=True)
class PlanValidatedEvent(AgentEvent):
    event_type: str = "PlanValidated"


@dataclass(frozen=True)
class PlanOptimizedEvent(AgentEvent):
    event_type: str = "PlanOptimized"


@dataclass(frozen=True)
class PlanApprovedEvent(AgentEvent):
    event_type: str = "PlanApproved"


@dataclass(frozen=True)
class PlanRejectedEvent(AgentEvent):
    event_type: str = "PlanRejected"


@dataclass(frozen=True)
class PlanUpdatedEvent(AgentEvent):
    event_type: str = "PlanUpdated"


@dataclass(frozen=True)
class PlanArchivedEvent(AgentEvent):
    event_type: str = "PlanArchived"


@dataclass(frozen=True)
class PlanExecutedEvent(AgentEvent):
    event_type: str = "PlanExecuted"


@dataclass(frozen=True)
class PlanCancelledEvent(AgentEvent):
    event_type: str = "PlanCancelled"
