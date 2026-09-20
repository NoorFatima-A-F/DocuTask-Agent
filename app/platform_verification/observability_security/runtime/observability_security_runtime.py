"""
Phase 3I.7: Observability Security, Privacy & Compliance Verification Runtime
Orchestrates all 12 security verifiers, the 6-pillar scoring engine, and the SHA-256 evidence exporter.
"""
import logging
from typing import Dict, Any

from ..verifiers.threat_model_verifier import ThreatModelVerifier
from ..verifiers.sensitive_data_verifier import SensitiveDataVerifier
from ..verifiers.log_redaction_verifier import LogRedactionVerifier
from ..verifiers.ai_privacy_verifier import AIPrivacyVerifier
from ..verifiers.access_control_verifier import AccessControlVerifier
from ..verifiers.telemetry_encryption_verifier import TelemetryEncryptionVerifier
from ..verifiers.data_retention_verifier import DataRetentionVerifier
from ..verifiers.audit_trail_verifier import AuditTrailVerifier
from ..verifiers.compliance_mapping_verifier import ComplianceMappingVerifier
from ..verifiers.attack_simulation_verifier import AttackSimulationVerifier
from ..verifiers.incident_response_verifier import IncidentResponseVerifier
from ..verifiers.continuous_security_verifier import ContinuousSecurityVerifier
from ..scoring.observability_security_scorer import ObservabilitySecurityScorer
from ..exporter.observability_security_evidence_exporter import ObservabilitySecurityEvidenceExporter

logger = logging.getLogger(__name__)


class ObservabilitySecurityRuntime:
    def __init__(
        self,
        output_dir: str = "observability_security_verification",
    ):
        self.output_dir = output_dir
        self.threat_verifier = ThreatModelVerifier()
        self.data_verifier = SensitiveDataVerifier()
        self.redact_verifier = LogRedactionVerifier()
        self.ai_verifier = AIPrivacyVerifier()
        self.access_verifier = AccessControlVerifier()
        self.encrypt_verifier = TelemetryEncryptionVerifier()
        self.retention_verifier = DataRetentionVerifier()
        self.audit_verifier = AuditTrailVerifier()
        self.compliance_verifier = ComplianceMappingVerifier()
        self.attack_verifier = AttackSimulationVerifier()
        self.incident_verifier = IncidentResponseVerifier()
        self.continuous_verifier = ContinuousSecurityVerifier()
        self.scorer = ObservabilitySecurityScorer()
        self.exporter = ObservabilitySecurityEvidenceExporter()

    def run_full_verification(self) -> Dict[str, Any]:
        logger.info("Starting Phase 3I.7 Observability Security & Privacy Verification Suite...")

        # 1. Execute all 12 verification stages
        threat_report = self.threat_verifier.verify_threat_model()
        data_report = self.data_verifier.verify_sensitive_data_protection()
        redact_report = self.redact_verifier.verify_log_redaction()
        ai_report = self.ai_verifier.verify_ai_telemetry_privacy()
        access_report = self.access_verifier.verify_access_control()
        encrypt_report = self.encrypt_verifier.verify_telemetry_encryption()
        retention_report = self.retention_verifier.verify_data_retention()
        audit_report = self.audit_verifier.verify_audit_trail()
        compliance_report = self.compliance_verifier.verify_compliance_mapping()
        attack_report = self.attack_verifier.verify_attack_simulations()
        incident_report = self.incident_verifier.verify_incident_response()
        continuous_report = self.continuous_verifier.verify_continuous_security()

        # 2. Compute 6-pillar score and certification
        cert_report = self.scorer.calculate_certification_score(
            threat_report=threat_report,
            data_report=data_report,
            redact_report=redact_report,
            ai_report=ai_report,
            access_report=access_report,
            encrypt_report=encrypt_report,
            retention_report=retention_report,
            audit_report=audit_report,
            compliance_report=compliance_report,
            attack_report=attack_report,
            incident_report=incident_report,
            continuous_report=continuous_report,
        )

        # 3. Export all JSON artifacts with SHA-256 signatures to output directory
        metadata = self.exporter.export_all_reports(
            output_dir=self.output_dir,
            threat_report=threat_report,
            data_report=data_report,
            redact_report=redact_report,
            ai_report=ai_report,
            access_report=access_report,
            encrypt_report=encrypt_report,
            retention_report=retention_report,
            audit_report=audit_report,
            compliance_report=compliance_report,
            attack_report=attack_report,
            incident_report=incident_report,
            continuous_report=continuous_report,
            certification_report=cert_report,
        )

        return {
            "status": "SUCCESS" if cert_report.certification_granted else "FAILED",
            "certification_tier": cert_report.certification_tier.value,
            "overall_score_pct": cert_report.overall_score_pct,
            "certification_granted": cert_report.certification_granted,
            "threat_report": threat_report.model_dump(mode="json"),
            "data_report": data_report.model_dump(mode="json"),
            "redaction_report": redact_report.model_dump(mode="json"),
            "ai_report": ai_report.model_dump(mode="json"),
            "access_report": access_report.model_dump(mode="json"),
            "encryption_report": encrypt_report.model_dump(mode="json"),
            "retention_report": retention_report.model_dump(mode="json"),
            "audit_report": audit_report.model_dump(mode="json"),
            "compliance_report": compliance_report.model_dump(mode="json"),
            "attack_report": attack_report.model_dump(mode="json"),
            "incident_report": incident_report.model_dump(mode="json"),
            "continuous_report": continuous_report.model_dump(mode="json"),
            "certification_report": cert_report.model_dump(mode="json"),
            "metadata": metadata,
        }
