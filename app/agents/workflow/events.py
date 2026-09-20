"""
Workflow Domain Events.
Pub/Sub compatible domain events published to EventBus for workflow orchestration telemetry.
"""

from dataclasses import dataclass
from app.agents.events import AgentEvent


@dataclass(frozen=True)
class WorkflowCreatedEvent(AgentEvent):
    event_type: str = "WorkflowCreated"


@dataclass(frozen=True)
class WorkflowStartedEvent(AgentEvent):
    event_type: str = "WorkflowStarted"


@dataclass(frozen=True)
class WorkflowPausedEvent(AgentEvent):
    event_type: str = "WorkflowPaused"


@dataclass(frozen=True)
class WorkflowResumedEvent(AgentEvent):
    event_type: str = "WorkflowResumed"


@dataclass(frozen=True)
class WorkflowWaitingEvent(AgentEvent):
    event_type: str = "WorkflowWaiting"


@dataclass(frozen=True)
class WorkflowCompletedEvent(AgentEvent):
    event_type: str = "WorkflowCompleted"


@dataclass(frozen=True)
class WorkflowFailedEvent(AgentEvent):
    event_type: str = "WorkflowFailed"


@dataclass(frozen=True)
class WorkflowCancelledEvent(AgentEvent):
    event_type: str = "WorkflowCancelled"


@dataclass(frozen=True)
class WorkflowMigratedEvent(AgentEvent):
    event_type: str = "WorkflowMigrated"


@dataclass(frozen=True)
class ChildWorkflowStartedEvent(AgentEvent):
    event_type: str = "ChildWorkflowStarted"


@dataclass(frozen=True)
class SagaStartedEvent(AgentEvent):
    event_type: str = "SagaStarted"


@dataclass(frozen=True)
class CompensationStartedEvent(AgentEvent):
    event_type: str = "CompensationStarted"


@dataclass(frozen=True)
class ApprovalRequestedEvent(AgentEvent):
    event_type: str = "ApprovalRequested"


@dataclass(frozen=True)
class ApprovalReceivedEvent(AgentEvent):
    event_type: str = "ApprovalReceived"
