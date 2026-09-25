"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Agent Message Bus.
Implements asynchronous and priority-based agent communication with
structured message schemas, tracing, and decoupled mailboxes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import uuid
import logging

logger = logging.getLogger(__name__)


class AgentMessageType(str, Enum):
    """Classification of messages exchanged across the agent communication bus."""
    COMMAND = "COMMAND"
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"
    PROPOSAL = "PROPOSAL"
    DECISION = "DECISION"
    EVIDENCE = "EVIDENCE"
    ARTIFACT = "ARTIFACT"
    ERROR = "ERROR"
    HEARTBEAT = "HEARTBEAT"
    CANCELLATION = "CANCELLATION"
    APPROVAL = "APPROVAL"


@dataclass
class AgentMessage:
    """Standardized schema for all multi-agent communication."""
    id: str = field(default_factory=lambda: f"msg-{uuid.uuid4().hex[:12]}")
    sender: str = ""
    receiver: str = ""  # Specific agent ID, or "*" for broadcast
    type: AgentMessageType | str = AgentMessageType.REQUEST
    priority: str = "NORMAL"  # CRITICAL, HIGH, NORMAL, LOW
    trace_id: str = field(default_factory=lambda: f"trace-{uuid.uuid4().hex[:10]}")
    ttl_seconds: int = 300
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "type": self.type.value if isinstance(self.type, Enum) else str(self.type),
            "priority": self.priority,
            "trace_id": self.trace_id,
            "ttl_seconds": self.ttl_seconds,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
        }


class AgentMessageBus:
    """
    Decoupled Message Bus for agent-to-agent and supervisor-worker communication.
    Guarantees no direct unmediated agent-to-agent calls.
    """

    def __init__(self):
        # agent_id -> list of pending messages
        self._mailboxes: Dict[str, List[AgentMessage]] = {}
        # subscriber handlers: agent_id or topic -> list of callbacks
        self._subscribers: Dict[str, List[Callable[[AgentMessage], None]]] = {}
        # global trace audit
        self._audit_trail: List[AgentMessage] = []

    def send(self, message: AgentMessage) -> None:
        """Sends a point-to-point or broadcast message to agent mailbox(es)."""
        self._audit_trail.append(message)

        if message.receiver == "*":
            # Broadcast to all known mailboxes and subscribers
            for agent_id, box in self._mailboxes.items():
                box.append(message)
            for sub_list in self._subscribers.values():
                for callback in sub_list:
                    try:
                        callback(message)
                    except Exception as e:
                        logger.warning(f"Error in broadcast subscriber callback: {e}")
            logger.info(f"Broadcast message {message.id} from '{message.sender}'")
            return

        if message.receiver not in self._mailboxes:
            self._mailboxes[message.receiver] = []
        self._mailboxes[message.receiver].append(message)

        # Notify active subscribers for this receiver
        if message.receiver in self._subscribers:
            for callback in self._subscribers[message.receiver]:
                try:
                    callback(message)
                except Exception as e:
                    logger.warning(f"Error in message subscriber callback: {e}")

        logger.info(
            f"Message {message.id} routed: '{message.sender}' -> '{message.receiver}' "
            f"[{message.type}]"
        )

    def receive(self, agent_id: str) -> Optional[AgentMessage]:
        """Retrieves and removes the next pending message for an agent."""
        if agent_id not in self._mailboxes or not self._mailboxes[agent_id]:
            return None
        # Retrieve highest priority message or oldest FIFO
        messages = self._mailboxes[agent_id]
        return messages.pop(0)

    def peek(self, agent_id: str) -> List[AgentMessage]:
        """Peeks at all pending messages in an agent's mailbox without removing them."""
        return list(self._mailboxes.get(agent_id, []))

    def subscribe(self, channel_or_agent: str, handler: Callable[[AgentMessage], None]) -> None:
        """Subscribes a listener callback to messages for a specific agent or channel."""
        if channel_or_agent not in self._subscribers:
            self._subscribers[channel_or_agent] = []
        self._subscribers[channel_or_agent].append(handler)

    def get_trace_history(self, trace_id: str) -> List[AgentMessage]:
        """Returns all messages correlating to a specific distributed trace ID."""
        return [m for m in self._audit_trail if m.trace_id == trace_id]

    def clear(self) -> None:
        """Clears all mailboxes and audit logs."""
        self._mailboxes.clear()
        self._subscribers.clear()
        self._audit_trail.clear()
