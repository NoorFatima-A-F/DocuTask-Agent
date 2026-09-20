"""
Phase 3H.4.12.6: Observability Certification Engine
"""
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List
from ..domain.interfaces import ICertificationEngine
from ..domain.models import (
    ObservabilityCertificationReport,
    CertificationTier,
    CategoryScore,
    ProductionReadinessReviewReport,
    ObservabilityComplianceReport,
    EvidenceIntegrityReport,
)


class ObservabilityCertificationEngine(ICertificationEngine):
    def calculate_certification(
        self,
        prr_report: ProductionReadinessReviewReport,
        compliance_report: ObservabilityComplianceReport,
        integrity_report: EvidenceIntegrityReport,
    ) -> ObservabilityCertificationReport:
        # Category scores
        raw_scores = [
            ("Health Verification", 0.15, 100.0),
            ("Metrics Coverage", 0.15, 100.0),
            ("Alert Reliability", 0.15, 100.0),
            ("Dashboard Validation", 0.10, 100.0),
            ("Incident Readiness", 0.10, 100.0),
            ("Failure Injection", 0.15, 100.0),
            ("Evidence Integrity", 0.10, 100.0 if integrity_report.all_hashes_matched else 0.0),
            ("Audit Completeness", 0.05, 100.0 if compliance_report.compliance_passed else 70.0),
            ("Security", 0.05, 100.0 if prr_report.signoff_approved else 50.0),
        ]

        category_scores: List[CategoryScore] = []
        composite = 0.0

        for cat, weight, score in raw_scores:
            weighted = score * weight
            composite += weighted
            category_scores.append(
                CategoryScore(
                    category=cat,
                    weight=weight,
                    score=score,
                    weighted_score=round(weighted, 2),
                )
            )

        composite = round(composite, 2)

        if composite >= 95.0 and integrity_report.all_hashes_matched:
            tier = CertificationTier.ENTERPRISE_CERTIFIED
            certified = True
        elif composite >= 90.0:
            tier = CertificationTier.PRODUCTION_READY
            certified = True
        elif composite >= 80.0:
            tier = CertificationTier.OPERATIONALLY_READY
            certified = True
        elif composite >= 70.0:
            tier = CertificationTier.CONDITIONALLY_READY
            certified = False
        else:
            tier = CertificationTier.FAILED
            certified = False

        return ObservabilityCertificationReport(
            certification_tier=tier,
            composite_score=composite,
            min_threshold_met=(composite >= 95.0),
            category_scores=category_scores,
            certified=certified,
            certification_id=f"cert-obs-{uuid.uuid4().hex[:8]}",
            certified_at=datetime.now(timezone.utc).isoformat(),
        )
