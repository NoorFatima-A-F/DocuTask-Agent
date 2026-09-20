"""
Memory Subsystem Domain Events.
Pub/Sub compatible domain events for memory lifecycle changes.
"""

from dataclasses import dataclass, field
from app.agents.events import AgentEvent


@dataclass(frozen=True)
class MemoryCreatedEvent(AgentEvent):
    event_type: str = "MemoryCreated"


@dataclass(frozen=True)
class MemoryUpdatedEvent(AgentEvent):
    event_type: str = "MemoryUpdated"


@dataclass(frozen=True)
class MemoryDeletedEvent(AgentEvent):
    event_type: str = "MemoryDeleted"


@dataclass(frozen=True)
class MemoryExpiredEvent(AgentEvent):
    event_type: str = "MemoryExpired"


@dataclass(frozen=True)
class MemoryPromotedEvent(AgentEvent):
    event_type: str = "MemoryPromoted"


@dataclass(frozen=True)
class MemoryRetrievedEvent(AgentEvent):
    event_type: str = "MemoryRetrieved"


@dataclass(frozen=True)
class MemoryMergedEvent(AgentEvent):
    event_type: str = "MemoryMerged"


@dataclass(frozen=True)
class MemoryArchivedEvent(AgentEvent):
    event_type: str = "MemoryArchived"


@dataclass(frozen=True)
class MemoryCompactedEvent(AgentEvent):
    event_type: str = "MemoryCompacted"


@dataclass(frozen=True)
class MemoryRestoredEvent(AgentEvent):
    event_type: str = "MemoryRestored"
