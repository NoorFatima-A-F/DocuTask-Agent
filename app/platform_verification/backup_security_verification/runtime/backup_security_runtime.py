"""
Master Runtime Orchestrator for Backup Security Verification Framework (Part 3G.2F).
"""
import time
from typing import Dict, Any, Optional

from app.platform_verification.backup_security_verification.inventory.backup_security_inventory_engine import (
    BackupSecurityInventoryEngine,
)
from app.platform_verification.backup_security_verification.inventory.data_classification_engine import (
    DataClassificationEngine,
)
from app.platform_verification.backup_security_verification.encryption_validator.backup_encryption_engine import (
    BackupEncryptionEngine,
)
from app.platform_verification.backup_security_verification.encryption_validator.key_management_engine import (
    KeyManagementEngine,
)
from app.platform_verification.backup_security_verification.encryption_validator.key_rotation_engine import (
    KeyRotationEngine,
)
from app.platform_verification.backup_security_verification.access_control_validator.access_control_engine import (
    AccessControlEngine,
)
from app.platform_verification.backup_security_verification.access_control_validator.iam_policy_tester import (
    IAMPolicyTester,
)
from app.platform_verification.backup_security_verification.integrity_tamper.tamper_detector_engine import (
    TamperDetectorEngine,
)
from app.platform_verification.backup_security_verification.integrity_tamper.poisoning_protection_engine import (
    PoisoningProtectionEngine,
)
from app.platform_verification.backup_security_verification.integrity_tamper.immutability_engine import (
    ImmutabilityEngine,
)
from app.platform_verification.backup_security_verification.audit_policy.audit_analyzer_engine import (
    AuditAnalyzerEngine,
)
from app.platform_verification.backup_security_verification.audit_policy.retention_security_engine import (
    RetentionSecurityEngine,
)
from app.platform_verification.backup_security_verification.compliance_engine.backup_security_compliance_engine import (
    BackupSecurityComplianceEngine,
)
from app.platform_verification.backup_security_verification.scoring.backup_security_scoring_engine import (
    BackupSecurityQualityScoringEngine,
)
from app.platform_verification.backup_security_verification.evidence_generator.backup_security_evidence_engine import (
    BackupSecurityEvidenceEngine,
)


