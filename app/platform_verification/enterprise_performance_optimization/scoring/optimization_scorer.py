"""
Phase 3J.11: Intelligent Performance Optimization Quality Scorer & Certification Engine.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..domain.models import (
    AutonomousPerformanceTier,
    BaseVerificationReport,
    CategoryScore,
    OptimizationScorecard,
    VerificationStatus,
)


class OptimizationScorer:
    """Computes weighted multi-dimensional performance optimization scores and certifications."""

    WEIGHTS = {
        "Root cause accuracy": 0.20,
        "Optimization recommendations": 0.20,
        "Auto-scaling capability": 0.15,
        "Predictive planning": 0.15,
        "Automated remediation": 0.15,
        "Safety controls": 0.15,
    }

    CATEGORY_MAPPING = {
        "VERIFY-3J.11.1-INTELLIGENCE-ARCH": "Safety controls",
        "VERIFY-3J.11.2-ROOT-CAUSE-ANALYSIS": "Root cause accuracy",
        "VERIFY-3J.11.3-OPTIMIZATION-RECOMMENDATION": "Optimization recommendations",
        "VERIFY-3J.11.4-INTELLIGENT-AUTOSCALING": "Auto-scaling capability",
        "VERIFY-3J.11.5-DATABASE-OPTIMIZATION": "Optimization recommendations",
        "VERIFY-3J.11.6-AI-PIPELINE-OPTIMIZATION": "Optimization recommendations",
        "VERIFY-3J.11.7-PREDICTIVE-CAPACITY": "Predictive planning",
        "VERIFY-3J.11.8-PERFORMANCE-ANOMALY": "Automated remediation",
        "VERIFY-3J.11.9-AUTOMATED-REMEDIATION": "Automated remediation",
        "VERIFY-3J.11.10-OPTIMIZATION-SAFETY": "Safety controls",
        "VERIFY-3J.11.11-CONTINUOUS-LOOP": "Automated remediation",
        "VERIFY-3J.11.12-CICD-OPTIMIZATION-PIPELINE": "Safety controls",
    }

    def score(
        self,
        reports: List[BaseVerificationReport],
        execution_time_seconds: float = 0.0,
    ) -> OptimizationScorecard:
        category_checks: Dict[str, List[bool]] = {cat: [] for cat in self.WEIGHTS}

        for report in reports:
            cat = self.CATEGORY_MAPPING.get(report.verifier_id, "Safety controls")
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
            tier = AutonomousPerformanceTier.AUTONOMOUS_PERFORMANCE_READY
            status = VerificationStatus.PASSED
        elif overall_score >= 90.0:
            tier = AutonomousPerformanceTier.PRODUCTION_OPTIMIZATION_READY
            status = VerificationStatus.PASSED
        elif overall_score >= 80.0:
            tier = AutonomousPerformanceTier.IMPROVEMENT_REQUIRED
            status = VerificationStatus.WARNING
        else:
            tier = AutonomousPerformanceTier.FAILED
            status = VerificationStatus.FAILED

        return OptimizationScorecard(
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
