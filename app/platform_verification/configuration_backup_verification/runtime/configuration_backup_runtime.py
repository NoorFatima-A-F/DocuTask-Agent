"""
Verification Runtime Orchestrator for Enterprise Configuration & Secret Backup Verification (Part 3G.2D).
"""
import time
from typing import Dict, Any, Optional

from app.platform_verification.configuration_backup_verification.discovery.configuration_inventory_engine import (
    ConfigurationInventoryEngine,
)
from app.platform_verification.configuration_backup_verification.discovery.configuration_catalog_engine import (
    ConfigurationCatalogEngine,
)
from app.platform_verification.configuration_backup_verification.discovery.configuration_validation_engine import (
    ConfigurationValidationEngine,
)
from app.platform_verification.configuration_backup_verification.secrets.secret_discovery_engine import (
    SecretDiscoveryEngine,
)
from app.platform_verification.configuration_backup_verification.secrets.secret_backup_engine import (
    SecretBackupEngine,
)
from app.platform_verification.configuration_backup_verification.cryptography.encryption_key_recovery_engine import (
    EncryptionKeyRecoveryEngine,
)
from app.platform_verification.configuration_backup_verification.cryptography.certificate_recovery_engine import (
    CertificateRecoveryEngine,
)
from app.platform_verification.configuration_backup_verification.continuity.feature_flag_recovery_engine import (
    FeatureFlagRecoveryEngine,
)
from app.platform_verification.configuration_backup_verification.continuity.iac_recovery_engine import (
    IaCRecoveryEngine,
)
from app.platform_verification.configuration_backup_verification.continuity.version_compatibility_engine import (
    VersionCompatibilityEngine,
)
from app.platform_verification.configuration_backup_verification.continuity.configuration_drift_engine import (
    ConfigurationDriftEngine,
)
from app.platform_verification.configuration_backup_verification.simulation.configuration_restore_simulation_engine import (
    ConfigurationRestoreSimulationEngine,
)
from app.platform_verification.configuration_backup_verification.simulation.configuration_security_engine import (
    ConfigurationSecurityEngine,
)
from app.platform_verification.configuration_backup_verification.simulation.configuration_compliance_engine import (
    ConfigurationComplianceEngine,
)
from app.platform_verification.configuration_backup_verification.scoring.configuration_quality_scoring_engine import (
    ConfigurationQualityScoringEngine,
)
from app.platform_verification.configuration_backup_verification.evidence.configuration_evidence_manifest_engine import (
    ConfigurationEvidenceManifestEngine,
)


