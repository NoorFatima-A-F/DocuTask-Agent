"""
Routing Rules.
"""

from pydantic import BaseModel, Field


class RoutingRule(BaseModel):
    message_type: str
    target_topic: str
    model_config = {"frozen": True}
