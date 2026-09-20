"""
Hypothesis Prioritizer (Phase 86C)
=================================
Multi-objective prioritization ranking hypotheses based on
Expected Impact, Feasibility, Confidence, and Risk.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List

from research_validation.hypothesis.hypothesis_model import ScientificHypothesis


@dataclass(frozen=True)
class PrioritizedHypothesis:
    """Hypothesis decorated with multi-objective composite priority rank."""
    hypothesis: ScientificHypothesis
    composite_priority_score: float
    rank: int
    recommendation_verdict: str  # "EXECUTE_IMMEDIATELY", "SCHEDULE_NEXT", "DEFER"


class HypothesisPrioritizer:
    """
    Ranks hypotheses by maximizing Impact and Confidence while penalizing Risk and Runtime.
    """

    @classmethod
    def prioritize(
        cls,
        hypotheses: List[ScientificHypothesis],
        impact_weight: float = 0.40,
        confidence_weight: float = 0.30,
        risk_penalty_weight: float = 0.20,
        runtime_penalty_weight: float = 0.10,
    ) -> List[PrioritizedHypothesis]:
        if not hypotheses:
            return []

        scored: List[PrioritizedHypothesis] = []
        for h in hypotheses:
            runtime_factor = min(1.0, h.estimated_runtime_sec / 300.0)  # normalized to 5 min
            score = (
                impact_weight * h.impact_score
                + confidence_weight * h.confidence_level
                - risk_penalty_weight * h.risk_score
                - runtime_penalty_weight * runtime_factor
            )
            score = max(0.0, min(1.0, score))

            if score >= 0.50:
                verdict = "EXECUTE_IMMEDIATELY"
            elif score >= 0.30:
                verdict = "SCHEDULE_NEXT"
            else:
                verdict = "DEFER"

            scored.append(PrioritizedHypothesis(
                hypothesis=h,
                composite_priority_score=score,
                rank=0,
                recommendation_verdict=verdict,
            ))

        scored.sort(key=lambda p: p.composite_priority_score, reverse=True)
        ranked = [
            PrioritizedHypothesis(
                hypothesis=p.hypothesis,
                composite_priority_score=p.composite_priority_score,
                rank=idx + 1,
                recommendation_verdict=p.recommendation_verdict,
            )
            for idx, p in enumerate(scored)
        ]
        return ranked
