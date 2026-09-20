"""
Coordination Message Bus.
Coordinates asynchronous publish-subscribe message distribution across teams, topics, and swarms.
"""

from typing import Callable, Dict, List
from uuid import UUID
from app.agents.coordination.communication import AgentMessage


class CoordinationMessageBus:
    """Pub/Sub message bus supporting topic subscriptions for agents and teams."""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[AgentMessage], None]]] = {}

    def subscribe(self, topic: str, handler: Callable[[AgentMessage], None]) -> None:
        """Subscribes an agent callback handler to a topic."""
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(handler)

    async def publish(self, topic: str, message: AgentMessage) -> None:
        """Publishes a message to all subscribers of the topic."""
        handlers = self._subscribers.get(topic, [])
        for handler in handlers:
            handler(message)
