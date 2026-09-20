"""
Agent Domain Events for Autonomous Agent Operating System.
Defines immutable domain events emitted across the entire cognitive, execution,
collaboration, security, reflection, and learning lifecycle.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4


class EventPriority(str, Enum):
    """Priority levels for event dispatching."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class AgentEvent:
    """Base domain event for all agent state lifecycle changes."""

    event_id: UUID = field(default_factory=uuid4)
    event_type: str = "AgentEvent"
    execution_id: str = ""
    document_id: str = ""
    trace_id: str = ""
    correlation_id: str = ""
    priority: EventPriority = EventPriority.NORMAL
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    payload: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes event to dictionary for event bus publishing and serialization."""
        data = asdict(self)
        data["event_id"] = str(self.event_id)
        data["priority"] = self.priority.value if isinstance(self.priority, EventPriority) else str(self.priority)
        data["timestamp"] = self.timestamp.isoformat()
        return data


# ==========================================
# Legacy-Compatible Lifecycle Events
# ==========================================

@dataclass(frozen=True)
class GoalReceivedEvent(AgentEvent):
    event_type: str = "GoalReceived"


@dataclass(frozen=True)
class PlanningStartedEvent(AgentEvent):
    event_type: str = "PlanningStarted"


@dataclass(frozen=True)
class PlanningCompletedEvent(AgentEvent):
    event_type: str = "PlanningCompleted"


@dataclass(frozen=True)
class ExecutionStartedEvent(AgentEvent):
    event_type: str = "ExecutionStarted"


@dataclass(frozen=True)
class ExecutionCompletedEvent(AgentEvent):
    event_type: str = "ExecutionCompleted"


@dataclass(frozen=True)
class ObservationCompletedEvent(AgentEvent):
    event_type: str = "ObservationCompleted"


@dataclass(frozen=True)
class ReflectionStartedEvent(AgentEvent):
    event_type: str = "ReflectionStarted"


@dataclass(frozen=True)
class AgentCompletedEvent(AgentEvent):
    event_type: str = "AgentCompleted"


@dataclass(frozen=True)
class AgentFailedEvent(AgentEvent):
    event_type: str = "AgentFailed"


@dataclass(frozen=True)
class RetryRequestedEvent(AgentEvent):
    event_type: str = "RetryRequested"


# ==========================================
# Phase 26 Advanced Autonomous Events
# ==========================================

@dataclass(frozen=True)
class GoalUnderstandingCompletedEvent(AgentEvent):
    """Emitted when natural language goal is parsed and formal specification is generated."""
    event_type: str = "GoalUnderstandingCompleted"


@dataclass(frozen=True)
class PlanOptimizedEvent(AgentEvent):
    """Emitted when candidate execution plans have been Pareto-optimized."""
    event_type: str = "PlanOptimized"


@dataclass(frozen=True)
class TaskStartedEvent(AgentEvent):
    """Emitted when an individual node in the DAG begins execution."""
    event_type: str = "TaskStarted"
    task_id: str = ""
    assigned_agent: str = ""


@dataclass(frozen=True)
class TaskCompletedEvent(AgentEvent):
    """Emitted when an individual node in the DAG completes successfully."""
    event_type: str = "TaskCompleted"
    task_id: str = ""
    duration_ms: float = 0.0


@dataclass(frozen=True)
class TaskFailedEvent(AgentEvent):
    """Emitted when an individual node in the DAG encounters an error."""
    event_type: str = "TaskFailed"
    task_id: str = ""
    error_message: str = ""
    retry_count: int = 0


@dataclass(frozen=True)
class TaskMutatedEvent(AgentEvent):
    """Emitted when the TaskGraph is dynamically altered during execution."""
    event_type: str = "TaskMutated"
    mutation_type: str = ""
    affected_tasks: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class AgentNegotiationStartedEvent(AgentEvent):
    """Emitted when multiple agents begin contract negotiation for a task."""
    event_type: str = "AgentNegotiationStarted"
    task_id: str = ""


@dataclass(frozen=True)
class AgentNegotiationCompletedEvent(AgentEvent):
    """Emitted when task delegation is finalized between agents."""
    event_type: str = "AgentNegotiationCompleted"
    task_id: str = ""
    selected_agent_id: str = ""
    agreed_cost: float = 0.0


@dataclass(frozen=True)
class ToolInvokedEvent(AgentEvent):
    """Emitted when a cognitive tool is triggered."""
    event_type: str = "ToolInvoked"
    tool_name: str = ""
    agent_id: str = ""


@dataclass(frozen=True)
class ToolPolicyViolationEvent(AgentEvent):
    """Emitted when a tool invocation breaches compliance or security policy."""
    event_type: str = "ToolPolicyViolation"
    tool_name: str = ""
    policy_name: str = ""
    violation_reason: str = ""


@dataclass(frozen=True)
class ReflectionCritiqueCompletedEvent(AgentEvent):
    """Emitted when multi-critic evaluation concludes."""
    event_type: str = "ReflectionCritiqueCompleted"
    overall_score: float = 0.0
    passed: bool = False


@dataclass(frozen=True)
class SelfCorrectionTriggeredEvent(AgentEvent):
    """Emitted when a low critique score triggers autonomous replanning."""
    event_type: str = "SelfCorrectionTriggered"
    iteration: int = 1
    reason: str = ""


@dataclass(frozen=True)
class HumanEscalationRequestedEvent(AgentEvent):
    """Emitted when autonomous confidence falls below safety thresholds."""
    event_type: str = "HumanEscalationRequested"
    ticket_id: str = ""
    priority: EventPriority = EventPriority.HIGH
    sla_timeout_seconds: float = 300.0


@dataclass(frozen=True)
class HumanFeedbackReceivedEvent(AgentEvent):
    """Emitted when human operator provides feedback or overrides a decision."""
    event_type: str = "HumanFeedbackReceived"
    ticket_id: str = ""
    action: str = ""  # APPROVE, REJECT, MODIFY
    operator_id: str = ""


@dataclass(frozen=True)
class MemoryConsolidationCompletedEvent(AgentEvent):
    """Emitted when background pattern mining distills semantic rules."""
    event_type: str = "MemoryConsolidationCompleted"
    promoted_patterns_count: int = 0


@dataclass(frozen=True)
class StateTransitionEvent(AgentEvent):
    """Emitted on every state transition of the autonomous runtime state machine."""
    event_type: str = "StateTransition"
    from_state: str = ""
    to_state: str = ""


@dataclass(frozen=True)
class SecurityViolationEvent(AgentEvent):
    """Emitted when an agent attempts an unauthorized operation."""
    event_type: str = "SecurityViolation"
    agent_id: str = ""
    action: str = ""
    severity: str = "CRITICAL"
