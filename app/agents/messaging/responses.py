"""
Agent Response Contracts.
"""

from typing import Any, Optional
from pydantic import BaseModel, Field
from app.agents.messaging.metadata import MessageMetadata


class AgentResponse(BaseModel):
    """Response contract for agent request/response interaction."""

    request_id: str
    metadata: MessageMetadata = Field(default_factory=MessageMetadata)
    success: bool = Field(default=True)
    body: Optional[Any] = Field(default=None)

    model_config = {"frozen": True}
