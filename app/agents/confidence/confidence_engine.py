"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Confidence Engine.
Calculates composite confidence scores combining validation results,
evidence strength, model consistency, policy compliance, and risk.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class ConfidenceReport:
    """Detailed confidence breakdown and review recommendations."""
    confidence_score: float = 1.0
    evidence_score: float = 1.0
    risk_score: float = 0.0
    verification_score: float = 1.0
    requires_human_review: bool = False
    recommendation_reason: str = ""
    factors: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "confidence_score": self.confidence_score,
            "evidence_score": self.evidence_score,
            "risk_score": self.risk_score,
            "verification_score": self.verification_score,
            "requires_human_review": self.requires_human_review,
            "recommendation_reason": self.recommendation_reason,
            "factors": self.factors,
            "timestamp": self.timestamp.isoformat(),
        }


class ConfidenceEngine:
    """
    Cognitive Confidence Scorer determining whether an AI decision or output
    meets enterprise thresholds or must be escalated for human review.
    """

    def __init__(self, confidence_threshold: float = 0.80, risk_threshold: float = 0.40):
        self.confidence_threshold = confidence_threshold
        self.risk_threshold = risk_threshold

    def calculate_confidence(
        self,
        validation_results: Dict[str, Any],
        evidence_items: Optional[List[Dict[str, Any]]] = None,
        policy_compliance: float = 1.0,
        model_confidence: float = 0.90,
        financial_impact_usd: float = 0.0,
    ) -> ConfidenceReport:
        """
        Computes composite confidence and flags human review requirement if below threshold.
        """
        # 1. Verification score from validation results
        is_valid = validation_results.get("is_valid", True)
        valid_rules_ratio = validation_results.get("passed_rules_ratio", 1.0 if is_valid else 0.4)
        verification_score = float(valid_rules_ratio)

        # 2. Evidence score
        evidence_items = evidence_items or []
        if not evidence_items:
            evidence_score = 0.5
        else:
            supported = sum(1 for e in evidence_items if e.get("supports", True))
            evidence_score = supported / len(evidence_items)

        # 3. Risk calculation
        risk_score = 0.1
        if financial_impact_usd > 10000:
            risk_score += 0.4
        elif financial_impact_usd > 1000:
            risk_score += 0.2
        if not is_valid:
            risk_score += 0.3
        risk_score = min(1.0, risk_score)

        # 4. Composite confidence score
        composite_score = (
            (verification_score * 0.35)
            + (evidence_score * 0.25)
            + (policy_compliance * 0.25)
            + (model_confidence * 0.15)
        )
        composite_score = round(max(0.0, min(1.0, composite_score)), 3)

        # 5. Recommendation
        requires_human = False
        reasons: List[str] = []

        if composite_score < self.confidence_threshold:
            requires_human = True
            reasons.append(f"Confidence score ({composite_score}) below threshold ({self.confidence_threshold})")

        if risk_score >= self.risk_threshold:
            requires_human = True
            reasons.append(f"Risk score ({risk_score}) exceeds risk threshold ({self.risk_threshold})")

        if financial_impact_usd >= 10000:
            requires_human = True
            reasons.append(f"High financial threshold: ${financial_impact_usd} >= $10,000")

        report = ConfidenceReport(
            confidence_score=composite_score,
            evidence_score=round(evidence_score, 3),
            risk_score=round(risk_score, 3),
            verification_score=round(verification_score, 3),
            requires_human_review=requires_human,
            recommendation_reason="; ".join(reasons) if reasons else "Confidence satisfied, autonomous execution permitted",
            factors={
                "verification": verification_score,
                "evidence": evidence_score,
                "policy": policy_compliance,
                "model": model_confidence,
            }
        )

        logger.info(
            f"ConfidenceEngine calculated: Score={composite_score}, Risk={risk_score}, "
            f"RequiresHuman={requires_human}"
        )
        return report
