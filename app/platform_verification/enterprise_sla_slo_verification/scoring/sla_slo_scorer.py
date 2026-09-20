"""
Phase 3J.10: Enterprise SLA/SLO Quality Scorer & Certification Engine.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..domain.models import (
    BaseVerificationReport,
    CategoryScore,
    EnterprisePerformanceReliabilityTier,
    SLASLOScorecard,
    VerificationStatus,
)


class SLASLOScorer:
    """Computes weighted multi-dimensional performance reliability scores and certifications."""

    WEIGHTS = {
        "SLA Definition": 0.15,
        "SLO Implementation": 0.20,
        "Continuous Monitoring": 0.20,
        "Regression Detection": 0.15,
        "Incident Handling": 0.15,
        "Evidence Quality": 0.15,
    }

    # Category mappings from verifier IDs
    CATEGORY_MAPPING = {
        "VERIFY-3J.10.1-SLA-DEFINITION": "SLA Definition",
        "VERIFY-3J.10.2-SLO-IMPLEMENTATION": "SLO Implementation",
        "VERIFY-3J.10.3-ERROR-BUDGET": "SLO Implementation",
        "VERIFY-3J.10.4-CONTINUOUS-MONITORING": "Continuous Monitoring",
        "VERIFY-3J.10.5-REGRESSION-DETECTION": "Regression Detection",
        "VERIFY-3J.10.6-LONG-RUNNING-RELIABILITY": "Continuous Monitoring",
        "VERIFY-3J.10.7-PERFORMANCE-ALERTS": "Incident Handling",
        "VERIFY-3J.10.8-INCIDENT-SIMULATION": "Incident Handling",
        "VERIFY-3J.10.9-PERFORMANCE-RECOVERY": "Incident Handling",
        "VERIFY-3J.10.10-DASHBOARD-VALIDATION": "Continuous Monitoring",
        "VERIFY-3J.10.11-PERFORMANCE-GOVERNANCE": "Regression Detection",
        "VERIFY-3J.10.12-CICD-PERFORMANCE-PIPELINE": "Evidence Quality",
    }

    def score(
        self,
        reports: List[BaseVerificationReport],
        execution_time_seconds: float = 0.0,
    ) -> SLASLOScorecard:
        category_checks: Dict[str, List[bool]] = {cat: [] for cat in self.WEIGHTS}

        for report in reports:
            cat = self.CATEGORY_MAPPING.get(report.verifier_id, "Evidence Quality")
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
            tier = EnterprisePerformanceReliabilityTier.ENTERPRISE_PERFORMANCE_RELIABILITY_READY
            status = VerificationStatus.PASSED
        elif overall_score >= 90.0:
            tier = EnterprisePerformanceReliabilityTier.PRODUCTION_PERFORMANCE_READY
            status = VerificationStatus.PASSED
        elif overall_score >= 80.0:
            tier = EnterprisePerformanceReliabilityTier.NEEDS_IMPROVEMENT
            status = VerificationStatus.WARNING
        else:
            tier = EnterprisePerformanceReliabilityTier.FAILED
            status = VerificationStatus.FAILED

        return SLASLOScorecard(
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
