"""
Phase 3J.12: Continuous Performance Engineering Quality Scorer & Certification Engine.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..domain.models import (
    BaseVerificationReport,
    CategoryScore,
    ContinuousPerformanceEngineeringTier,
    ContinuousPerformanceScorecard,
    VerificationStatus,
)


class ContinuousPerformanceScorer:
    """Computes weighted multi-dimensional performance engineering scores and certifications."""

    WEIGHTS = {
        "Baseline accuracy": 0.15,
        "Benchmark automation": 0.20,
        "Regression detection": 0.25,
        "CI/CD integration": 0.15,
        "Trend analysis": 0.10,
        "Performance knowledge": 0.15,
    }

    CATEGORY_MAPPING = {
        "VERIFY-3J.12.1-CONT-PERF-ARCH": "Benchmark automation",
        "VERIFY-3J.12.2-BASELINE-MANAGEMENT": "Baseline accuracy",
        "VERIFY-3J.12.3-BENCHMARK-EXECUTION": "Benchmark automation",
        "VERIFY-3J.12.4-REGRESSION-ENGINE": "Regression detection",
        "VERIFY-3J.12.5-CHANGE-IMPACT": "Regression detection",
        "VERIFY-3J.12.6-QUALITY-GATES": "Regression detection",
        "VERIFY-3J.12.7-MULTI-ENV-COMPARISON": "Trend analysis",
        "VERIFY-3J.12.8-KNOWLEDGE-REPOSITORY": "Performance knowledge",
        "VERIFY-3J.12.9-TREND-ANALYSIS": "Trend analysis",
        "VERIFY-3J.12.10-DASHBOARD-VALIDATION": "Trend analysis",
        "VERIFY-3J.12.11-CICD-INTEGRATION": "CI/CD integration",
        "VERIFY-3J.12.12-EXPERIMENT-TRACKING": "Performance knowledge",
    }

    def score(
        self,
        reports: List[BaseVerificationReport],
        execution_time_seconds: float = 0.0,
    ) -> ContinuousPerformanceScorecard:
        category_checks: Dict[str, List[bool]] = {cat: [] for cat in self.WEIGHTS}

        for report in reports:
            cat = self.CATEGORY_MAPPING.get(report.verifier_id, "Benchmark automation")
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
            tier = ContinuousPerformanceEngineeringTier.CONTINUOUS_PERFORMANCE_ENGINEERING_READY
            status = VerificationStatus.PASSED
        elif overall_score >= 90.0:
            tier = ContinuousPerformanceEngineeringTier.PRODUCTION_PERFORMANCE_GOVERNANCE_READY
            status = VerificationStatus.PASSED
        elif overall_score >= 80.0:
            tier = ContinuousPerformanceEngineeringTier.NEEDS_IMPROVEMENT
            status = VerificationStatus.WARNING
        else:
            tier = ContinuousPerformanceEngineeringTier.FAILED
            status = VerificationStatus.FAILED

        return ContinuousPerformanceScorecard(
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
