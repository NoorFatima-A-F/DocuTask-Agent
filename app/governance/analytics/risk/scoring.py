"""Risk Scoring Formula, Factor Weighting, and Category Taxonomy."""

from enum import Enum
from typing import Dict
from pydantic import BaseModel


class RiskCategory(str, Enum):
    SECURITY_RISK = "Security Risk"
    PRIVACY_RISK = "Privacy Risk"
    COMPLIANCE_RISK = "Compliance Risk"
    MODEL_RISK = "Model Risk"
    PROMPT_RISK = "Prompt Risk"
    DATA_RISK = "Data Risk"
    OPERATIONAL_RISK = "Operational Risk"
    FINANCIAL_RISK = "Financial Risk"


class RiskScoreBreakdown(BaseModel):
    category: RiskCategory
    impact: float = 0.5          # 0.0 to 1.0
    probability: float = 0.5     # 0.0 to 1.0
    exposure: float = 1.0        # 0.0 to 1.0
    calculated_score: float = 0.25
    severity_level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL


class RiskScoringModel:
    """Computes configurable multi-factor risk: Score = Impact x Probability x Exposure."""

    CATEGORY_WEIGHTS: Dict[RiskCategory, float] = {
        RiskCategory.SECURITY_RISK: 1.2,
        RiskCategory.PRIVACY_RISK: 1.1,
        RiskCategory.COMPLIANCE_RISK: 1.1,
        RiskCategory.MODEL_RISK: 1.0,
        RiskCategory.PROMPT_RISK: 1.0,
        RiskCategory.DATA_RISK: 1.0,
        RiskCategory.OPERATIONAL_RISK: 0.9,
        RiskCategory.FINANCIAL_RISK: 1.0,
    }

    @classmethod
    def calculate_score(
        cls,
        category: RiskCategory,
        impact: float,
        probability: float,
        exposure: float = 1.0,
    ) -> RiskScoreBreakdown:
        weight = cls.CATEGORY_WEIGHTS.get(category, 1.0)
        raw_score = impact * probability * exposure * weight
        final_score = min(1.0, max(0.0, raw_score))

        if final_score >= 0.8:
            severity = "CRITICAL"
        elif final_score >= 0.6:
            severity = "HIGH"
        elif final_score >= 0.3:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        return RiskScoreBreakdown(
            category=category,
            impact=impact,
            probability=probability,
            exposure=exposure,
            calculated_score=round(final_score, 4),
            severity_level=severity,
        )
