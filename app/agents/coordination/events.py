"""
Coordination Domain Events.
Pub/Sub compatible domain events published to EventBus for multi-agent coordination telemetry.
"""

from dataclasses import dataclass
from app.agents.events import AgentEvent


@dataclass(frozen=True)
class AgentRegisteredEvent(AgentEvent):
    """Emitted when an agent registers in the directory."""
    event_type: str = "AgentRegistered"


@dataclass(frozen=True)
class AgentAvailableEvent(AgentEvent):
    """Emitted when an agent transitions to AVAILABLE."""
    event_type: str = "AgentAvailable"


@dataclass(frozen=True)
class AgentSelectedEvent(AgentEvent):
    """Emitted when an agent is matched and selected for a task or team."""
    event_type: str = "AgentSelected"


@dataclass(frozen=True)
class DelegationStartedEvent(AgentEvent):
    """Emitted when task delegation commences."""
    event_type: str = "DelegationStarted"


@dataclass(frozen=True)
class DelegationCompletedEvent(AgentEvent):
    """Emitted when delegated tasks complete."""
    event_type: str = "DelegationCompleted"


@dataclass(frozen=True)
class TeamCreatedEvent(AgentEvent):
    """Emitted when an agent team or dynamic formation is established."""
    event_type: str = "TeamCreated"


@dataclass(frozen=True)
class TeamDisbandedEvent(AgentEvent):
    """Emitted when a temporary team is dismissed."""
    event_type: str = "TeamDisbanded"


@dataclass(frozen=True)
class CapabilityMatchedEvent(AgentEvent):
    """Emitted when capabilities are matched for a task."""
    event_type: str = "CapabilityMatched"


@dataclass(frozen=True)
class NegotiationStartedEvent(AgentEvent):
    """Emitted when Contract Net or auction negotiation begins."""
    event_type: str = "NegotiationStarted"


@dataclass(frozen=True)
class NegotiationCompletedEvent(AgentEvent):
    """Emitted when negotiation concludes with an award."""
    event_type: str = "NegotiationCompleted"


@dataclass(frozen=True)
class ConsensusReachedEvent(AgentEvent):
    """Emitted when quorum consensus or voting concludes."""
    event_type: str = "ConsensusReached"


@dataclass(frozen=True)
class ConflictDetectedEvent(AgentEvent):
    """Emitted when a resource or capability conflict occurs."""
    event_type: str = "ConflictDetected"


@dataclass(frozen=True)
class ConflictResolvedEvent(AgentEvent):
    """Emitted when a conflict is mediated and resolved."""
    event_type: str = "ConflictResolved"


@dataclass(frozen=True)
class SwarmStartedEvent(AgentEvent):
    """Emitted when a swarm execution initiates."""
    event_type: str = "SwarmStarted"


@dataclass(frozen=True)
class SwarmCompletedEvent(AgentEvent):
    """Emitted when a swarm execution terminates."""
    event_type: str = "SwarmCompleted"
