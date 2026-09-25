"""
Agent Event Bus Interface.
Defines contract for publishing and subscribing to agent domain events.
"""

from abc import ABC, abstractmethod
from typing import Callable, Coroutine
from app.agents.events import AgentEvent


class AgentEventBus(ABC):
    """Abstract interface for agent domain event bus."""

    @abstractmethod
    async def publish(self, event: AgentEvent) -> None:
        """Publishes a domain event to all registered listeners."""
        pass

    @abstractmethod
    def subscribe(self, event_type: str, handler: Callable[[AgentEvent], Coroutine]) -> None:
        """Subscribes an async handler function to a specific event type."""
        pass