class ConfigurationBackupVerificationRuntime:
    """
    Master orchestrator for Part 3G.2D Configuration, Secret & Cryptographic Backup Verification.
    Runs all discovery, secret, cryptographic, operational continuity, simulation, and compliance audits.
    """

    def __init__(
        self,
        inventory_engine: Optional[ConfigurationInventoryEngine] = None,
        catalog_engine: Optional[ConfigurationCatalogEngine] = None,
        validation_engine: Optional[ConfigurationValidationEngine] = None,
        secret_discovery_engine: Optional[SecretDiscoveryEngine] = None,
        secret_backup_engine: Optional[SecretBackupEngine] = None,
        key_recovery_engine: Optional[EncryptionKeyRecoveryEngine] = None,
        cert_recovery_engine: Optional[CertificateRecoveryEngine] = None,
        feature_flag_engine: Optional[FeatureFlagRecoveryEngine] = None,
        iac_engine: Optional[IaCRecoveryEngine] = None,
        version_engine: Optional[VersionCompatibilityEngine] = None,
        drift_engine: Optional[ConfigurationDriftEngine] = None,
        restore_simulation_engine: Optional[ConfigurationRestoreSimulationEngine] = None,
        security_engine: Optional[ConfigurationSecurityEngine] = None,
        compliance_engine: Optional[ConfigurationComplianceEngine] = None,
        scoring_engine: Optional[ConfigurationQualityScoringEngine] = None,
        evidence_engine: Optional[ConfigurationEvidenceManifestEngine] = None,
    ):
        self.inventory_engine = inventory_engine or ConfigurationInventoryEngine()
        self.catalog_engine = catalog_engine or ConfigurationCatalogEngine()
        self.validation_engine = validation_engine or ConfigurationValidationEngine()
        self.secret_discovery_engine = secret_discovery_engine or SecretDiscoveryEngine()
        self.secret_backup_engine = secret_backup_engine or SecretBackupEngine()
        self.key_recovery_engine = key_recovery_engine or EncryptionKeyRecoveryEngine()
        self.cert_recovery_engine = cert_recovery_engine or CertificateRecoveryEngine()
        self.feature_flag_engine = feature_flag_engine or FeatureFlagRecoveryEngine()
        self.iac_engine = iac_engine or IaCRecoveryEngine()
        self.version_engine = version_engine or VersionCompatibilityEngine()
        self.drift_engine = drift_engine or ConfigurationDriftEngine()
        self.restore_simulation_engine = restore_simulation_engine or ConfigurationRestoreSimulationEngine()
        self.security_engine = security_engine or ConfigurationSecurityEngine()
        self.compliance_engine = compliance_engine or ConfigurationComplianceEngine()
        self.scoring_engine = scoring_engine or ConfigurationQualityScoringEngine()
        self.evidence_engine = evidence_engine or ConfigurationEvidenceManifestEngine()

    def execute_full_verification(
        self, output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end configuration and secret verification across all 14 sub-phases.
        """
        start_time = time.perf_counter()

        # 1. Discovery & Catalog
        inv_report = self.inventory_engine.discover_configuration_inventory()
        cat_report = self.catalog_engine.build_configuration_catalog(inv_report)
        val_report = self.validation_engine.validate_required_configurations(cat_report)

        # 2. Secret Discovery & Backup
        secret_inv_report = self.secret_discovery_engine.discover_and_classify_secrets()
        secret_bk_report = self.secret_backup_engine.verify_secret_backup_strategies(secret_inv_report)

        # 3. Cryptography & Certificates
        key_report = self.key_recovery_engine.verify_encryption_key_recovery()
        cert_report = self.cert_recovery_engine.verify_certificate_recovery_and_handshakes()

        # 4. Operational Continuity & Drift
        ff_report = self.feature_flag_engine.verify_feature_flag_recovery()
        iac_report = self.iac_engine.verify_iac_infrastructure_recovery()
        ver_report = self.version_engine.verify_version_compatibility()
        drift_report = self.drift_engine.audit_configuration_drift()

        # 5. Simulation, Security & Compliance
        restore_report = self.restore_simulation_engine.execute_configuration_restore_simulation()
        sec_report = self.security_engine.verify_configuration_security_controls()
        comp_report = self.compliance_engine.evaluate_compliance_standards()

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        # 6. Scoring Calculations
        cfg_cov_score = val_report.validation_score_percent
        sec_cov_score = secret_bk_report.backup_coverage_percent
        crypto_score = 100.0 if key_report.all_cryptographic_outputs_identical else 60.0
        cert_score = cert_report.handshake_success_rate_percent
        iac_ff_score = 100.0 if (iac_report.passed and ff_report.passed) else 70.0
        restore_score = 100.0 if restore_report.passed else 50.0
        drift_ver_score = 100.0 if (drift_report.passed and ver_report.passed) else 65.0
        sec_comp_score = 100.0 if (sec_report.passed and comp_report.passed) else 60.0

        scorecard = self.scoring_engine.compute_quality_scorecard(
            configuration_coverage_score=cfg_cov_score,
            secret_coverage_encryption_score=sec_cov_score,
            cryptographic_continuity_score=crypto_score,
            certificate_health_score=cert_score,
            iac_and_feature_flags_score=iac_ff_score,
            restore_simulation_score=restore_score,
            drift_and_version_score=drift_ver_score,
            security_and_compliance_score=sec_comp_score,
            execution_duration_ms=elapsed_ms,
        )

        verification_data = {
            "configuration_inventory": inv_report,
            "configuration_catalog": cat_report,
            "configuration_validation": val_report,
            "secret_inventory": secret_inv_report,
            "secret_backup": secret_bk_report,
            "encryption_key_recovery": key_report,
            "certificate_recovery": cert_report,
            "feature_flag_restore": ff_report,
            "infrastructure_configuration": iac_report,
            "version_compatibility": ver_report,
            "configuration_drift": drift_report,
            "restore_simulation": restore_report,
            "security_report": sec_report,
            "compliance_report": comp_report,
            "scorecard": scorecard,
        }

        # 7. Evidence Export
        manifest_paths = self.evidence_engine.export_all_evidence_artifacts(
            verification_data, output_dir=output_dir
        )

        verification_data["exported_manifest_paths"] = manifest_paths
        verification_data["passed"] = scorecard.passed

        return verification_data
