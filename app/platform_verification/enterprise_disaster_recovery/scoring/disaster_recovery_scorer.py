"""
Phase 3L: Disaster Recovery Quality Scorer & Certification Engine.
"""

from datetime import datetime, timezone
from typing import Dict, List

from ..domain.models import (
    BaseVerificationReport,
    CategoryScore,
    DisasterRecoveryScorecard,
    DisasterRecoveryTier,
    VerificationStatus,
)


class DisasterRecoveryScorer:
    """Computes weighted multi-dimensional disaster recovery resilience scores and certifications."""

    WEIGHTS = {
        "Backup Reliability": 0.25,
        "Restore Capability": 0.25,
        "Data Integrity": 0.20,
        "Recovery Speed": 0.15,
        "Security": 0.10,
        "Automation": 0.05,
    }

    CATEGORY_MAPPING = {
        "VERIFY-3L.1-DR-ARCHITECTURE": "Backup Reliability",
        "VERIFY-3L.2-BIA": "Recovery Speed",
        "VERIFY-3L.3-RECOVERY-OBJECTIVES": "Recovery Speed",
        "VERIFY-3L.4-DATABASE-RECOVERY": "Data Integrity",
        "VERIFY-3L.5-STORAGE-RECOVERY": "Data Integrity",
        "VERIFY-3L.6-CONFIG-RECOVERY": "Restore Capability",
        "VERIFY-3L.7-SECRET-RECOVERY": "Security",
        "VERIFY-3L.8-SYSTEM-RESTORE": "Restore Capability",
        "VERIFY-3L.9-PITR-RECOVERY": "Restore Capability",
        "VERIFY-3L.10-BACKUP-SECURITY": "Security",
        "VERIFY-3L.11-DR-AUTOMATION": "Automation",
        "VERIFY-3L.12-FAILURE-SIMULATION": "Backup Reliability",
        "VERIFY-3L.13-RECOVERY-OBSERVABILITY": "Backup Reliability",
    }

    def score(
        self,
        reports: List[BaseVerificationReport],
        execution_time_seconds: float = 0.0,
    ) -> DisasterRecoveryScorecard:
        category_checks: Dict[str, List[bool]] = {cat: [] for cat in self.WEIGHTS}

        for report in reports:
            cat = self.CATEGORY_MAPPING.get(report.verifier_id, "Backup Reliability")
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
            tier = DisasterRecoveryTier.ENTERPRISE_DR_READY
            status = VerificationStatus.PASSED
        elif overall_score >= 90.0:
            tier = DisasterRecoveryTier.PRODUCTION_RECOVERY_READY
            status = VerificationStatus.PASSED
        elif overall_score >= 80.0:
            tier = DisasterRecoveryTier.IMPROVEMENT_REQUIRED
            status = VerificationStatus.WARNING
        else:
            tier = DisasterRecoveryTier.FAILED
            status = VerificationStatus.FAILED

        return DisasterRecoveryScorecard(
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
