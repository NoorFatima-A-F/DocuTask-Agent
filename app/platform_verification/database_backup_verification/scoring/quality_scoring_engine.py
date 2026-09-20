"""
Quality Scoring and Enterprise Certification Engine (Part 3G.2B Quality Scoring).
Applies the 8-category weighted scoring model and awards enterprise certification tiers.
"""
from typing import Dict, Any
from app.platform_verification.database_backup_verification.domain.models import (
    DBCertificationTier,
    QualityScorecard,
)
from app.platform_verification.database_backup_verification.domain.interfaces import (
    IQualityScoringEngine,
)


class QualityScoringEngine(IQualityScoringEngine):
    """
    Computes weighted database readiness and recoverability score:
    - Recoverability: 25%
    - Consistency: 20%
    - Integrity: 15%
    - Security: 15%
    - Performance: 10%
    - Compatibility: 5%
    - Automation: 5%
    - Evidence Quality: 5%
    """

    def compute_quality_scorecard(
        self,
        recoverability_score: float,
        consistency_score: float,
        integrity_score: float,
        security_score: float,
        performance_score: float,
        compatibility_score: float,
        automation_score: float,
        evidence_quality_score: float,
        execution_duration_ms: float,
    ) -> QualityScorecard:
        w_rec = 0.25
        w_cons = 0.20
        w_integ = 0.15
        w_sec = 0.15
        w_perf = 0.10
        w_compat = 0.05
        w_auto = 0.05
        w_evid = 0.05

        composite = (
            (recoverability_score * w_rec)
            + (consistency_score * w_cons)
            + (integrity_score * w_integ)
            + (security_score * w_sec)
            + (performance_score * w_perf)
            + (compatibility_score * w_compat)
            + (automation_score * w_auto)
            + (evidence_quality_score * w_evid)
        )

        composite_rounded = round(composite, 2)

        if composite_rounded >= 98.0:
            tier = DBCertificationTier.ENTERPRISE_PLATINUM
            passed = True
        elif composite_rounded >= 95.0:
            tier = DBCertificationTier.ENTERPRISE_CERTIFIED
            passed = True
        elif composite_rounded >= 90.0:
            tier = DBCertificationTier.PRODUCTION_READY
            passed = True
        elif composite_rounded >= 80.0:
            tier = DBCertificationTier.CONDITIONALLY_READY
            passed = False
        elif composite_rounded >= 70.0:
            tier = DBCertificationTier.DEVELOPMENT_GRADE
            passed = False
        else:
            tier = DBCertificationTier.FAILED
            passed = False

        metadata = {
            "standards_compliance": [
                "PostgreSQL Core Reliability Principles",
                "Google SRE Database Reliability Engineering Standards",
                "AWS Well-Architected Framework (Reliability & Security Pillars)",
                "NIST SP 800-34 Contingency Planning & NIST SP 800-86 Forensics",
                "ISO 22301 Business Continuity & ISO/IEC 27001:2022 A.8.13",
                "CIS Controls v8 Safeguard 11 (Data Recovery)",
            ],
            "weights_table": {
                "Recoverability": "25%",
                "Consistency": "20%",
                "Integrity": "15%",
                "Security": "15%",
                "Performance": "10%",
                "Compatibility": "5%",
                "Automation": "5%",
                "Evidence Quality": "5%",
            },
            "certification_bands": {
                "98-100": "Enterprise Platinum",
                "95-97": "Enterprise Certified",
                "90-94": "Production Ready",
                "80-89": "Conditionally Ready",
                "70-79": "Development Grade",
                "<70": "Failed",
            },
        }

        return QualityScorecard(
            recoverability_score=recoverability_score,
            consistency_score=consistency_score,
            integrity_score=integrity_score,
            security_score=security_score,
            performance_score=performance_score,
            compatibility_score=compatibility_score,
            automation_score=automation_score,
            evidence_quality_score=evidence_quality_score,
            composite_score=composite_rounded,
            certification_tier=tier,
            passed=passed,
            execution_duration_ms=execution_duration_ms,
            audit_metadata=metadata,
        )

    def export_scorecard_json(self, scorecard: QualityScorecard) -> Dict[str, Any]:
        return {
            "composite_score": scorecard.composite_score,
            "certification_tier": scorecard.certification_tier.value,
            "passed": scorecard.passed,
            "execution_duration_ms": scorecard.execution_duration_ms,
            "category_scores": {
                "recoverability_score": scorecard.recoverability_score,
                "consistency_score": scorecard.consistency_score,
                "integrity_score": scorecard.integrity_score,
                "security_score": scorecard.security_score,
                "performance_score": scorecard.performance_score,
                "compatibility_score": scorecard.compatibility_score,
                "automation_score": scorecard.automation_score,
                "evidence_quality_score": scorecard.evidence_quality_score,
            },
            "audit_metadata": scorecard.audit_metadata,
        }
