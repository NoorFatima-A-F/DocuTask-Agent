"""
Phase 3O: Infrastructure Quality Scorer.
"""

from datetime import datetime, timezone
from typing import Dict, List

from ..domain.interfaces import IInfrastructureQualityScorer
from ..domain.models import (
    CategoryQualityScore,
    NormalizedEvidenceItem,
    QualityScorecard,
    VerificationStatus,
)


class InfrastructureQualityScorer(IInfrastructureQualityScorer):
    """
    Computes weighted quality scores across 6 enterprise infrastructure pillars:
    1. Reliability (25%)
    2. Security (20%)
    3. Scalability (20%)
    4. Observability (15%)
    5. Deployment Quality (10%)
    6. Recovery Capability (10%)
    """

    WEIGHTS = {
        "Reliability": 0.25,
        "Security": 0.20,
        "Scalability": 0.20,
        "Observability": 0.15,
        "Deployment Quality": 0.10,
        "Recovery Capability": 0.10,
    }

    def calculate_score(
        self,
        evidence_items: List[NormalizedEvidenceItem],
        execution_time_seconds: float = 0.0,
    ) -> QualityScorecard:
        # Group evidence by category
        grouped: Dict[str, List[NormalizedEvidenceItem]] = {cat: [] for cat in self.WEIGHTS}
        for item in evidence_items:
            cat = item.category if item.category in self.WEIGHTS else "Reliability"
            grouped[cat].append(item)

        categories: Dict[str, CategoryQualityScore] = {}
        total_weighted_score = 0.0
        total_passed = 0
        total_evaluated = len(evidence_items)

        for cat_name, weight in self.WEIGHTS.items():
            items = grouped[cat_name]
            if items:
                cat_passed = sum(1 for it in items if it.status == VerificationStatus.PASSED)
                cat_total = len(items)
                score_val = (cat_passed / cat_total * 100.0) if cat_total > 0 else 100.0
            else:
                cat_passed = 0
                cat_total = 0
                score_val = 100.0

            contribution = score_val * weight
            total_weighted_score += contribution
            total_passed += cat_passed

            categories[cat_name] = CategoryQualityScore(
                category=cat_name,
                weight=weight,
                score=round(score_val, 2),
                contribution=round(contribution, 2),
                passed_items=cat_passed,
                total_items=cat_total,
                status=VerificationStatus.PASSED if score_val >= 80.0 else VerificationStatus.FAILED,
            )

        overall_score = round(total_weighted_score, 2)

        if overall_score >= 95.0:
            grade = "ENTERPRISE_READY"
        elif overall_score >= 90.0:
            grade = "PRODUCTION_READY"
        elif overall_score >= 80.0:
            grade = "TESTING_READY"
        elif overall_score >= 60.0:
            grade = "DEVELOPMENT_READY"
        else:
            grade = "FAILED"

        return QualityScorecard(
            overall_score=overall_score,
            grade=grade,
            categories=categories,
            total_evidence_evaluated=total_evaluated,
            total_evidence_passed=total_passed,
            calculated_at=datetime.now(timezone.utc).isoformat(),
            execution_time_seconds=execution_time_seconds,
        )
