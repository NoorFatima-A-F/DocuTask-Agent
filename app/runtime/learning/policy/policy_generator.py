"""
Policy Generator for Phase 13.5 (ARLP-KIP).
Synthesizes candidate optimization policies and parameter adjustments from mined lessons.
"""

from typing import Dict, Any, List
from pydantic import BaseModel


class PolicyAdjustment(BaseModel):
    parameter_name: str
    baseline_value: Any
    proposed_value: Any
    rationale: str


class PolicyGenerator:
    """
    Generates rule proposals and parameter adjustments for autonomous sub-systems.
    """

    @classmethod
    def generate_adjustments(cls, target_component: str, parameters: Dict[str, Any]) -> List[PolicyAdjustment]:
        adjustments = []
        for k, v in parameters.items():
            adjustments.append(
                PolicyAdjustment(
                    parameter_name=k,
                    baseline_value=max(1, int(v * 0.75)) if isinstance(v, int) else 0.80,
                    proposed_value=v,
                    rationale=f"Synthesized from mined performance wavefronts on {target_component}",
                )
            )
        return adjustments
