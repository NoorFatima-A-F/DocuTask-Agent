"""
Comprehensive Unit and Integration Test Suite for Enterprise Backup Security Verification Framework.
Part 3G.2F — Backup Security, Encryption, Integrity, Access Control & Compliance.
"""
import pytest
import os
import json
import tempfile
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.backup_security_verification.domain.models import (
    DataClassificationLevel,
    BackupEncryptionAlgorithm,
    KeyProviderType,
    SecurityCertificationTier,
    BackupSecurityAssetItem,
)
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
from app.platform_verification.backup_security_verification.audit_policy.secret_backup_security_engine import (
    SecretBackupSecurityEngine,
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
from app.platform_verification.backup_security_verification.runtime.backup_security_runtime import (
    BackupSecurityVerificationRuntime,
)
from app.platform_verification.backup_security_verification.api.backup_security_api import (
    router,
)


@pytest.fixture
def app_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_inventory_discovery():
    """Verify discovery of 245 backup assets across 8 asset types."""
    engine = BackupSecurityInventoryEngine()
    report = engine.discover_backup_security_inventory()
    assert report.backup_assets == 245
    assert report.encrypted_assets == 245
    assert report.unencrypted_assets == 0
    assert len(report.assets_by_type) == 8
    assert report.passed is True
    assert len(report.sample_assets) >= 5


def test_data_classification():
    """Verify classification of assets across categories and policy enforcement."""
    inv_engine = BackupSecurityInventoryEngine()
    inv_report = inv_engine.discover_backup_security_inventory()
    class_engine = DataClassificationEngine()
    report = class_engine.verify_data_classification_controls(inv_report)

    assert report.total_categories_audited >= 4
    assert report.classification_rules_satisfied is True
    assert report.passed is True
    for cat in report.categories:
        assert cat.encryption_enforced is True
        if cat.classification_level != DataClassificationLevel.PUBLIC:
            assert cat.restricted_access_enforced is True
        assert cat.audit_logging_enforced is True


def test_backup_encryption_standards():
    """Verify AES-256-GCM encryption at rest and in-transit, rejection of weak ciphers."""
    enc_engine = BackupEncryptionEngine()
    report = enc_engine.verify_backup_encryption()

    assert report.algorithm == "AES-256-GCM"
    assert report.encrypted is True
    assert report.encryption_at_rest_verified is True
    assert report.encryption_in_transit_verified is True
    assert report.insecure_formats_rejected is True
    assert report.passed is True
    assert "FIPS-140-2" in report.key_provider or "AWS KMS" in report.key_provider or "KMS" in report.key_provider


def test_key_management_and_isolation():
    """Verify KMS/HSM isolation, Envelope Encryption, and zero collocated keys."""
    km_engine = KeyManagementEngine()
    report = km_engine.verify_key_management_architecture()

    assert report.master_keys_isolated is True
    assert report.data_encryption_keys_wrapped is True
    assert report.backup_keys_stored_in_kms is True
    assert len(report.allowed_providers) >= 4
    assert report.prohibited_practices_rejected is True
    assert report.passed is True


def test_key_rotation_and_historic_decryptability():
    """Verify 90-day rotation policy and backward decryptability of historic backups."""
    rot_engine = KeyRotationEngine()
    report = rot_engine.verify_key_rotation_and_historic_decryptability()

    assert report.automatic_rotation_enabled is True
    assert report.rotation_interval_days == 90
    assert report.previous_keys_retained is True
    assert report.historic_backups_decryptable is True
    assert report.rotation_simulation_passed is True
    assert report.passed is True


def test_access_control_and_least_privilege():
    """Verify RBAC policies, separation of duties, and MFA enforcement."""
    ac_engine = AccessControlEngine()
    report = ac_engine.verify_backup_access_controls()

    assert report.least_privilege_enforced is True
    assert report.write_only_backup_service_verified is True
    assert report.read_only_recovery_service_verified is True
    assert report.auditor_read_only_verified is True
    assert report.unauthorized_identities_blocked_count >= 4
    assert report.passed is True


def test_iam_policy_penetration_testing():
    """Verify IAM policy test scenarios: unauthorized denial, privesc denial, recovery allowance."""
    tester = IAMPolicyTester()
    report = tester.execute_iam_penetration_tests()

    assert report.unauthorized_user_access_denied is True
    assert report.developer_privilege_escalation_denied is True
    assert report.recovery_identity_access_allowed is True
    assert report.tests_executed_count >= 4
    assert report.tests_passed_count == report.tests_executed_count
    assert report.passed is True


def test_cryptographic_tamper_detection():
    """Verify 1-byte bit-flip tamper detection via SHA-512 and digital signatures."""
    tamper_engine = TamperDetectorEngine()
    report = tamper_engine.test_backup_tamper_detection()

    assert report.one_byte_modification_detected is True
    assert report.sha512_hash_comparison_verified is True
    assert report.digital_signature_verification_passed is True
    assert report.tampered_backups_quarantined is True
    assert report.passed is True


def test_poisoning_protection_and_pre_restore_validation():
    """Verify malware analysis, schema validation, and pre-restore sandbox isolation."""
    poison_engine = PoisoningProtectionEngine()
    report = poison_engine.verify_backup_poisoning_protection()

    assert report.malware_scan_pre_restore_passed is True
    assert report.schema_injection_validation_passed is True
    assert report.signature_authenticity_verified is True
    assert report.untrusted_sources_rejected is True
    assert report.suspicious_payloads_blocked_count >= 4
    assert report.passed is True


def test_immutability_and_worm_retention():
    """Verify S3 Object Lock Compliance mode, legal hold, and deletion prevention."""
    imm_engine = ImmutabilityEngine()
    report = imm_engine.verify_storage_immutability_and_worm()

    assert report.object_lock_compliance_mode_active is True
    assert report.worm_storage_enforced is True
    assert report.deletion_attempts_denied is True
    assert report.modification_attempts_denied is True
    assert report.overwrite_attempts_denied is True
    assert report.retention_period_enforced_days >= 2555  # 7 years
    assert report.passed is True


def test_audit_analyzer_and_merkle_chains():
    """Verify 6 operation audit logging, SHA-256 Merkle chain immutability."""
    audit_engine = AuditAnalyzerEngine()
    report = audit_engine.verify_backup_access_auditing()

    assert report.all_operations_logged is True
    assert len(report.operations_tracked) >= 6
    assert report.log_tamper_proofing_active is True
    assert report.audit_trail_complete is True
    assert report.passed is True


def test_retention_security_and_crypto_shredding():
    """Verify crypto-shredding key destruction upon expiration, legal hold overrides."""
    ret_engine = RetentionSecurityEngine()
    report = ret_engine.verify_retention_and_crypto_shredding()

    assert report.retention_period_verified is True
    assert report.deletion_policy_secure is True
    assert report.legal_hold_supported is True
    assert report.crypto_shredding_expired_backups is True
    assert report.protected_backups_immutable is True
    assert report.passed is True


def test_secret_backup_security():
    """Verify zero plaintext secret leaks in backups."""
    sec_engine = SecretBackupSecurityEngine()
    report = sec_engine.verify_secret_backup_security()

    assert report["total_secrets_scanned"] >= 5
    assert report["zero_plaintext_leakage_verified"] is True
    assert report["passed"] is True


def test_regulatory_compliance_engine():
    """Verify compliance across NIST, OWASP, CIS, ISO 27001, SOC 2, and GDPR."""
    comp_engine = BackupSecurityComplianceEngine()
    report = comp_engine.evaluate_backup_security_compliance()

    assert report.nist_sp_800_53_aligned is True
    assert report.nist_sp_800_57_aligned is True
    assert report.owasp_asvs_aligned is True
    assert report.owasp_secrets_management_aligned is True
    assert report.cis_benchmarks_aligned is True
    assert report.iso_27001_aligned is True
    assert report.soc_2_aligned is True
    assert report.gdpr_security_principles_aligned is True
    assert report.compliance_score_percent == 100.0
    assert report.passed is True


def test_scoring_engine_and_quality_scorecard():
    """Verify composite scoring model and tier assignment."""
    scoring_engine = BackupSecurityQualityScoringEngine()
    scorecard = scoring_engine.compute_quality_scorecard(
        encryption_score=100.0,
        access_control_score=100.0,
        integrity_protection_score=100.0,
        key_management_score=100.0,
        auditability_score=100.0,
        compliance_score=100.0,
        execution_duration_ms=45.2,
    )

    assert scorecard.composite_score >= 95.0
    assert scorecard.certification_tier == SecurityCertificationTier.ENTERPRISE_BACKUP_SECURITY_CERTIFIED
    assert scorecard.passed is True


def test_evidence_generation():
    """Verify serialization of all 14 evidence files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        runtime = BackupSecurityVerificationRuntime()
        results = runtime.execute_full_security_verification(output_dir=tmpdir)

        assert len(results["exported_manifest_paths"]) == 14
        for name, filepath in results["exported_manifest_paths"].items():
            assert os.path.exists(filepath), f"Missing evidence file: {filepath}"
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert isinstance(data, dict)
                assert len(data) > 0


def test_api_endpoints(app_client):
    """Verify FastAPI router endpoints."""
    # Scorecard endpoint
    resp = app_client.get("/api/v1/platform-verification/backup-security/scorecard")
    assert resp.status_code == 200
    data = resp.json()
    assert data["composite_score"] >= 95.0
    assert data["certification_tier"] == "Enterprise Backup Security Certified"

    # Inventory endpoint
    resp = app_client.get("/api/v1/platform-verification/backup-security/inventory")
    assert resp.status_code == 200
    data = resp.json()
    assert data["inventory"]["backup_assets"] == 245

    # Encryption status endpoint
    resp = app_client.get("/api/v1/platform-verification/backup-security/encryption-status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["encrypted"] is True
    assert data["algorithm"] == "AES-256-GCM"

    # Tamper resistance endpoint
    resp = app_client.get("/api/v1/platform-verification/backup-security/tamper-resistance")
    assert resp.status_code == 200
    data = resp.json()
    assert data["tamper_detection"]["one_byte_modification_detected"] is True

    # Immutability endpoint
    resp = app_client.get("/api/v1/platform-verification/backup-security/immutability-status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["worm_storage_enforced"] is True

    # Compliance endpoint
    resp = app_client.get("/api/v1/platform-verification/backup-security/compliance")
    assert resp.status_code == 200
    data = resp.json()
    assert data["compliance_score_percent"] == 100.0
