"""
Phase 3I.7: Observability Security, Privacy & Compliance Verification Framework — Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import (
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
    ObservabilitySecurityCertificationReport,
)


class IThreatModelVerifier(ABC):
    @abstractmethod
    def verify_threat_model(self) -> ObservabilityThreatModelReport:
        pass


class ISensitiveDataVerifier(ABC):
    @abstractmethod
    def verify_sensitive_data_protection(self) -> SensitiveDataReport:
        pass


class ILogRedactionVerifier(ABC):
    @abstractmethod
    def verify_log_redaction(self) -> LogRedactionReport:
        pass


class IAIPrivacyVerifier(ABC):
    @abstractmethod
    def verify_ai_telemetry_privacy(self) -> AITelemetryPrivacyReport:
        pass


class IAccessControlVerifier(ABC):
    @abstractmethod
    def verify_access_control(self) -> AccessControlReport:
        pass


class ITelemetryEncryptionVerifier(ABC):
    @abstractmethod
    def verify_telemetry_encryption(self) -> TelemetryEncryptionReport:
        pass


class IDataRetentionVerifier(ABC):
    @abstractmethod
    def verify_data_retention(self) -> TelemetryRetentionReport:
        pass


class IAuditTrailVerifier(ABC):
    @abstractmethod
    def verify_audit_trail(self) -> ObservabilityAuditReport:
        pass


class IComplianceMappingVerifier(ABC):
    @abstractmethod
    def verify_compliance_mapping(self) -> ComplianceMappingReport:
        pass


class IAttackSimulationVerifier(ABC):
    @abstractmethod
    def verify_attack_simulations(self) -> AttackSimulationReport:
        pass


class IIncidentResponseVerifier(ABC):
    @abstractmethod
    def verify_incident_response(self) -> TelemetryIncidentResponseReport:
        pass


class IContinuousSecurityVerifier(ABC):
    @abstractmethod
    def verify_continuous_security(self) -> ContinuousSecurityReport:
        pass


class IObservabilitySecurityScorer(ABC):
    @abstractmethod
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
        pass


class IObservabilitySecurityEvidenceExporter(ABC):
    @abstractmethod
    def export_all_reports(
        self,
        output_dir: str,
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
        certification_report: ObservabilitySecurityCertificationReport,
    ) -> Dict[str, Any]:
        pass
