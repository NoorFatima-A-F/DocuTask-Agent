"""
Event Bus Interface
===================
Abstract event bus contract for event-driven decoupled goal intelligence workflows.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, TypeVar


@dataclass(frozen=True)
class GoalIntelligenceDomainEvent:
    """Base immutable domain event for goal and mission lifecycle changes."""
    event_id: str
    event_type: str
    aggregate_id: str
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    payload: Dict[str, Any] = field(default_factory=dict)
    event_digest_sha256: str = field(default="")


E = TypeVar("E", bound=GoalIntelligenceDomainEvent)
EventHandler = Callable[[E], None]


class IEventBus(ABC):
    """Event bus interface for publishing and subscribing to domain events."""

    @abstractmethod
    def publish(self, event: GoalIntelligenceDomainEvent) -> None:
        """Publishes an event to all registered subscribers."""
        raise NotImplementedError

    @abstractmethod
    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """Registers a handler for a specific event type."""
        raise NotImplementedError

    @abstractmethod
    def get_published_events(self) -> List[GoalIntelligenceDomainEvent]:
        """Returns the full historical sequence of published events."""
        raise NotImplementedError


class InMemoryEventBus(IEventBus):
    """Synchronous in-memory event bus implementation."""

    def __init__(self):
        self._handlers: Dict[str, List[EventHandler]] = {}
        self._event_history: List[GoalIntelligenceDomainEvent] = []

    def publish(self, event: GoalIntelligenceDomainEvent) -> None:
        self._event_history.append(event)
        handlers = self._handlers.get(event.event_type, [])
        for handler in handlers:
            handler(event)
        # Catch-all handlers
        for handler in self._handlers.get("*", []):
            handler(event)

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def get_published_events(self) -> List[GoalIntelligenceDomainEvent]:
        return list(self._event_history)

    def clear(self) -> None:
        self._event_history.clear()
