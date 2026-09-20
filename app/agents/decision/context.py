"""
Decision Context Model.
"""

from typing import Any, Dict, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class DecisionContext(BaseModel):
    """Context parameters provided during decision evaluation requests."""

    document_id: Optional[UUID] = Field(default=None)
    user_id: Optional[UUID] = Field(default=None)
    action_type: str = Field(default="EXECUTE_TASK")
    document_type: str = Field(default="generic")
    estimated_cost_usd: float = Field(default=0.0, ge=0.0)
    parameters: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}
