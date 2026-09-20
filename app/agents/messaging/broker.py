"""
Message Broker Abstraction.
Defines BaseMessageBroker and InMemoryMessageBroker.
Future-compatible with Google Cloud Pub/Sub, Kafka, and Redis Streams.
"""

from abc import ABC, abstractmethod
import asyncio
from typing import Callable, Coroutine, Dict, List
from app.agents.messaging.envelopes import MessageEnvelope


class BaseMessageBroker(ABC):
    @abstractmethod
    async def publish_envelope(self, topic: str, envelope: MessageEnvelope) -> None:
        pass

    @abstractmethod
    async def subscribe_topic(self, topic: str, handler: Callable[[MessageEnvelope], Coroutine]) -> None:
        pass


class InMemoryMessageBroker(BaseMessageBroker):
    """In-memory Message Broker implementation."""

    def __init__(self):
        self._subscriptions: Dict[str, List[Callable[[MessageEnvelope], Coroutine]]] = {}
        self._lock = asyncio.Lock()

    async def publish_envelope(self, topic: str, envelope: MessageEnvelope) -> None:
        async with self._lock:
            handlers = list(self._subscriptions.get(topic, []))
        for handler in handlers:
            await handler(envelope)

    async def subscribe_topic(self, topic: str, handler: Callable[[MessageEnvelope], Coroutine]) -> None:
        async with self._lock:
            if topic not in self._subscriptions:
                self._subscriptions[topic] = []
            self._subscriptions[topic].append(handler)
