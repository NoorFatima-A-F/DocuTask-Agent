"""
Message Acknowledgements.
"""

from enum import Enum
from pydantic import BaseModel, Field


class AckStatus(str, Enum):
    """Acknowledgement status enum."""
    ACK = "ACK"
    NACK = "NACK"
    REJECT = "REJECT"


class MessageAcknowledgement(BaseModel):
    """Acknowledgement message model."""

    message_id: str
    status: AckStatus = Field(default=AckStatus.ACK)
    reason: str = Field(default="")
    model_config = {"frozen": True}
