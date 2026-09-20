"""
Phase 3K: Enterprise Chaos Engineering Quality Scorer & Certification Engine.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..domain.models import (
    BaseVerificationReport,
    CategoryScore,
    ChaosResilienceTier,
    ChaosScorecard,
    VerificationStatus,
)


class ChaosScorer:
    """Computes weighted multi-dimensional chaos engineering scores and certifications."""

    WEIGHTS = {
        "Failure Detection": 0.25,
        "Recovery Capability": 0.25,
        "Data Integrity": 0.20,
        "Observability": 0.15,
        "Automation": 0.10,
        "Safety Controls": 0.05,
    }

    CATEGORY_MAPPING = {
        "VERIFY-3K.1-CHAOS-READINESS": "Failure Detection",
        "VERIFY-3K.2-CONTAINER-FAILURE": "Recovery Capability",
        "VERIFY-3K.3-DATABASE-FAILURE": "Data Integrity",
        "VERIFY-3K.4-QUEUE-FAILURE": "Recovery Capability",
        "VERIFY-3K.5-NETWORK-FAILURE": "Failure Detection",
        "VERIFY-3K.6-AI-PROVIDER-FAILURE": "Failure Detection",
        "VERIFY-3K.7-RESOURCE-EXHAUSTION": "Safety Controls",
        "VERIFY-3K.8-WORKER-AGENT-FAILURE": "Failure Detection",
        "VERIFY-3K.9-CASCADING-FAILURE": "Recovery Capability",
        "VERIFY-3K.10-CHAOS-AUTOMATION-PIPELINE": "Automation",
        "VERIFY-3K.11-CHAOS-OBSERVABILITY": "Observability",
        "VERIFY-3K.12-CHAOS-REPORTING": "Safety Controls",
    }

    def score(
        self,
        reports: List[BaseVerificationReport],
        execution_time_seconds: float = 0.0,
    ) -> ChaosScorecard:
        category_checks: Dict[str, List[bool]] = {cat: [] for cat in self.WEIGHTS}

        for report in reports:
            cat = self.CATEGORY_MAPPING.get(report.verifier_id, "Failure Detection")
            for check in report.checks:
                category_checks[cat].append(check.passed)

        categories: Dict[str, CategoryScore] = {}
        total_weighted_score = 0.0
        total_passed = 0
        total_evaluated = 0

        for cat_name, weight in self.WEIGHTS.items():
            checks_list = category_checks.get(cat_name, [])
            cat_passed = sum(1 for p in checks_list if p)
            cat_total = len(checks_list)
            cat_score = (cat_passed / cat_total * 100.0) if cat_total > 0 else 100.0
            contribution = cat_score * weight

            categories[cat_name] = CategoryScore(
                name=cat_name,
                weight=weight,
                score=round(cat_score, 2),
                contribution=round(contribution, 2),
                checks_passed=cat_passed,
                total_checks=cat_total,
                status=VerificationStatus.PASSED if cat_score >= 80.0 else VerificationStatus.FAILED,
            )

            total_weighted_score += contribution
            total_passed += cat_passed
            total_evaluated += cat_total

        overall_score = round(total_weighted_score, 2)

        if overall_score >= 95.0:
            tier = ChaosResilienceTier.CHAOS_RESILIENT
            status = VerificationStatus.PASSED
        elif overall_score >= 90.0:
            tier = ChaosResilienceTier.PRODUCTION_RESILIENT
            status = VerificationStatus.PASSED
        elif overall_score >= 80.0:
            tier = ChaosResilienceTier.NEEDS_IMPROVEMENT
            status = VerificationStatus.WARNING
        else:
            tier = ChaosResilienceTier.FAILED
            status = VerificationStatus.FAILED

        return ChaosScorecard(
            overall_score=overall_score,
            certification_tier=tier,
            status=status,
            categories=categories,
            total_verifiers_executed=len(reports),
            total_checks_passed=total_passed,
            total_checks_evaluated=total_evaluated,
            generated_at=datetime.now(timezone.utc).isoformat(),
            execution_time_seconds=execution_time_seconds,
        )
