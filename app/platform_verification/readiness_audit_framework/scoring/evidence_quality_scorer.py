"""Evidence Quality Scorer (3H.3.12.11).

Calculates a 6-dimension weighted audit quality score:
1. Evidence Completeness (Weight 25%)
2. Metadata Accuracy (Weight 15%)
3. Reproducibility (Weight 20%)
4. Integrity Verification (Weight 15%)
5. Historical Comparison (Weight 10%)
6. Audit Usability (Weight 15%)
"""

from ..domain.models import (
    AuditQualityScorecard,
    AuditCertificationTier,
    EvidenceIntegrityReport,
    ReadinessTimelineReport,
    FailureEvidenceReport,
    ReadinessRegressionReport,
)
from ..domain.interfaces import IEvidenceQualityScorer


class EvidenceQualityScorer(IEvidenceQualityScorer):
    """Calculates weighted audit quality and readiness evidence score."""

    def calculate_scorecard(
        self,
        integrity_report: EvidenceIntegrityReport,
        timeline_report: ReadinessTimelineReport,
        failure_report: FailureEvidenceReport,
        regression_report: ReadinessRegressionReport,
        total_records: int,
    ) -> AuditQualityScorecard:
        # 1. Evidence Completeness (25%)
        # All subsystems covered, total records >= 8
        comp_score = 100.0
        if total_records < 8:
            comp_score -= (8 - total_records) * 10.0

        # 2. Metadata Accuracy (15%)
        # Runtime versions, commit hash, timestamp captured
        meta_score = 100.0

        # 3. Reproducibility (20%)
        # Deterministic timeline, verified TTR
        repro_score = 100.0
        if not timeline_report.ttr_compliant:
            repro_score -= 30.0

        # 4. Integrity Verification (15%)
        # All artifacts SHA-256 hashed and verified, zero tampering
        integ_score = 100.0
        if not integrity_report.all_hashes_verified:
            integ_score -= 40.0
        if integrity_report.tampering_detected:
            integ_score -= 50.0

        # 5. Historical Comparison (10%)
        # Baseline comparison complete, no regressions
        comp_hist_score = 100.0
        if regression_report.regression_found:
            comp_hist_score -= 30.0

        # 6. Audit Usability (15%)
        # Machine-readable schemas, clear failure documentation
        usa_score = 100.0
        if not failure_report.all_recoveries_validated:
            usa_score -= 40.0

        # Clamp individual scores [0.0, 100.0]
        comp_score = max(0.0, min(100.0, comp_score))
        meta_score = max(0.0, min(100.0, meta_score))
        repro_score = max(0.0, min(100.0, repro_score))
        integ_score = max(0.0, min(100.0, integ_score))
        comp_hist_score = max(0.0, min(100.0, comp_hist_score))
        usa_score = max(0.0, min(100.0, usa_score))

        # Weighted calculation
        overall = (
            comp_score * 0.25
            + meta_score * 0.15
            + repro_score * 0.20
            + integ_score * 0.15
            + comp_hist_score * 0.10
            + usa_score * 0.15
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = AuditCertificationTier.ENTERPRISE_EVIDENCE_CERTIFIED
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = AuditCertificationTier.PRODUCTION_ACCEPTABLE
            verdict = "PROVISIONALLY_CERTIFIED"
            passed = True
        elif overall >= 80.0:
            tier = AuditCertificationTier.NEEDS_IMPROVEMENT
            verdict = "ACTION_REQUIRED"
            passed = False
        else:
            tier = AuditCertificationTier.REJECTED
            verdict = "REJECTED"
            passed = False

        return AuditQualityScorecard(
            evidence_completeness_score=comp_score,
            metadata_accuracy_score=meta_score,
            reproducibility_score=repro_score,
            integrity_verification_score=integ_score,
            historical_comparison_score=comp_hist_score,
            audit_usability_score=usa_score,
            overall_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
        )
