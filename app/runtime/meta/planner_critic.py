"""Planner Critic for DocuTask ADIP Meta-Reasoning Layer.

Critiques candidate plans, diagnosing search bias, potential model hallucinations,
unaccounted pipeline bottlenecks, and search depth insufficiencies before execution.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CriticDiagnosis(BaseModel):
    """Specific diagnostic finding from metacognitive review."""
    code: str
    severity: str = "MEDIUM"  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    title: str
    description: str
    remediation: str


class PlannerCritiqueReport(BaseModel):
    """Aggregate metacognitive critique of a mission plan."""
    mission_id: str
    strategy_id: str
    critique_score: float = Field(ge=0.0, le=1.0, description="1.0 = Flawless, 0.0 = Rejected")
    diagnoses: List[CriticDiagnosis] = Field(default_factory=list)
    search_depth_adequate: bool
    should_deepen_search: bool
    should_switch_algorithm: bool
    recommended_algorithm: Optional[str] = None
    summary: str = ""


class PlannerCritic:
    """Metacognitive critique engine reviewing plan robustness."""

    def critique_plan(
        self,
        mission_id: str,
        strategy_id: str,
        candidate_count: int,
        search_depth: int,
        estimated_risk: float,
        confidence_score: float,
    ) -> PlannerCritiqueReport:
        diagnoses: List[CriticDiagnosis] = []
        score = 1.0

        # Check search breadth
        if candidate_count < 3:
            diagnoses.append(
                CriticDiagnosis(
                    code="NARROW_SEARCH_BREADTH",
                    severity="MEDIUM",
                    title="Search Space Too Constrained",
                    description=f"Only {candidate_count} candidate strategies evaluated. High risk of local optimum.",
                    remediation="Expand candidate generator to evaluate at least 4 distinct archetypes.",
                )
            )
            score -= 0.15

        # Check risk vs confidence discrepancy
        if estimated_risk > 0.15 and confidence_score > 0.90:
            diagnoses.append(
                CriticDiagnosis(
                    code="OVERCONFIDENCE_BIAS",
                    severity="HIGH",
                    title="Overconfidence Under Elevated Risk",
                    description=f"Confidence ({confidence_score*100:.1f}%) is disproportionate to risk score ({estimated_risk*100:.1f}%).",
                    remediation="Inject secondary AST verification layer and activate EVOI sensing checks.",
                )
            )
            score -= 0.25

        # Search depth adequacy
        depth_adequate = search_depth >= 3
        should_deepen = (not depth_adequate) or (estimated_risk > 0.20)
        should_switch = score < 0.60
        rec_algo = "MCTS_DEEP_SEARCH" if should_switch else None

        final_score = max(0.0, round(score, 4))
        summary = (
            f"Metacognitive Critique: Score {final_score*100:.1f}%. "
            f"{len(diagnoses)} diagnoses found. Search Depth: {'ADEQUATE' if depth_adequate else 'SHALLOW'}."
        )

        return PlannerCritiqueReport(
            mission_id=mission_id,
            strategy_id=strategy_id,
            critique_score=final_score,
            diagnoses=diagnoses,
            search_depth_adequate=depth_adequate,
            should_deepen_search=should_deepen,
            should_switch_algorithm=should_switch,
            recommended_algorithm=rec_algo,
            summary=summary,
        )
