"""
Abstract Interfaces for Enterprise Backup Security Verification Framework (Part 3G.2F).
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

from app.platform_verification.backup_security_verification.domain.models import (
    BackupSecurityInventoryReport,
    DataClassificationReport,
    BackupEncryptionReport,
    KeyManagementReport,
    KeyRotationReport,
    AccessControlReport,
    IAMTestReport,
    TamperDetectionReport,
    PoisoningProtectionReport,
    ImmutabilityReport,
    AuditReport,
    RetentionSecurityReport,
    BackupSecurityComplianceReport,
    BackupSecurityQualityScorecard,
)


class IBackupSecurityInventoryEngine(ABC):
    @abstractmethod
    def discover_backup_security_inventory(self) -> BackupSecurityInventoryReport:
        pass


class IDataClassificationEngine(ABC):
    @abstractmethod
    def verify_data_classification_controls(
        self, inventory: BackupSecurityInventoryReport
    ) -> DataClassificationReport:
        pass


class IBackupEncryptionEngine(ABC):
    @abstractmethod
    def verify_backup_encryption(self) -> BackupEncryptionReport:
        pass


class IKeyManagementEngine(ABC):
    @abstractmethod
    def verify_key_management_architecture(self) -> KeyManagementReport:
        pass


class IKeyRotationEngine(ABC):
    @abstractmethod
    def verify_key_rotation_and_historic_decryptability(
        self,
    ) -> KeyRotationReport:
        pass


class IAccessControlEngine(ABC):
    @abstractmethod
    def verify_backup_access_controls(self) -> AccessControlReport:
        pass


class IIAMPolicyTester(ABC):
    @abstractmethod
    def execute_iam_penetration_tests(self) -> IAMTestReport:
        pass


class ITamperDetectorEngine(ABC):
    @abstractmethod
    def test_backup_tamper_detection(self) -> TamperDetectionReport:
        pass


class IPoisoningProtectionEngine(ABC):
    @abstractmethod
    def verify_backup_poisoning_protection(self) -> PoisoningProtectionReport:
        pass


class IImmutabilityEngine(ABC):
    @abstractmethod
    def verify_storage_immutability_and_worm(self) -> ImmutabilityReport:
        pass


class IAuditAnalyzerEngine(ABC):
    @abstractmethod
    def verify_backup_access_auditing(self) -> AuditReport:
        pass


class IRetentionSecurityEngine(ABC):
    @abstractmethod
    def verify_retention_and_crypto_shredding(self) -> RetentionSecurityReport:
        pass


class IBackupSecurityComplianceEngine(ABC):
    @abstractmethod
    def evaluate_backup_security_compliance(
        self,
    ) -> BackupSecurityComplianceReport:
        pass


class IBackupSecurityQualityScoringEngine(ABC):
    @abstractmethod
    def compute_quality_scorecard(
        self,
        encryption_score: float,
        access_control_score: float,
        integrity_protection_score: float,
        key_management_score: float,
        auditability_score: float,
        compliance_score: float,
        execution_duration_ms: float,
    ) -> BackupSecurityQualityScorecard:
        pass


class IBackupSecurityEvidenceEngine(ABC):
    @abstractmethod
    def export_all_evidence_artifacts(
        self,
        verification_data: Dict[str, Any],
        output_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        pass
