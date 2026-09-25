"""
Planner Domain Events.
Pub/Sub compatible domain events emitted during cognitive planning progression.
"""

from dataclasses import dataclass
from app.agents.events import AgentEvent


@dataclass(frozen=True)
class PlanningStartedEvent(AgentEvent):
    event_type: str = "PlanningStarted"


@dataclass(frozen=True)
class GoalAnalyzedEvent(AgentEvent):
    event_type: str = "GoalAnalyzed"


@dataclass(frozen=True)
class TasksDecomposedEvent(AgentEvent):
    event_type: str = "TasksDecomposed"


@dataclass(frozen=True)
class PlanGeneratedEvent(AgentEvent):
    event_type: str = "PlanGenerated"


@dataclass(frozen=True)
class PlanValidatedEvent(AgentEvent):
    event_type: str = "PlanValidated"


@dataclass(frozen=True)
class PlanOptimizedEvent(AgentEvent):
    event_type: str = "PlanOptimized"


@dataclass(frozen=True)
class PlanRankedEvent(AgentEvent):
    event_type: str = "PlanRanked"


@dataclass(frozen=True)
class PlanRepairedEvent(AgentEvent):
    event_type: str = "PlanRepaired"


@dataclass(frozen=True)
class PlanCompletedEvent(AgentEvent):
    event_type: str = "PlanCompleted"


@dataclass(frozen=True)
class PlanningFailedEvent(AgentEvent):
    event_type: str = "PlanningFailed"
