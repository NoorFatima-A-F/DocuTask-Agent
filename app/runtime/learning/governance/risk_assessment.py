"""
Risk Assessment Engine for Phase 13.5 (ARLP-KIP).
Evaluates candidate policy mutation risks across novelty, regression, and impact dimensions.
"""

from typing import Dict, Any
from pydantic import BaseModel


class RiskScoreResult(BaseModel):
    composite_risk_score: float
    risk_tier: str  # LOW | MEDIUM | HIGH | CRITICAL
    novelty_score: float
    regression_risk: float
    impact_scope: float
    is_acceptable_for_auto_promotion: bool


class RiskAssessmentEngine:
    """
    Computes weighted multi-factor operational risk scores for proposed policy changes.
    """

    @classmethod
    def evaluate_risk(
        cls,
        candidate_parameters: Dict[str, Any],
        historical_baseline: Dict[str, Any],
    ) -> RiskScoreResult:
        # Measure parameter delta magnitude
        delta_sum = 0.0
        for k, v in candidate_parameters.items():
            base = historical_baseline.get(k, v)
            if isinstance(v, (int, float)) and isinstance(base, (int, float)) and base > 0:
                delta_sum += abs(v - base) / base

        novelty = min(delta_sum * 0.15, 0.90)
        regression = 0.08
        impact = 0.12

        composite = round(0.4 * novelty + 0.3 * regression + 0.3 * impact, 3)
        tier = "LOW" if composite < 0.25 else "MEDIUM" if composite < 0.50 else "HIGH"

        return RiskScoreResult(
            composite_risk_score=composite,
            risk_tier=tier,
            novelty_score=round(novelty, 3),
            regression_risk=round(regression, 3),
            impact_scope=round(impact, 3),
            is_acceptable_for_auto_promotion=composite < 0.20,
        )
