"""
Change Impact Analysis Engine detecting code/prompt/model/dataset changes and triggering invalidation.
"""
from __future__ import annotations
import uuid
from typing import List, Optional
from app.platform_verification.certification_engine.domain.interfaces import (
    IChangeImpactAnalyzer,
    ICertificationEngine,
)
from app.platform_verification.certification_engine.domain.models import (
    CertificationLevel,
    CertificationStatus,
    ChangeImpactReport,
    ChangeType,
)


class EnterpriseChangeImpactAnalyzer(IChangeImpactAnalyzer):
    """Maps system change vectors to affected certification tiers and invalidates outdated certifications."""

    def __init__(self, cert_engine: ICertificationEngine):
        self.cert_engine = cert_engine

    def analyze_change(
        self,
        change_type: ChangeType,
        changed_entity: str,
        version_before: str,
        version_after: str,
        system_id: str,
    ) -> ChangeImpactReport:
        affected_levels: List[CertificationLevel] = []
        required_suites: List[str] = []

        if change_type == ChangeType.PROMPT:
            affected_levels = [
                CertificationLevel.LEVEL_4_SYSTEM_CERTIFIED,
                CertificationLevel.LEVEL_5_PRODUCTION_CERTIFIED,
                CertificationLevel.LEVEL_7_ENTERPRISE_CERTIFIED,
            ]
            required_suites = ["AIQualityEvaluationSuite", "HallucinationBenchmarkSuite"]

        elif change_type == ChangeType.MODEL:
            affected_levels = [
                CertificationLevel.LEVEL_2_COMPONENT_CERTIFIED,
                CertificationLevel.LEVEL_4_SYSTEM_CERTIFIED,
                CertificationLevel.LEVEL_5_PRODUCTION_CERTIFIED,
                CertificationLevel.LEVEL_6_ADVERSARIAL_CERTIFIED,
                CertificationLevel.LEVEL_7_ENTERPRISE_CERTIFIED,
            ]
            required_suites = [
                "FullModelEvaluationSuite",
                "AdversarialSafetySuite",
                "PerformanceRegressionSuite",
            ]

        elif change_type == ChangeType.CODE:
            affected_levels = [
                CertificationLevel.LEVEL_1_DEVELOPMENT_VERIFIED,
                CertificationLevel.LEVEL_3_INTEGRATION_CERTIFIED,
                CertificationLevel.LEVEL_4_SYSTEM_CERTIFIED,
                CertificationLevel.LEVEL_5_PRODUCTION_CERTIFIED,
            ]
            required_suites = ["UnitRegressionSuite", "IntegrationTestSuite", "E2EWorkflowSuite"]

        elif change_type == ChangeType.SECURITY:
            affected_levels = [
                CertificationLevel.LEVEL_6_ADVERSARIAL_CERTIFIED,
                CertificationLevel.LEVEL_7_ENTERPRISE_CERTIFIED,
            ]
            required_suites = ["SecurityPenetrationSuite", "VulnerabilityScanSuite"]

        else:
            affected_levels = [CertificationLevel.LEVEL_5_PRODUCTION_CERTIFIED]
            required_suites = ["FullSystemVerificationSuite"]

        # Invalidate active certifications matching affected levels
        active_certs = getattr(self.cert_engine, "list_certifications", lambda sid: [])(system_id)
        invalidated_ids: List[str] = []

        for cert in active_certs:
            if cert.certification_level in affected_levels and cert.status == CertificationStatus.ACTIVE:
                self.cert_engine.revoke_certification(
                    certification_id=cert.id,
                    reason=f"Automated invalidation due to {change_type.value} change in {changed_entity} ({version_before} -> {version_after})",
                    revoked_by="AutomatedChangeImpactAnalyzer",
                )
                invalidated_ids.append(cert.id)

        return ChangeImpactReport(
            change_id=f"CHG-{uuid.uuid4().hex[:8].upper()}",
            change_type=change_type,
            changed_entity=changed_entity,
            version_before=version_before,
            version_after=version_after,
            affected_certification_levels=affected_levels,
            invalidated_certifications=invalidated_ids,
            required_reverification_suites=required_suites,
        )
