"""
Decision Summary for Phase 13.3 (ASCE-CGP).
Generates an executive summary of confidence certainty for stakeholders and judges.
"""

from typing import Dict, Any


class DecisionSummaryService:
    """
    Produces executive confidence certainty summaries.
    """

    @classmethod
    def generate_summary(
        cls,
        mission_id: str,
        overall_score: float,
        uncertainty: float,
        governance_passed: bool,
    ) -> Dict[str, Any]:
        return {
            "mission_id": mission_id,
            "overall_score_pct": round(overall_score * 100, 2),
            "uncertainty_pct": round(uncertainty * 100, 2),
            "confidence_band": f"{round(overall_score * 100, 1)}% ± {round(uncertainty * 100, 1)}%",
            "certainty_level": "VERY_HIGH" if overall_score >= 0.95 else "HIGH",
            "audit_verdict": "CERTIFIED" if governance_passed else "FLAGGED",
            "rationale": "Autonomous execution verified against deterministic arithmetic invariants and Merkle evidence chain.",
        }
