"""
Compensation Engine.
Plans and executes semantic compensating actions for completed nodes when rolling back.
"""

from typing import Any, Dict
from pydantic import BaseModel, Field


class CompensatingAction(BaseModel):
    """Semantic compensation instruction to invert or neutralize a task effect."""
    action_id: str
    target_node_id: str
    compensation_type: str = Field(default="DELETE_OR_REVERSE")
    parameters: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}


class CompensationEngine:
    """Calculates compensation actions for nodes requiring reversal."""

    def plan_compensation(self, node_id: str, node_type: str) -> CompensatingAction:
        return CompensatingAction(
            action_id=f"comp_{node_id}",
            target_node_id=node_id,
            compensation_type="REVERSE_STATE",
            parameters={"target_node": node_id, "type": node_type}
        )
