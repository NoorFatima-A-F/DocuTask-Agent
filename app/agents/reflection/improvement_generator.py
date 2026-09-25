"""
Improvement Generator.
Generates concrete improvement directives from self-critiques and evaluation scores.
"""

from typing import List
from pydantic import BaseModel
from app.agents.reflection.evaluation import EvaluationReport
from app.agents.reflection.self_critique import SelfCritique


class ImprovementDirective(BaseModel):
    """Specific directive describing what to improve in future execution runs."""
    target_area: str
    directive: str
    priority: str = "MEDIUM"  # LOW, MEDIUM, HIGH, URGENT
    expected_gain: str

    model_config = {"frozen": True}


class ImprovementGenerator:
    """Derives high-level strategic improvement directives from reflection findings."""

    def generate_improvements(
        self,
        critique: SelfCritique,
        evaluation: EvaluationReport
    ) -> List[ImprovementDirective]:
        """Synthesizes improvement directives across quality and efficiency dimensions."""
        directives: List[ImprovementDirective] = []

        if evaluation.overall_score < 0.8:
            directives.append(ImprovementDirective(
                target_area="OVERALL_QUALITY",
                directive="Introduce multi-candidate planning to select highest confidence graph.",
                priority="HIGH",
                expected_gain="Improves overall execution score above 0.80 benchmark."
            ))

        for w in evaluation.key_weaknesses:
            directives.append(ImprovementDirective(
                target_area="OPERATIONAL",
                directive=f"Remediate weakness: {w}",
                priority="MEDIUM",
                expected_gain="Mitigates observed performance degradation."
            ))

        for opp in critique.improvement_opportunities:
            directives.append(ImprovementDirective(
                target_area="COGNITIVE",
                directive=opp,
                priority="MEDIUM",
                expected_gain="Enhances reasoning rigor and reduces plan revisions."
            ))

        return directives
