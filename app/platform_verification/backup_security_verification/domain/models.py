"""
Domain Models for Enterprise Backup Security Verification Framework (Part 3G.2F).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any


class DataClassificationLevel(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    HIGHLY_SENSITIVE = "HIGHLY_SENSITIVE"


class BackupEncryptionAlgorithm(str, Enum):
    AES_256_GCM = "AES-256-GCM"
    CHACHA20_POLY1305 = "ChaCha20-Poly1305"
    AES_256_CBC_HMAC = "AES-256-CBC-HMAC-SHA256"


class KeyProviderType(str, Enum):
    AWS_KMS = "AWS KMS"
    GOOGLE_CLOUD_KMS = "Google Cloud KMS"
    AZURE_KEY_VAULT = "Azure Key Vault"
    HASHICORP_VAULT = "HashiCorp Vault"
    HARDWARE_SECURITY_MODULE = "Hardware Security Module (FIPS 140-2 Level 3)"


class SecurityCertificationTier(str, Enum):
    ENTERPRISE_BACKUP_SECURITY_CERTIFIED = "Enterprise Backup Security Certified"  # 95 - 100
    SECURE_PRODUCTION_READY = "Secure Production Ready"                          # 90 - 94
    SECURITY_IMPROVEMENTS_REQUIRED = "Security Improvements Required"              # 80 - 89
    FAILED = "Failed"                                                              # < 80


@dataclass
class BackupSecurityAssetItem:
    backup_id: str
    asset_type: str  # database, documents, config, secrets, container_image, infrastructure, snapshot, audit_log
    location: str
    owner: str
    data_classification: DataClassificationLevel
    encryption_status: str
    encryption_algorithm: str
    access_policy: str
    retention_policy: str
    creation_time_iso: str
    last_verification_time_iso: str
    checksum_sha256: str
    storage_provider: str
    is_immutable: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BackupSecurityInventoryReport:
    backup_assets: int
    encrypted_assets: int
    unencrypted_assets: int
    assets_by_type: Dict[str, int]
    assets_by_classification: Dict[str, int]
    sample_assets: List[BackupSecurityAssetItem]
    status: str
    passed: bool


@dataclass
class DataClassificationItem:
    category_name: str
    classification_level: DataClassificationLevel
    encryption_enforced: bool
    restricted_access_enforced: bool
    audit_logging_enforced: bool
    retention_control_enforced: bool
    sample_resources: List[str]


@dataclass
class DataClassificationReport:
    total_categories_audited: int
    classification_rules_satisfied: bool
    categories: List[DataClassificationItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BackupEncryptionReport:
    algorithm: str
    encrypted: bool
    encryption_at_rest_verified: bool
    encryption_in_transit_verified: bool
    insecure_formats_rejected: bool  # Rejected plain zip, unencrypted sql, plain json, raw env
    key_rotation: str
    key_id: str
    key_provider: str
    status: str
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyManagementReport:
    master_keys_isolated: bool
    data_encryption_keys_wrapped: bool
    backup_keys_stored_in_kms: bool
    allowed_providers: List[str]
    prohibited_practices_rejected: bool  # Zero keys beside backups, zero keys in git
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyRotationReport:
    automatic_rotation_enabled: bool
    rotation_interval_days: int
    previous_keys_retained: bool
    historic_backups_decryptable: bool
    rotation_simulation_passed: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AccessControlReport:
    least_privilege_enforced: bool
    write_only_backup_service_verified: bool
    read_only_recovery_service_verified: bool
    auditor_read_only_verified: bool
    unauthorized_identities_blocked_count: int
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IAMTestReport:
    unauthorized_user_access_denied: bool
    developer_privilege_escalation_denied: bool
    recovery_identity_access_allowed: bool
    tests_executed_count: int
    tests_passed_count: int
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TamperDetectionReport:
    one_byte_modification_detected: bool
    sha512_hash_comparison_verified: bool
    digital_signature_verification_passed: bool
    tampered_backups_quarantined: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PoisoningProtectionReport:
    malware_scan_pre_restore_passed: bool
    schema_injection_validation_passed: bool
    signature_authenticity_verified: bool
    untrusted_sources_rejected: bool
    suspicious_payloads_blocked_count: int
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImmutabilityReport:
    object_lock_compliance_mode_active: bool
    worm_storage_enforced: bool
    deletion_attempts_denied: bool
    modification_attempts_denied: bool
    overwrite_attempts_denied: bool
    retention_period_enforced_days: int
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditReport:
    all_operations_logged: bool
    operations_tracked: List[str]  # Read, Write, Delete, Restore, Download, Permission Change
    log_tamper_proofing_active: bool
    audit_trail_complete: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RetentionSecurityReport:
    retention_period_verified: bool
    deletion_policy_secure: bool
    legal_hold_supported: bool
    crypto_shredding_expired_backups: bool
    protected_backups_immutable: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BackupSecurityComplianceReport:
    nist_sp_800_53_aligned: bool
    nist_sp_800_57_aligned: bool
    owasp_asvs_aligned: bool
    owasp_secrets_management_aligned: bool
    cis_benchmarks_aligned: bool
    iso_27001_aligned: bool
    soc_2_aligned: bool
    gdpr_security_principles_aligned: bool
    compliance_score_percent: float
    passed: bool
    frameworks: Dict[str, Dict[str, Any]] = field(default_factory=dict)


@dataclass
class BackupSecurityQualityScorecard:
    encryption_score: float             # Weight 25%
    access_control_score: float         # Weight 20%
    integrity_protection_score: float   # Weight 20%
    key_management_score: float         # Weight 15%
    auditability_score: float           # Weight 10%
    compliance_score: float             # Weight 10%
    composite_score: float              # 0 - 100
    certification_tier: SecurityCertificationTier
    passed: bool
    execution_duration_ms: float
    audit_metadata: Dict[str, Any] = field(default_factory=dict)
