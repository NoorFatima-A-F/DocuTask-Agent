"""
Reflection Domain Events.
Pub/Sub compatible domain events published to EventBus for reflection, evaluation, and learning telemetry.
"""

from dataclasses import dataclass
from app.agents.events import AgentEvent


@dataclass(frozen=True)
class ReflectionStartedEvent(AgentEvent):
    """Emitted when a reflection session initiates processing an execution trace."""
    event_type: str = "ReflectionStarted"


@dataclass(frozen=True)
class EvaluationCompletedEvent(AgentEvent):
    """Emitted when the multi-dimensional evaluation pipeline finishes analysis."""
    event_type: str = "EvaluationCompleted"


@dataclass(frozen=True)
class CritiqueGeneratedEvent(AgentEvent):
    """Emitted when the self-critique engine completes cognitive and operational critique."""
    event_type: str = "CritiqueGenerated"


@dataclass(frozen=True)
class LearningArtifactCreatedEvent(AgentEvent):
    """Emitted when an immutable learning artifact is synthesized and ready for memory promotion."""
    event_type: str = "LearningArtifactCreated"


@dataclass(frozen=True)
class RecommendationGeneratedEvent(AgentEvent):
    """Emitted when cross-subsystem actionable recommendations are formulated."""
    event_type: str = "RecommendationGenerated"


@dataclass(frozen=True)
class PlannerFeedbackGeneratedEvent(AgentEvent):
    """Emitted when structured feedback is produced for the Intelligent Planner."""
    event_type: str = "PlannerFeedbackGenerated"


@dataclass(frozen=True)
class ExecutionFeedbackGeneratedEvent(AgentEvent):
    """Emitted when structured feedback is produced for the Stateful Execution Engine."""
    event_type: str = "ExecutionFeedbackGenerated"


@dataclass(frozen=True)
class AdaptationProposalCreatedEvent(AgentEvent):
    """Emitted when an operational adaptation proposal is staged for approval."""
    event_type: str = "AdaptationProposalCreated"


@dataclass(frozen=True)
class ReflectionCompletedEvent(AgentEvent):
    """Emitted when the entire reflection and learning cycle terminates successfully."""
    event_type: str = "ReflectionCompleted"


@dataclass(frozen=True)
class ReflectionFailedEvent(AgentEvent):
    """Emitted when reflection fails to process or encounters an unrecoverable validation error."""
    event_type: str = "ReflectionFailed"
