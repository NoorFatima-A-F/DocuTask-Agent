"""
Planning Dynamic Branch Routing Models.
"""

from typing import Optional
from pydantic import BaseModel, Field


class PlanRouting(BaseModel):
    """Dynamic routing decision mapping execution state to target node branch."""
    routing_id: str
    current_node_id: str
    selected_target_node_id: str
    routing_reason: Optional[str] = Field(default=None)
    model_config = {"frozen": True}
