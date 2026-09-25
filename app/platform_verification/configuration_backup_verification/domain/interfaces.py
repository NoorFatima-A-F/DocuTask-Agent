"""
Abstract Interfaces for Enterprise Configuration, Secret & Cryptographic Material Backup Verification (Part 3G.2D).
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from app.platform_verification.configuration_backup_verification.domain.models import (
    ConfigurationInventoryReport,
    ConfigurationCatalogReport,
    ConfigurationValidationReport,
    SecretInventoryReport,
    SecretBackupReport,
    EncryptionKeyRecoveryReport,
    CertificateRecoveryReport,
    FeatureFlagRestoreReport,
    InfrastructureConfigurationReport,
    VersionCompatibilityReport,
    ConfigurationDriftReport,
    ConfigurationRestoreSimulationReport,
    ConfigurationSecurityReport,
    ConfigurationComplianceReport,
    ConfigurationQualityScorecard,
)


class IConfigurationInventoryEngine(ABC):
    @abstractmethod
    def discover_configuration_inventory(self) -> ConfigurationInventoryReport:
        pass


class IConfigurationCatalogEngine(ABC):
    @abstractmethod
    def build_configuration_catalog(
        self, inventory: ConfigurationInventoryReport
    ) -> ConfigurationCatalogReport:
        pass


class IConfigurationValidationEngine(ABC):
    @abstractmethod
    def validate_required_configurations(
        self, catalog: ConfigurationCatalogReport
    ) -> ConfigurationValidationReport:
        pass


class ISecretDiscoveryEngine(ABC):
    @abstractmethod
    def discover_and_classify_secrets(self) -> SecretInventoryReport:
        pass


class ISecretBackupEngine(ABC):
    @abstractmethod
    def verify_secret_backup_strategies(
        self, secret_inventory: SecretInventoryReport
    ) -> SecretBackupReport:
        pass


class IEncryptionKeyRecoveryEngine(ABC):
    @abstractmethod
    def verify_encryption_key_recovery(self) -> EncryptionKeyRecoveryReport:
        pass


class ICertificateRecoveryEngine(ABC):
    @abstractmethod
    def verify_certificate_recovery_and_handshakes(
        self,
    ) -> CertificateRecoveryReport:
        pass


class IFeatureFlagRecoveryEngine(ABC):
    @abstractmethod
    def verify_feature_flag_recovery(self) -> FeatureFlagRestoreReport:
        pass


class IIaCRecoveryEngine(ABC):
    @abstractmethod
    def verify_iac_infrastructure_recovery(
        self,
    ) -> InfrastructureConfigurationReport:
        pass


class IVersionCompatibilityEngine(ABC):
    @abstractmethod
    def verify_version_compatibility(self) -> VersionCompatibilityReport:
        pass


class IConfigurationDriftEngine(ABC):
    @abstractmethod
    def audit_configuration_drift(self) -> ConfigurationDriftReport:
        pass


class IConfigurationRestoreSimulationEngine(ABC):
    @abstractmethod
    def execute_configuration_restore_simulation(
        self,
    ) -> ConfigurationRestoreSimulationReport:
        pass


class IConfigurationSecurityEngine(ABC):
    @abstractmethod
    def verify_configuration_security_controls(
        self,
    ) -> ConfigurationSecurityReport:
        pass


class IConfigurationComplianceEngine(ABC):
    @abstractmethod
    def evaluate_compliance_standards(
        self,
    ) -> ConfigurationComplianceReport:
        pass


class IConfigurationQualityScoringEngine(ABC):
    @abstractmethod
    def compute_quality_scorecard(
        self,
        configuration_coverage_score: float,
        secret_coverage_encryption_score: float,
        cryptographic_continuity_score: float,
        certificate_health_score: float,
        iac_and_feature_flags_score: float,
        restore_simulation_score: float,
        drift_and_version_score: float,
        security_and_compliance_score: float,
        execution_duration_ms: float,
    ) -> ConfigurationQualityScorecard:
        pass


class IConfigurationEvidenceManifestEngine(ABC):
    @abstractmethod
    def export_all_evidence_artifacts(
        self,
        verification_data: Dict[str, Any],
        output_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        pass
