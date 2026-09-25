"""
Routing Rules.
"""

from pydantic import BaseModel


class RoutingRule(BaseModel):
    message_type: str
    target_topic: str
    model_config = {"frozen": True}
