"""
Phase 3N: Infrastructure Security Quality Scorer & Certification Engine.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..domain.models import (
    BaseVerificationReport,
    CategoryScore,
    SecurityCertificationTier,
    SecurityScorecard,
    VerificationStatus,
)


class InfrastructureSecurityScorer:
    """Computes weighted multi-dimensional infrastructure security scores and certifications across 8 engineering pillars."""

    WEIGHTS = {
        "Identity & Access Security": 0.20,
        "Container Security": 0.15,
        "Network Security": 0.15,
        "Secret Protection": 0.15,
        "Supply Chain Security": 0.10,
        "Data Security": 0.10,
        "AI Security": 0.10,
        "Monitoring": 0.05,
    }

    CATEGORY_MAPPING = {
        "VERIFY-3N.1-SEC-ARCH": "Identity & Access Security",
        "VERIFY-3N.2-THREAT-MODEL": "Identity & Access Security",
        "VERIFY-3N.3-CONTAINER-SEC": "Container Security",
        "VERIFY-3N.4-SUPPLY-CHAIN": "Supply Chain Security",
        "VERIFY-3N.5-VULN-MGMT": "Supply Chain Security",
        "VERIFY-3N.6-SECRET-SEC": "Secret Protection",
        "VERIFY-3N.7-IAM-SEC": "Identity & Access Security",
        "VERIFY-3N.8-NETWORK-SEC": "Network Security",
        "VERIFY-3N.9-SERVICE-SEC": "Network Security",
        "VERIFY-3N.10-API-SEC": "Network Security",
        "VERIFY-3N.11-DATABASE-SEC": "Data Security",
        "VERIFY-3N.12-STORAGE-SEC": "Data Security",
        "VERIFY-3N.13-AI-SEC": "AI Security",
        "VERIFY-3N.14-CICD-SEC": "Secret Protection",
        "VERIFY-3N.15-ATTACK-SIM": "Container Security",
        "VERIFY-3N.16-SEC-MONITORING": "Monitoring",
    }

    def score(
        self,
        reports: List[BaseVerificationReport],
        execution_time_seconds: float = 0.0,
    ) -> SecurityScorecard:
        category_checks: Dict[str, List[bool]] = {cat: [] for cat in self.WEIGHTS}

        for report in reports:
            cat = self.CATEGORY_MAPPING.get(report.verifier_id, "Identity & Access Security")
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
            tier = SecurityCertificationTier.ENTERPRISE_SECURITY_READY
            status = VerificationStatus.PASSED
        elif overall_score >= 90.0:
            tier = SecurityCertificationTier.PRODUCTION_SECURE
            status = VerificationStatus.PASSED
        elif overall_score >= 80.0:
            tier = SecurityCertificationTier.IMPROVEMENTS_REQUIRED
            status = VerificationStatus.WARNING
        else:
            tier = SecurityCertificationTier.FAILED
            status = VerificationStatus.FAILED

        return SecurityScorecard(
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
