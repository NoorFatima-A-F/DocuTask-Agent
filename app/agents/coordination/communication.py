"""
Communication Models and Message Envelopes.
Defines strongly typed agent messages, message types, delivery semantics, and correlation envelopes.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class CommunicationPattern(str, Enum):
    """Message delivery patterns."""
    REQUEST_REPLY = "REQUEST_REPLY"
    BROADCAST = "BROADCAST"
    PUBLISH_SUBSCRIBE = "PUBLISH_SUBSCRIBE"
    STREAMING = "STREAMING"
    ASYNCHRONOUS_ONE_WAY = "ASYNCHRONOUS_ONE_WAY"


class MessagePerformative(str, Enum):
    """FIPA-ACL compliant communicative acts."""
    INFORM = "INFORM"
    REQUEST = "REQUEST"
    PROPOSE = "PROPOSE"
    ACCEPT_PROPOSAL = "ACCEPT_PROPOSAL"
    REJECT_PROPOSAL = "REJECT_PROPOSAL"
    QUERY = "QUERY"
    CONFIRM = "CONFIRM"
    DISCONFIRM = "DISCONFIRM"
    CALL_FOR_PROPOSALS = "CALL_FOR_PROPOSALS"


class AgentMessage(BaseModel):
    """Structured message exchanged between autonomous agents."""
    message_id: UUID = Field(default_factory=uuid4)
    sender_id: UUID
    recipient_id: Optional[UUID] = None  # None indicates broadcast
    performative: MessagePerformative = MessagePerformative.INFORM
    pattern: CommunicationPattern = CommunicationPattern.REQUEST_REPLY
    conversation_id: UUID = Field(default_factory=uuid4)
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    reply_to: Optional[UUID] = None
    content: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}
