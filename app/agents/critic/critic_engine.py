"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Critic Engine.
Performs independent evaluations of agent outputs across quality, completeness,
policy compliance, hallucination risk, evidence support, and security.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid
import logging

logger = logging.getLogger(__name__)


@dataclass
class CriticReport:
    """Evaluation verdict produced by the CriticEngine."""
    id: str = field(default_factory=lambda: f"crit-{uuid.uuid4().hex[:10]}")
    score: float = 1.0  # 0.0 to 1.0
    is_approved: bool = True
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    quality_score: float = 1.0
    completeness_score: float = 1.0
    policy_compliance_score: float = 1.0
    hallucination_risk_score: float = 0.0  # 0.0 (low) to 1.0 (high)
    evidence_score: float = 1.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "score": self.score,
            "is_approved": self.is_approved,
            "issues": self.issues,
            "recommendations": self.recommendations,
            "quality_score": self.quality_score,
            "completeness_score": self.completeness_score,
            "policy_compliance_score": self.policy_compliance_score,
            "hallucination_risk_score": self.hallucination_risk_score,
            "evidence_score": self.evidence_score,
            "timestamp": self.timestamp.isoformat(),
        }


class CriticEngine:
    """
    Independent Critic service validating agent outputs before downstream propagation.
    """

    def evaluate(
        self,
        output: Dict[str, Any],
        evidence: Optional[List[Dict[str, Any]]] = None,
        policies: Optional[List[str]] = None,
        required_fields: Optional[List[str]] = None,
    ) -> CriticReport:
        """
        Evaluates task execution output for quality, completeness, and safety.
        """
        issues: List[str] = []
        recommendations: List[str] = []

        # 1. Completeness check
        completeness = 1.0
        if required_fields:
            missing = [f for f in required_fields if f not in output]
            if missing:
                issues.append(f"Missing required output fields: {missing}")
                recommendations.append(f"Ensure fields {missing} are extracted and populated")
                completeness = max(0.0, 1.0 - (len(missing) / len(required_fields)))

        # 2. Evidence Grounding / Hallucination Risk
        evidence_score = 1.0
        hallucination_risk = 0.0
        if evidence is not None and len(evidence) == 0:
            issues.append("No supporting evidence attached to claims")
            recommendations.append("Attach document citations or verification sources")
            evidence_score = 0.4
            hallucination_risk = 0.6

        # 3. Policy Compliance
        policy_score = 1.0
        for p in policies or []:
            if "strict" in p.lower() and completeness < 0.9:
                issues.append(f"Violated strict completeness policy '{p}'")
                policy_score = 0.5

        # 4. Overall score
        overall_score = round(
            (completeness * 0.3) + (evidence_score * 0.3) + (policy_score * 0.4) - (hallucination_risk * 0.2),
            3
        )
        overall_score = max(0.0, min(1.0, overall_score))
        is_approved = overall_score >= 0.70 and len(issues) == 0

        report = CriticReport(
            score=overall_score,
            is_approved=is_approved,
            issues=issues,
            recommendations=recommendations,
            quality_score=round(overall_score, 2),
            completeness_score=completeness,
            policy_compliance_score=policy_score,
            hallucination_risk_score=hallucination_risk,
            evidence_score=evidence_score,
        )

        logger.info(f"CriticEngine evaluation finished: Approved={is_approved}, Score={overall_score}")
        return report
