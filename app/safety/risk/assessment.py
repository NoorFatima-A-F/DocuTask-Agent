"""Risk Assessment Engine and Policy Threshold Mapping."""

from typing import List, Optional
from pydantic import BaseModel
from ..gateway.decision import SafetyStatus, ViolationSeverity, SafetyViolation
from .scoring import CompositeRiskScorer, RiskComponentScores, RiskWeights


class RiskAssessmentResult(BaseModel):
    recommended_status: SafetyStatus
    composite_risk_score: float
    component_scores: RiskComponentScores
    requires_human_escalation: bool
    explanation: str


class RiskAssessmentEngine:
    """Maps composite multi-factor risk scores and violation severities to definitive safety actions."""

    def __init__(self, scorer: Optional[CompositeRiskScorer] = None):
        self.scorer = scorer or CompositeRiskScorer()

    def assess(
        self,
        component_scores: RiskComponentScores,
        violations: Optional[List[SafetyViolation]] = None,
    ) -> RiskAssessmentResult:
        violations = violations or []
        score = component_scores.composite_risk

        # 1. Critical violations or extreme score automatically BLOCK
        has_critical = any(v.severity == ViolationSeverity.CRITICAL for v in violations)
        if has_critical or score >= 0.85:
            return RiskAssessmentResult(
                recommended_status=SafetyStatus.BLOCK,
                composite_risk_score=score,
                component_scores=component_scores,
                requires_human_escalation=True,
                explanation="Operation blocked due to critical safety violation or composite risk >= 0.85",
            )

        # 2. High severity violations or high score require ESCALATE / REQUIRE_HUMAN
        has_high = any(v.severity == ViolationSeverity.HIGH for v in violations)
        if has_high or score >= 0.60:
            return RiskAssessmentResult(
                recommended_status=SafetyStatus.REQUIRE_HUMAN,
                composite_risk_score=score,
                component_scores=component_scores,
                requires_human_escalation=True,
                explanation="Operation requires human supervisor approval due to high risk assessment (score >= 0.60)",
            )

        # 3. Medium risk allows with audit
        if score >= 0.30:
            return RiskAssessmentResult(
                recommended_status=SafetyStatus.ALLOW_WITH_AUDIT,
                composite_risk_score=score,
                component_scores=component_scores,
                requires_human_escalation=False,
                explanation="Operation allowed with mandatory compliance audit log (score between 0.30 and 0.60)",
            )

        # 4. Low risk allows unconditionally
        return RiskAssessmentResult(
            recommended_status=SafetyStatus.ALLOW,
            composite_risk_score=score,
            component_scores=component_scores,
            requires_human_escalation=False,
            explanation="Operation approved under normal safety parameters (score < 0.30)",
        )
