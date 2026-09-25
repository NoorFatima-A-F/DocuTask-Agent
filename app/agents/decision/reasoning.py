"""
Decision Reasoning Step Models.
"""

from pydantic import BaseModel


class ReasoningStep(BaseModel):
    step_number: int
    rule_or_policy: str
    outcome: str
    explanation: str
    model_config = {"frozen": True}
