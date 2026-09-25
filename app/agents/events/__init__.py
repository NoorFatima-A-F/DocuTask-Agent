"""
Agent Domain Events and Event-Driven Architecture Package.
"""

from app.agents.events.event_types import (
    AgentCompletedEvent,
    AgentEvent,
    AgentFailedEvent,
    AgentNegotiationCompletedEvent,
    AgentNegotiationStartedEvent,
    EventPriority,
    ExecutionCompletedEvent,
    ExecutionStartedEvent,
    GoalReceivedEvent,
    GoalUnderstandingCompletedEvent,
    HumanEscalationRequestedEvent,
    HumanFeedbackReceivedEvent,
    MemoryConsolidationCompletedEvent,
    ObservationCompletedEvent,
    PlanOptimizedEvent,
    PlanningCompletedEvent,
    PlanningStartedEvent,
    ReflectionCritiqueCompletedEvent,
    ReflectionStartedEvent,
    RetryRequestedEvent,
    SecurityViolationEvent,
    SelfCorrectionTriggeredEvent,
    StateTransitionEvent,
    TaskCompletedEvent,
    TaskFailedEvent,
    TaskMutatedEvent,
    TaskStartedEvent,
    ToolInvokedEvent,
    ToolPolicyViolationEvent,
)
from app.agents.events.dead_letter_queue import DeadLetterQueue, DeadLetterRecord
from app.agents.events.event_store import EventEntry, EventStore
from app.agents.events.event_bus import EnterpriseEventBus

__all__ = [
    # Legacy event types
    "AgentEvent",
    "GoalReceivedEvent",
    "PlanningStartedEvent",
    "PlanningCompletedEvent",
    "ExecutionStartedEvent",
    "ExecutionCompletedEvent",
    "ObservationCompletedEvent",
    "ReflectionStartedEvent",
    "AgentCompletedEvent",
    "AgentFailedEvent",
    "RetryRequestedEvent",
    # Advanced Phase 26 event types
    "EventPriority",
    "GoalUnderstandingCompletedEvent",
    "PlanOptimizedEvent",
    "TaskStartedEvent",
    "TaskCompletedEvent",
    "TaskFailedEvent",
    "TaskMutatedEvent",
    "AgentNegotiationStartedEvent",
    "AgentNegotiationCompletedEvent",
    "ToolInvokedEvent",
    "ToolPolicyViolationEvent",
    "ReflectionCritiqueCompletedEvent",
    "SelfCorrectionTriggeredEvent",
    "HumanEscalationRequestedEvent",
    "HumanFeedbackReceivedEvent",
    "MemoryConsolidationCompletedEvent",
    "StateTransitionEvent",
    "SecurityViolationEvent",
    # Infrastructure
    "DeadLetterQueue",
    "DeadLetterRecord",
    "EventStore",
    "EventEntry",
    "EnterpriseEventBus",
]
