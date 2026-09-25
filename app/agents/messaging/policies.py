"""
Messaging Subsystem Policies.
"""

from pydantic import BaseModel, Field
from app.agents.messaging.delivery import DeliveryPolicy
from app.agents.messaging.retry import MessageRetryPolicy


class MessagingPolicy(BaseModel):
    """Aggregate policy for messaging dispatch."""

    delivery: DeliveryPolicy = Field(default_factory=DeliveryPolicy)
    retry: MessageRetryPolicy = Field(default_factory=MessageRetryPolicy)
    model_config = {"frozen": True}
