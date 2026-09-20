"""
Message Envelope Model.
Wraps message payloads with metadata, headers, signatures, and routing attributes.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from app.agents.messaging.metadata import MessageMetadata


class MessageEnvelope(BaseModel):
    """Reusable Message Envelope wrapping strongly typed message payload."""

    metadata: MessageMetadata = Field(default_factory=MessageMetadata)
    payload_type: str = Field(default="AgentMessage")
    payload: Any
    headers: Dict[str, str] = Field(default_factory=dict)
    signature: Optional[str] = Field(default=None)

    model_config = {"frozen": True}
