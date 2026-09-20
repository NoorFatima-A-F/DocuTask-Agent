"""
Message Router.
Routes messages between agents, ensuring correct point-to-point, broadcast, or multicast delivery.
"""

from typing import Dict, List, Optional
from uuid import UUID
from app.agents.coordination.communication import AgentMessage, CommunicationPattern
from app.agents.coordination.exceptions import InvalidCommunicationRouteError
from app.agents.coordination.interfaces import IMessageRouter


class MessageRouter(IMessageRouter):
    """In-memory point-to-point and broadcast message router with inbox queues."""

    def __init__(self):
        self._inboxes: Dict[UUID, List[AgentMessage]] = {}

    def register_endpoint(self, agent_id: UUID) -> None:
        """Registers an agent inbox."""
        if agent_id not in self._inboxes:
            self._inboxes[agent_id] = []

    async def send_message(self, message: AgentMessage) -> None:
        """Routes message to recipient inbox or broadcasts to all registered inboxes."""
        if message.pattern == CommunicationPattern.BROADCAST or message.recipient_id is None:
            # Broadcast to all registered agents except sender
            for agent_id, inbox in self._inboxes.items():
                if agent_id != message.sender_id:
                    inbox.append(message)
        else:
            if message.recipient_id not in self._inboxes:
                raise InvalidCommunicationRouteError(
                    f"Recipient agent {message.recipient_id} has no registered inbox.",
                    message.recipient_id
                )
            self._inboxes[message.recipient_id].append(message)

    def receive_messages(self, agent_id: UUID) -> List[AgentMessage]:
        """Drains and returns all queued messages for an agent."""
        if agent_id not in self._inboxes:
            return []
        messages = list(self._inboxes[agent_id])
        self._inboxes[agent_id].clear()
        return messages
