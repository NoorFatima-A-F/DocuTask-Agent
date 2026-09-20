"""Enterprise Agent Message Bus for Inter-Agent Communication Protocol.

Provides asynchronous pub/sub messaging, point-to-point dispatch, topic routing,
dead-letter queue (DLQ), and distributed message tracing.
"""

from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from typing import Any, Callable, Coroutine, Dict, List, Optional

from app.agents.collaboration.messaging.agent_message import AgentMessage, MessageType

logger = logging.getLogger(__name__)

MessageHandler = Callable[[AgentMessage], Coroutine[Any, Any, None]]


class AgentMessageBus:
    """High-throughput asynchronous message bus for agent collaboration."""

    def __init__(self) -> None:
        self._direct_handlers: Dict[str, List[MessageHandler]] = defaultdict(list)
        self._topic_handlers: Dict[str, List[MessageHandler]] = defaultdict(list)
        self._message_history: List[AgentMessage] = []
        self._dead_letter_queue: List[AgentMessage] = []

    def subscribe_agent(self, agent_id: str, handler: MessageHandler) -> None:
        """Register a message listener for direct messages addressed to agent_id."""
        self._direct_handlers[agent_id].append(handler)
        logger.debug("Subscribed direct handler for agent %s", agent_id)

    def subscribe_topic(self, topic: str, handler: MessageHandler) -> None:
        """Register a topic subscriber."""
        self._topic_handlers[topic].append(handler)
        logger.debug("Subscribed topic handler for topic %s", topic)

    async def send(self, message: AgentMessage) -> bool:
        """Deliver a direct message to its recipient."""
        self._message_history.append(message)
        handlers = self._direct_handlers.get(message.recipient_id, [])

        if not handlers:
            logger.warning("No handler registered for recipient %s. Moving to DLQ.", message.recipient_id)
            self._dead_letter_queue.append(message)
            return False

        for handler in handlers:
            try:
                await handler(message)
            except Exception as ex:
                logger.exception("Error executing handler for agent %s: %s", message.recipient_id, ex)
                self._dead_letter_queue.append(message)
                return False

        return True

    async def publish(self, topic: str, message: AgentMessage) -> int:
        """Broadcast a message across a topic to all active subscribers."""
        self._message_history.append(message)
        handlers = self._topic_handlers.get(topic, [])

        delivered = 0
        for handler in handlers:
            try:
                await handler(message)
                delivered += 1
            except Exception as ex:
                logger.exception("Error broadcasting on topic %s: %s", topic, ex)

        return delivered

    def get_history(self, correlation_id: Optional[str] = None) -> List[AgentMessage]:
        if correlation_id:
            return [m for m in self._message_history if m.correlation_id == correlation_id]
        return list(self._message_history)

    def get_dlq(self) -> List[AgentMessage]:
        return list(self._dead_letter_queue)

    def clear_dlq(self) -> int:
        count = len(self._dead_letter_queue)
        self._dead_letter_queue.clear()
        return count
