"""
Agent Request Contracts.
"""

from typing import Any, Dict
from pydantic import BaseModel, Field
from app.agents.messaging.metadata import MessageMetadata


class AgentRequest(BaseModel):
    """Request contract for agent request/response interaction."""

    request_type: str = Field(default="AgentRequest")
    metadata: MessageMetadata = Field(default_factory=MessageMetadata)
    body: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}
