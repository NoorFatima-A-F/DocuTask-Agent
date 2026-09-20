"""
Phase 3I.7.14: Observability Security & Privacy Quality Scorer
Calculates weighted scores across the 6 enterprise security pillars:
1. Sensitive Data Protection (25%)
2. Access Control (20%)
3. Encryption (15%)
4. AI Telemetry Privacy (15%)
5. Compliance Readiness (15%)
6. Incident Response & Containment (10%)
"""
from typing import List
from ..domain.interfaces import IObservabilitySecurityScorer
from ..domain.models import (
    ObservabilityThreatModelReport,
    SensitiveDataReport,
    LogRedactionReport,
    AITelemetryPrivacyReport,
    AccessControlReport,
    TelemetryEncryptionReport,
    TelemetryRetentionReport,
    ObservabilityAuditReport,
    ComplianceMappingReport,
    AttackSimulationReport,
    TelemetryIncidentResponseReport,
    ContinuousSecurityReport,
    SecurityPillarScore,
    ObservabilitySecurityCertificationReport,
    SecurityCertificationTier,
)


class ObservabilitySecurityScorer(IObservabilitySecurityScorer):
    def calculate_certification_score(
        self,
        threat_report: ObservabilityThreatModelReport,
        data_report: SensitiveDataReport,
        redact_report: LogRedactionReport,
        ai_report: AITelemetryPrivacyReport,
        access_report: AccessControlReport,
        encrypt_report: TelemetryEncryptionReport,
        retention_report: TelemetryRetentionReport,
        audit_report: ObservabilityAuditReport,
        compliance_report: ComplianceMappingReport,
        attack_report: AttackSimulationReport,
        incident_report: TelemetryIncidentResponseReport,
        continuous_report: ContinuousSecurityReport,
    ) -> ObservabilitySecurityCertificationReport:
        pillar_scores: List[SecurityPillarScore] = []

        # Pillar 1: Sensitive Data Protection (25%)
        p1_achieved = 100.0 if (
            data_report.zero_sensitive_data_leaked
            and redact_report.all_rules_verified
            and threat_report.critical_risks_unmitigated == 0
        ) else 85.0
        p1_weighted = round((p1_achieved * 25.0) / 100.0, 2)
        pillar_scores.append(
            SecurityPillarScore(
                pillar_name="Sensitive Data Protection & Automated Redaction",
                weight_pct=25.0,
                achieved_score_pct=p1_achieved,
                weighted_score_pct=p1_weighted,
                status="PASSED" if p1_achieved >= 95.0 else "WARNING",
            )
        )

        # Pillar 2: Access Control & Least Privilege (20%)
        p2_achieved = 100.0 if (
            access_report.rbac_enforced
            and access_report.mfa_mandatory_for_admins
            and audit_report.immutability_verified
        ) else 85.0
        p2_weighted = round((p2_achieved * 20.0) / 100.0, 2)
        pillar_scores.append(
            SecurityPillarScore(
                pillar_name="Access Control, RBAC & Audit Immutability",
                weight_pct=20.0,
                achieved_score_pct=p2_achieved,
                weighted_score_pct=p2_weighted,
                status="PASSED" if p2_achieved >= 95.0 else "WARNING",
            )
        )

        # Pillar 3: Telemetry Encryption & Lifecycle Retention (15%)
        p3_achieved = 100.0 if (
            encrypt_report.all_telemetry_encrypted
            and retention_report.lifecycle_management_active
        ) else 88.0
        p3_weighted = round((p3_achieved * 15.0) / 100.0, 2)
        pillar_scores.append(
            SecurityPillarScore(
                pillar_name="Encryption In-Transit/At-Rest & Lifecycle Retention",
                weight_pct=15.0,
                achieved_score_pct=p3_achieved,
                weighted_score_pct=p3_weighted,
                status="PASSED" if p3_achieved >= 95.0 else "WARNING",
            )
        )

        # Pillar 4: AI Telemetry Privacy & Prompt Protection (15%)
        p4_achieved = 100.0 if (
            ai_report.prompts_and_responses_protected
            and ai_report.metadata_only_logging_enforced
        ) else 80.0
        p4_weighted = round((p4_achieved * 15.0) / 100.0, 2)
        pillar_scores.append(
            SecurityPillarScore(
                pillar_name="AI Telemetry Privacy & Prompt Protection",
                weight_pct=15.0,
                achieved_score_pct=p4_achieved,
                weighted_score_pct=p4_weighted,
                status="PASSED" if p4_achieved >= 95.0 else "WARNING",
            )
        )

        # Pillar 5: Compliance Readiness & Standards Mapping (15%)
        p5_achieved = 100.0 if (
            compliance_report.overall_compliance_pct >= 95.0
            and continuous_report.ci_cd_gate_enforced
        ) else 85.0
        p5_weighted = round((p5_achieved * 15.0) / 100.0, 2)
        pillar_scores.append(
            SecurityPillarScore(
                pillar_name="Compliance Readiness & Continuous CI/CD Gates",
                weight_pct=15.0,
                achieved_score_pct=p5_achieved,
                weighted_score_pct=p5_weighted,
                status="PASSED" if p5_achieved >= 95.0 else "WARNING",
            )
        )

        # Pillar 6: Incident Response & Attack Simulation (10%)
        p6_achieved = 100.0 if (
            incident_report.sla_compliant
            and attack_report.all_attacks_mitigated
        ) else 80.0
        p6_weighted = round((p6_achieved * 10.0) / 100.0, 2)
        pillar_scores.append(
            SecurityPillarScore(
                pillar_name="Incident Response & Attack Simulation Defense",
                weight_pct=10.0,
                achieved_score_pct=p6_achieved,
                weighted_score_pct=p6_weighted,
                status="PASSED" if p6_achieved >= 95.0 else "WARNING",
            )
        )

        overall_score = round(sum(p.weighted_score_pct for p in pillar_scores), 2)
        min_threshold = 95.0
        certification_granted = overall_score >= min_threshold

        if overall_score >= 95.0:
            tier = SecurityCertificationTier.ENTERPRISE_OBSERVABILITY_SECURE
        elif overall_score >= 90.0:
            tier = SecurityCertificationTier.PRODUCTION_SECURE
        elif overall_score >= 80.0:
            tier = SecurityCertificationTier.IMPROVEMENT_REQUIRED
        else:
            tier = SecurityCertificationTier.FAILED

        return ObservabilitySecurityCertificationReport(
            report_title="Phase 3I.7 Enterprise Observability Security, Privacy & Compliance Certification",
            certification_tier=tier,
            overall_score_pct=overall_score,
            minimum_passing_threshold_pct=min_threshold,
            pillar_scores=pillar_scores,
            certification_granted=certification_granted,
            auditor="DocuTask Enterprise Observability Security & Privacy Governance Engine",
        )
