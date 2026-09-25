"""
Agent Event Contracts.
Defines DomainEvent, SystemEvent, ProgressEvent, and HeartbeatMessage for EventBus publishing.
"""

from typing import Any, Dict
from pydantic import BaseModel, Field
from app.agents.messaging.metadata import MessageMetadata


class DomainEvent(BaseModel):
    """Base class for all Messaging Domain Events."""

    event_type: str = Field(default="DomainEvent")
    metadata: MessageMetadata = Field(default_factory=MessageMetadata)
    payload: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


AgentEvent = DomainEvent



class SystemEvent(DomainEvent):
    """System-level infrastructure event."""
    event_type: str = Field(default="SystemEvent")


class ProgressEvent(DomainEvent):
    """Execution progress tracking event."""
    event_type: str = Field(default="ProgressEvent")
    progress_percentage: float = Field(default=0.0, ge=0.0, le=100.0)


class HeartbeatMessage(DomainEvent):
    """Agent liveness heartbeat event."""
    event_type: str = Field(default="Heartbeat")
