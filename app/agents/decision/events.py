"""
Decision Engine Domain Events.
Pub/Sub compatible domain events for policy evaluations and decision approvals.
"""

from dataclasses import dataclass
from app.agents.events import AgentEvent


@dataclass(frozen=True)
class DecisionRequestedEvent(AgentEvent):
    event_type: str = "DecisionRequested"


@dataclass(frozen=True)
class DecisionStartedEvent(AgentEvent):
    event_type: str = "DecisionStarted"


@dataclass(frozen=True)
class DecisionCompletedEvent(AgentEvent):
    event_type: str = "DecisionCompleted"


@dataclass(frozen=True)
class DecisionApprovedEvent(AgentEvent):
    event_type: str = "DecisionApproved"


@dataclass(frozen=True)
class DecisionRejectedEvent(AgentEvent):
    event_type: str = "DecisionRejected"


@dataclass(frozen=True)
class DecisionFailedEvent(AgentEvent):
    event_type: str = "DecisionFailed"


@dataclass(frozen=True)
class PolicyEvaluatedEvent(AgentEvent):
    event_type: str = "PolicyEvaluated"


@dataclass(frozen=True)
class RuleTriggeredEvent(AgentEvent):
    event_type: str = "RuleTriggered"


@dataclass(frozen=True)
class RiskDetectedEvent(AgentEvent):
    event_type: str = "RiskDetected"


@dataclass(frozen=True)
class EscalationTriggeredEvent(AgentEvent):
    event_type: str = "EscalationTriggered"
