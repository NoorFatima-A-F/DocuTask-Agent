"""
Database Certification and Readiness Scoring Engine (Part 3G.2B).
Applies exact enterprise weights across the 7 evaluation categories and awards certification.
"""
from typing import Dict, Any
from app.platform_verification.database_backup_verification.domain.models import (
    DBCertificationTier,
    DatabaseReadinessScorecard,
)
from app.platform_verification.database_backup_verification.domain.interfaces import (
    IDatabaseCertificationEngine,
)


class DatabaseCertificationEngine(IDatabaseCertificationEngine):
    """
    Calculates weighted composite database recovery certification score:
    - Recoverability: 30%
    - Integrity: 20%
    - Consistency: 15%
    - Performance: 10%
    - Security: 15%
    - Compatibility: 5%
    - Automation: 5%
    """

    def compute_scorecard(
        self,
        recoverability_score: float,
        integrity_score: float,
        consistency_score: float,
        performance_score: float,
        security_score: float,
        compatibility_score: float,
        automation_score: float,
        execution_duration_ms: float,
    ) -> DatabaseReadinessScorecard:
        w_rec = 0.30
        w_integ = 0.20
        w_cons = 0.15
        w_perf = 0.10
        w_sec = 0.15
        w_compat = 0.05
        w_auto = 0.05

        composite = (
            (recoverability_score * w_rec)
            + (integrity_score * w_integ)
            + (consistency_score * w_cons)
            + (performance_score * w_perf)
            + (security_score * w_sec)
            + (compatibility_score * w_compat)
            + (automation_score * w_auto)
        )

        composite_rounded = round(composite, 2)

        if composite_rounded >= 95.0:
            tier = DBCertificationTier.ENTERPRISE_CERTIFIED
            passed = True
        elif composite_rounded >= 90.0:
            tier = DBCertificationTier.PRODUCTION_READY
            passed = True
        elif composite_rounded >= 80.0:
            tier = DBCertificationTier.CONDITIONALLY_READY
            passed = False
        elif composite_rounded >= 70.0:
            tier = DBCertificationTier.DEVELOPMENT_QUALITY
            passed = False
        else:
            tier = DBCertificationTier.FAILED
            passed = False

        metadata = {
            "standards_compliance": [
                "PostgreSQL High Availability & DR Best Practices",
                "Google SRE Database Reliability Principles",
                "AWS Well-Architected Reliability Pillar for RDS/Aurora",
                "NIST SP 800-34 Rev. 1 (Contingency Planning)",
                "ISO 22301 (Business Continuity Management)",
                "ISO/IEC 27001:2022 (A.8.13 Information Backup)",
                "CIS Controls v8 Safeguard 11 (Data Recovery)",
            ],
            "weights_table": {
                "Recoverability": "30%",
                "Integrity": "20%",
                "Consistency": "15%",
                "Performance": "10%",
                "Security": "15%",
                "Compatibility": "5%",
                "Automation": "5%",
            },
        }

        return DatabaseReadinessScorecard(
            recoverability_score=recoverability_score,
            integrity_score=integrity_score,
            consistency_score=consistency_score,
            performance_score=performance_score,
            security_score=security_score,
            compatibility_score=compatibility_score,
            automation_score=automation_score,
            composite_score=composite_rounded,
            certification_tier=tier,
            passed=passed,
            execution_duration_ms=execution_duration_ms,
            audit_metadata=metadata,
        )

    def export_scorecard_json(self, scorecard: DatabaseReadinessScorecard) -> Dict[str, Any]:
        return {
            "composite_score": scorecard.composite_score,
            "certification_tier": scorecard.certification_tier.value,
            "passed": scorecard.passed,
            "execution_duration_ms": scorecard.execution_duration_ms,
            "category_scores": {
                "recoverability_score": scorecard.recoverability_score,
                "integrity_score": scorecard.integrity_score,
                "consistency_score": scorecard.consistency_score,
                "performance_score": scorecard.performance_score,
                "security_score": scorecard.security_score,
                "compatibility_score": scorecard.compatibility_score,
                "automation_score": scorecard.automation_score,
            },
            "audit_metadata": scorecard.audit_metadata,
        }
