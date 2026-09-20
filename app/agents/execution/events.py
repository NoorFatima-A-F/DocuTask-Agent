"""
Execution Domain Events.
Pub/Sub compatible domain events for runtime state updates and distributed telemetry.
"""

from dataclasses import dataclass
from app.agents.events import AgentEvent


@dataclass(frozen=True)
class ExecutionStartedEvent(AgentEvent):
    event_type: str = "ExecutionStarted"


@dataclass(frozen=True)
class ExecutionScheduledEvent(AgentEvent):
    event_type: str = "ExecutionScheduled"


@dataclass(frozen=True)
class NodeReadyEvent(AgentEvent):
    event_type: str = "NodeReady"


@dataclass(frozen=True)
class NodeStartedEvent(AgentEvent):
    event_type: str = "NodeStarted"


@dataclass(frozen=True)
class NodeCompletedEvent(AgentEvent):
    event_type: str = "NodeCompleted"


@dataclass(frozen=True)
class NodeFailedEvent(AgentEvent):
    event_type: str = "NodeFailed"


@dataclass(frozen=True)
class CheckpointCreatedEvent(AgentEvent):
    event_type: str = "CheckpointCreated"


@dataclass(frozen=True)
class RetryStartedEvent(AgentEvent):
    event_type: str = "RetryStarted"


@dataclass(frozen=True)
class RollbackStartedEvent(AgentEvent):
    event_type: str = "RollbackStarted"


@dataclass(frozen=True)
class ExecutionPausedEvent(AgentEvent):
    event_type: str = "ExecutionPaused"


@dataclass(frozen=True)
class ExecutionResumedEvent(AgentEvent):
    event_type: str = "ExecutionResumed"


@dataclass(frozen=True)
class ExecutionCancelledEvent(AgentEvent):
    event_type: str = "ExecutionCancelled"


@dataclass(frozen=True)
class ExecutionCompletedEvent(AgentEvent):
    event_type: str = "ExecutionCompleted"


@dataclass(frozen=True)
class ExecutionFailedEvent(AgentEvent):
    event_type: str = "ExecutionFailed"


@dataclass(frozen=True)
class WorkerAssignedEvent(AgentEvent):
    event_type: str = "WorkerAssigned"


@dataclass(frozen=True)
class WorkerReleasedEvent(AgentEvent):
    event_type: str = "WorkerReleased"
