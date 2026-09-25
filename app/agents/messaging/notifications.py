"""
Agent Notification Contracts.
"""

from typing import Any, Dict
from pydantic import BaseModel, Field
from app.agents.messaging.metadata import MessageMetadata


class AgentNotification(BaseModel):
    """Notification contract for asynchronous one-way message dispatches."""

    notification_type: str = Field(default="AgentNotification")
    metadata: MessageMetadata = Field(default_factory=MessageMetadata)
    details: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}
