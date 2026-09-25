"""
Domain Models for Enterprise Configuration, Secret & Cryptographic Material Backup Verification Platform (Part 3G.2D).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional


class ConfigurationSourceType(str, Enum):
    ENV_FILE = "ENV_FILE"
    YAML = "YAML"
    JSON = "JSON"
    TOML = "TOML"
    INI = "INI"
    DOCKER_COMPOSE = "DOCKER_COMPOSE"
    DOCKER_SECRETS = "DOCKER_SECRETS"
    KUBERNETES_CONFIGMAP = "KUBERNETES_CONFIGMAP"
    KUBERNETES_SECRET = "KUBERNETES_SECRET"
    HELM_VALUES = "HELM_VALUES"
    TERRAFORM_VARIABLES = "TERRAFORM_VARIABLES"
    ANSIBLE_INVENTORY = "ANSIBLE_INVENTORY"
    GITHUB_ACTIONS_SECRETS = "GITHUB_ACTIONS_SECRETS"
    GITLAB_CI_VARIABLES = "GITLAB_CI_VARIABLES"
    CLOUD_SECRET_MANAGER = "CLOUD_SECRET_MANAGER"


class ConfigurationCategory(str, Enum):
    APPLICATION = "Application"
    INFRASTRUCTURE = "Infrastructure"
    NETWORKING = "Networking"
    DATABASE = "Database"
    STORAGE = "Storage"
    AUTHENTICATION = "Authentication"
    AUTHORIZATION = "Authorization"
    MONITORING = "Monitoring"
    AI_PROVIDERS = "AI Providers"
    OCR_PROVIDERS = "OCR Providers"
    WORKER_RUNTIME = "Worker Runtime"
    SCHEDULER = "Scheduler"
    FEATURE_FLAGS = "Feature Flags"
    RATE_LIMITS = "Rate Limits"
    SECURITY = "Security"
    OBSERVABILITY = "Observability"
    LOGGING = "Logging"
    TELEMETRY = "Telemetry"


class ConfigurationSensitivity(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    RESTRICTED = "RESTRICTED"
    CONFIDENTIAL_SECRET = "CONFIDENTIAL_SECRET"


class SecretType(str, Enum):
    JWT_SIGNING_KEY = "JWT_SIGNING_KEY"
    API_KEY = "API_KEY"
    DATABASE_PASSWORD = "DATABASE_PASSWORD"
    REDIS_PASSWORD = "REDIS_PASSWORD"
    OAUTH_SECRET = "OAUTH_SECRET"
    PRIVATE_KEY = "PRIVATE_KEY"
    TLS_CERTIFICATE = "TLS_CERTIFICATE"
    ENCRYPTION_KEY = "ENCRYPTION_KEY"
    WEBHOOK_SECRET = "WEBHOOK_SECRET"
    SERVICE_ACCOUNT_TOKEN = "SERVICE_ACCOUNT_TOKEN"


class KeyAlgorithm(str, Enum):
    AES_256_GCM = "AES_256_GCM"
    RSA_4096 = "RSA_4096"
    ECC_SECP256R1 = "ECC_SECP256R1"
    ED25519 = "ED25519"
    HMAC_SHA256 = "HMAC_SHA256"


class ConfigCertificationTier(str, Enum):
    ENTERPRISE_CERTIFIED = "Enterprise Certified"      # 98 - 100
    PRODUCTION_READY = "Production Ready"              # 95 - 97
    ACCEPTABLE = "Acceptable"                          # 90 - 94
    IMPROVEMENT_REQUIRED = "Improvement Required"      # 80 - 89
    FAILED = "Failed"                                  # < 80


@dataclass
class ConfigurationSourceItem:
    source_id: str
    source_type: ConfigurationSourceType
    location_path: str
    item_count: int
    parser_type: str
    is_encrypted: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConfigurationInventoryReport:
    configuration_sources: int
    environment_variables: int
    config_files: int
    external_secret_stores: int
    sources_detail: List[ConfigurationSourceItem]
    status: str
    passed: bool


@dataclass
class ConfigurationCatalogItem:
    name: str
    category: ConfigurationCategory
    owner: str
    environment: str
    sensitivity: ConfigurationSensitivity
    required: bool
    default_value: Optional[str]
    version: str
    dependencies: List[str]
    backup_strategy: str
    restore_priority: int  # 1 (Highest / Core DB, KMS) -> 5 (Lowest / Telemetry)


@dataclass
class ConfigurationCatalogReport:
    total_catalog_items: int
    categories_covered: List[str]
    items_by_category: Dict[str, int]
    items_by_sensitivity: Dict[str, int]
    catalog_items: List[ConfigurationCatalogItem]
    passed: bool


@dataclass
class ConfigurationValidationReport:
    mandatory_variables_checked: int
    missing_variables: List[str]
    duplicate_definitions: List[str]
    unused_variables: List[str]
    deprecated_variables: List[str]
    conflicting_values: List[str]
    validation_score_percent: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SecretItem:
    secret_id: str
    secret_type: SecretType
    location_found: str
    scanner_detected_by: str
    masked_preview: str
    is_encrypted: bool
    entropy_score: float
    has_active_backup: bool
    rotation_period_days: int
    is_expired: bool = False


@dataclass
class SecretInventoryReport:
    total_secrets_discovered: int
    secrets_by_type: Dict[str, int]
    locations_scanned: List[str]
    scanners_utilized: List[str]
    secrets: List[SecretItem]
    plaintext_exposures_found: int
    passed: bool


@dataclass
class SecretBackupPolicy:
    secret_id: str
    backup_location: str
    encryption_method: str
    owner: str
    rotation_schedule: str
    recovery_procedure: str
    retention_period: str
    integrity_hash: str


@dataclass
class SecretBackupReport:
    total_secrets_audited: int
    secrets_with_valid_backup_policy: int
    unbacked_secrets: List[str]
    plaintext_stored_secrets: List[str]
    shared_credentials_detected: List[str]
    hardcoded_secrets_detected: List[str]
    expired_secrets_detected: List[str]
    backup_coverage_percent: float
    passed: bool
    policies: List[SecretBackupPolicy] = field(default_factory=list)


@dataclass
class EncryptionKeyRecoveryItem:
    key_id: str
    algorithm: KeyAlgorithm
    key_length_bits: int
    creation_date_iso: str
    rotation_status: str
    backup_status: str
    recovery_status: str
    roundtrip_decryption_match: bool


@dataclass
class EncryptionKeyRecoveryReport:
    total_keys_tested: int
    keys_successfully_recovered: int
    all_cryptographic_outputs_identical: bool
    key_recovery_details: List[EncryptionKeyRecoveryItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CertificateRecoveryItem:
    cert_id: str
    cert_type: str  # TLS Ingress, mTLS Service-to-Service, Internal CA, Root CA
    issuer: str
    subject: str
    expiration_date_iso: str
    is_expired: bool
    private_key_present: bool
    key_pair_match_verified: bool
    tls_handshake_successful: bool


@dataclass
class CertificateRecoveryReport:
    total_certificates_tested: int
    certificates_valid: int
    expired_certificates_count: int
    handshake_success_rate_percent: float
    certificates: List[CertificateRecoveryItem]
    passed: bool


@dataclass
class FeatureFlagItem:
    flag_id: str
    description: str
    current_state: bool
    restored_state: bool
    dependencies_preserved: bool
    rollback_supported: bool
    version_compatible: bool


@dataclass
class FeatureFlagRestoreReport:
    total_flags_tested: int
    flags_state_preserved: int
    dependencies_satisfied: bool
    rollback_verification_passed: bool
    feature_flags: List[FeatureFlagItem]
    passed: bool


@dataclass
class InfrastructureConfigurationReport:
    iac_types_verified: List[str]  # Terraform, Helm, Docker Compose, Kubernetes YAML
    provision_fresh_environment_simulated: bool
    provision_duration_seconds: float
    resource_mismatches_count: int
    missing_components_count: int
    infrastructure_drift_percent: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VersionCompatibilityReport:
    application_version: str
    schema_version: str
    migration_version: str
    api_version: str
    provider_version: str
    runtime_version: str
    incompatible_backups_found: int
    migration_paths_verified: bool
    compatibility_score_percent: float
    passed: bool


@dataclass
class ConfigurationDriftItem:
    parameter_name: str
    production_value: str
    backup_value: str
    repository_value: str
    runtime_value: str
    is_drifted: bool
    drift_severity: str  # NONE, LOW, MEDIUM, CRITICAL


@dataclass
class ConfigurationDriftReport:
    total_parameters_audited: int
    drifted_parameters_count: int
    critical_drifts_count: int
    drift_details: List[ConfigurationDriftItem]
    drift_rate_percent: float
    passed: bool


@dataclass
class ConfigurationRestoreSimulationReport:
    clean_environment_provisioned: bool
    secrets_injected_successfully: bool
    services_deployed: List[str]
    all_services_healthy: bool
    database_reachable: bool
    redis_reachable: bool
    ai_providers_authenticated: bool
    monitoring_functional: bool
    execution_duration_seconds: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConfigurationSecurityReport:
    secrets_encrypted_at_rest: bool
    secrets_encrypted_in_transit: bool
    least_privilege_enforced: bool
    zero_plaintext_exports_verified: bool
    tamper_detection_active: bool
    unencrypted_archives_rejected: bool
    shared_keys_rejected: bool
    security_score_percent: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConfigurationComplianceReport:
    nist_sp_800_57_aligned: bool
    nist_sp_800_209_aligned: bool
    owasp_asvs_aligned: bool
    owasp_secrets_management_aligned: bool
    cis_benchmarks_aligned: bool
    iso_27001_aligned: bool
    soc_2_aligned: bool
    cncf_security_aligned: bool
    compliance_score_percent: float
    passed: bool
    frameworks: Dict[str, Dict[str, Any]] = field(default_factory=dict)


@dataclass
class ConfigurationQualityScorecard:
    configuration_coverage_score: float         # Weight 15%
    secret_coverage_encryption_score: float     # Weight 15%
    cryptographic_continuity_score: float       # Weight 15%
    certificate_health_score: float             # Weight 10%
    iac_and_feature_flags_score: float          # Weight 10%
    restore_simulation_score: float             # Weight 15%
    drift_and_version_score: float              # Weight 10%
    security_and_compliance_score: float        # Weight 10%
    composite_score: float                      # 0 - 100
    certification_tier: ConfigCertificationTier
    passed: bool
    execution_duration_ms: float
    audit_metadata: Dict[str, Any] = field(default_factory=dict)
