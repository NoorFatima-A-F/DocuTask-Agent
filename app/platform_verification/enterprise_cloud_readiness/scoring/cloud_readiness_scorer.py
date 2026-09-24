"""
Phase 3M: Cloud Readiness Quality Scorer & Certification Engine.
"""

from datetime import datetime, timezone
from typing import Dict, List

from ..domain.models import (
    BaseVerificationReport,
    CategoryScore,
    CloudReadinessScorecard,
    CloudReadinessTier,
    VerificationStatus,
)


class CloudReadinessScorer:
    """Computes weighted multi-dimensional cloud readiness scores and certifications across 7 engineering pillars."""

    WEIGHTS = {
        "Container Compatibility": 0.20,
        "Scalability": 0.20,
        "Security": 0.20,
        "Infrastructure Automation": 0.15,
        "Storage & Database Readiness": 0.10,
        "Observability": 0.10,
        "Portability": 0.05,
    }

    CATEGORY_MAPPING = {
        "VERIFY-3M.1-CLOUD-ARCH": "Container Compatibility",
        "VERIFY-3M.2-CONTAINER-CLOUD": "Container Compatibility",
        "VERIFY-3M.3-COMPUTE-RESOURCE": "Scalability",
        "VERIFY-3M.4-CLOUD-NETWORKING": "Security",
        "VERIFY-3M.5-CLOUD-STORAGE": "Storage & Database Readiness",
        "VERIFY-3M.6-MANAGED-DB": "Storage & Database Readiness",
        "VERIFY-3M.7-WORKER-SCALING": "Scalability",
        "VERIFY-3M.8-AUTOSCALING": "Scalability",
        "VERIFY-3M.9-CLOUD-SECRETS": "Security",
        "VERIFY-3M.10-CLOUD-OBSERVABILITY": "Observability",
        "VERIFY-3M.11-IAC": "Infrastructure Automation",
        "VERIFY-3M.12-KUBERNETES-READINESS": "Infrastructure Automation",
        "VERIFY-3M.13-CLOUD-SECURITY": "Security",
        "VERIFY-3M.14-MULTI-CLOUD": "Portability",
        "VERIFY-3M.15-MIGRATION-SIM": "Infrastructure Automation",
    }

    def score(
        self,
        reports: List[BaseVerificationReport],
        execution_time_seconds: float = 0.0,
    ) -> CloudReadinessScorecard:
        category_checks: Dict[str, List[bool]] = {cat: [] for cat in self.WEIGHTS}

        for report in reports:
            cat = self.CATEGORY_MAPPING.get(report.verifier_id, "Container Compatibility")
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
            tier = CloudReadinessTier.CLOUD_NATIVE_READY
            status = VerificationStatus.PASSED
        elif overall_score >= 90.0:
            tier = CloudReadinessTier.CLOUD_PRODUCTION_READY
            status = VerificationStatus.PASSED
        elif overall_score >= 80.0:
            tier = CloudReadinessTier.MIGRATION_REQUIRED
            status = VerificationStatus.WARNING
        else:
            tier = CloudReadinessTier.NOT_READY
            status = VerificationStatus.FAILED

        return CloudReadinessScorecard(
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
