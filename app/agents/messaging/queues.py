"""
Message Queues Domain Model.
"""

from pydantic import BaseModel, Field


class MessageQueue(BaseModel):
    queue_name: str
    max_capacity: int = Field(default=1000, ge=1)
    model_config = {"frozen": True}
