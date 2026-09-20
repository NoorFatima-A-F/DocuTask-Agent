"""
Branching Conditions Models.
"""

from typing import Any, Dict
from pydantic import BaseModel, Field


class BranchCondition(BaseModel):
    """Condition evaluated at runtime for conditional branch traversal."""
    condition_id: str
    expression: str
    context_keys: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}