class BackupSecurityVerificationRuntime:
    """
    Master orchestrator for the Part 3G.2F Backup Security Verification Framework.
    Runs comprehensive encryption validation, IAM penetration testing, bit-flip tamper detection,
    poisoning defense evaluation, WORM immutability locks, forensic audit analysis, and regulatory compliance.
    """

    def __init__(
        self,
        inventory_engine: Optional[BackupSecurityInventoryEngine] = None,
        classification_engine: Optional[DataClassificationEngine] = None,
        encryption_engine: Optional[BackupEncryptionEngine] = None,
        key_management_engine: Optional[KeyManagementEngine] = None,
        key_rotation_engine: Optional[KeyRotationEngine] = None,
        access_control_engine: Optional[AccessControlEngine] = None,
        iam_policy_tester: Optional[IAMPolicyTester] = None,
        tamper_detector: Optional[TamperDetectorEngine] = None,
        poisoning_protection: Optional[PoisoningProtectionEngine] = None,
        immutability_engine: Optional[ImmutabilityEngine] = None,
        audit_analyzer: Optional[AuditAnalyzerEngine] = None,
        retention_engine: Optional[RetentionSecurityEngine] = None,
        compliance_engine: Optional[BackupSecurityComplianceEngine] = None,
        scoring_engine: Optional[BackupSecurityQualityScoringEngine] = None,
        evidence_engine: Optional[BackupSecurityEvidenceEngine] = None,
    ):
        self.inventory_engine = inventory_engine or BackupSecurityInventoryEngine()
        self.classification_engine = classification_engine or DataClassificationEngine()
        self.encryption_engine = encryption_engine or BackupEncryptionEngine()
        self.key_management_engine = key_management_engine or KeyManagementEngine()
        self.key_rotation_engine = key_rotation_engine or KeyRotationEngine()
        self.access_control_engine = access_control_engine or AccessControlEngine()
        self.iam_policy_tester = iam_policy_tester or IAMPolicyTester()
        self.tamper_detector = tamper_detector or TamperDetectorEngine()
        self.poisoning_protection = poisoning_protection or PoisoningProtectionEngine()
        self.immutability_engine = immutability_engine or ImmutabilityEngine()
        self.audit_analyzer = audit_analyzer or AuditAnalyzerEngine()
        self.retention_engine = retention_engine or RetentionSecurityEngine()
        self.compliance_engine = compliance_engine or BackupSecurityComplianceEngine()
        self.scoring_engine = scoring_engine or BackupSecurityQualityScoringEngine()
        self.evidence_engine = evidence_engine or BackupSecurityEvidenceEngine()

    def execute_full_security_verification(
        self, output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end backup security verification across all 14 phases.
        """
        start_time = time.perf_counter()

        # Step 1: Inventory & Classification
        inventory_report = self.inventory_engine.discover_backup_security_inventory()
        classification_report = self.classification_engine.verify_data_classification_controls(inventory_report)

        # Step 2: Encryption & Key Management
        encryption_report = self.encryption_engine.verify_backup_encryption()
        key_management_report = self.key_management_engine.verify_key_management_architecture()
        key_rotation_report = self.key_rotation_engine.verify_key_rotation_and_historic_decryptability()

        # Step 3: Access Control & IAM Testing
        access_control_report = self.access_control_engine.verify_backup_access_controls()
        iam_test_report = self.iam_policy_tester.execute_iam_penetration_tests()

        # Step 4: Integrity, Tamper Detection, Poisoning Defense & Immutability
        tamper_report = self.tamper_detector.test_backup_tamper_detection()
        poisoning_report = self.poisoning_protection.verify_backup_poisoning_protection()
        immutability_report = self.immutability_engine.verify_storage_immutability_and_worm()

        # Step 5: Audit & Retention Security
        audit_report = self.audit_analyzer.verify_backup_access_auditing()
        retention_report = self.retention_engine.verify_retention_and_crypto_shredding()

        # Step 6: Regulatory Compliance
        compliance_report = self.compliance_engine.evaluate_backup_security_compliance()

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        # Step 7: Scoring & Certification
        enc_score = 100.0 if encryption_report.passed and inventory_report.unencrypted_assets == 0 else 60.0
        acc_score = 100.0 if access_control_report.passed and iam_test_report.passed else 50.0
        integ_score = 100.0 if (tamper_report.passed and poisoning_report.passed and immutability_report.passed) else 65.0
        key_score = 100.0 if key_management_report.passed and key_rotation_report.passed else 55.0
        aud_score = 100.0 if audit_report.passed and retention_report.passed else 70.0
        comp_score = compliance_report.compliance_score_percent

        scorecard = self.scoring_engine.compute_quality_scorecard(
            encryption_score=enc_score,
            access_control_score=acc_score,
            integrity_protection_score=integ_score,
            key_management_score=key_score,
            auditability_score=aud_score,
            compliance_score=comp_score,
            execution_duration_ms=elapsed_ms,
        )

        verification_data = {
            "backup_security_inventory": inventory_report,
            "data_classification_report": classification_report,
            "encryption_report": encryption_report,
            "key_management_report": key_management_report,
            "key_rotation_report": key_rotation_report,
            "access_control_report": access_control_report,
            "iam_test_report": iam_test_report,
            "tamper_detection_report": tamper_report,
            "poisoning_protection_report": poisoning_report,
            "immutability_report": immutability_report,
            "audit_report": audit_report,
            "retention_security_report": retention_report,
            "compliance_report": compliance_report,
            "scorecard": scorecard,
        }

        # Step 8: Evidence Serialization
        manifest_paths = self.evidence_engine.export_all_evidence_artifacts(
            verification_data, output_dir=output_dir
        )

        verification_data["exported_manifest_paths"] = manifest_paths
        verification_data["passed"] = scorecard.passed

        return verification_data
