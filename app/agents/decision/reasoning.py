"""
Decision Reasoning Step Models.
"""

from typing import Any, Dict
from pydantic import BaseModel, Field


class ReasoningStep(BaseModel):
    step_number: int
    rule_or_policy: str
    outcome: str
    explanation: str
    model_config = {"frozen": True}
