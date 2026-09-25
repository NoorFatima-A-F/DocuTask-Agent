"""
Event Subscription Models.
"""

from pydantic import BaseModel, Field


class EventSubscription(BaseModel):
    subscription_id: str
    event_type: str
    target_topic: str = Field(default="events")
    model_config = {"frozen": True, "arbitrary_types_allowed": True}
