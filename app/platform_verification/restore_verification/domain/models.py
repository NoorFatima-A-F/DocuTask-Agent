"""
Domain Models for Enterprise Automated Restore Verification System (Part 3G.2E).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any


class RestoreExecutionMode(str, Enum):
    FULL_RESTORE = "FULL_RESTORE"
    PARTIAL_RESTORE = "PARTIAL_RESTORE"
    COMPONENT_RESTORE = "COMPONENT_RESTORE"
    SCHEDULED_DRILL = "SCHEDULED_DRILL"
    EMERGENCY_RECOVERY = "EMERGENCY_RECOVERY"


class RestoreComponentType(str, Enum):
    INFRASTRUCTURE = "infrastructure"
    NETWORK = "network"
    SECRETS = "secrets"
    DATABASE = "database"
    STORAGE = "storage"
    QUEUE = "queue"
    BACKEND = "backend"
    WORKERS = "workers"
    FRONTEND = "frontend"
    MONITORING = "monitoring"


class RestoreCertificationTier(str, Enum):
    DISASTER_RECOVERY_CERTIFIED = "Disaster Recovery Certified"  # 95 - 100
    RECOVERY_READY = "Recovery Ready"                          # 90 - 94
    IMPROVEMENT_REQUIRED = "Improvement Required"              # 80 - 89
    FAILED = "Failed"                                          # < 80


@dataclass
class RestoreExecutionPlan:
    restore_id: str
    backup_timestamp: str
    mode: RestoreExecutionMode
    components: List[str]
    dependency_order: List[str]
    status: str
    created_at_iso: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RecoveryEnvironmentReport:
    environment_type: str  # ephemeral-docker-compose / ephemeral-k8s-namespace
    environment_name: str
    resources_created: int
    configuration_loaded: bool
    network_isolated: bool
    teardown_successful: bool
    creation_duration_seconds: float
    teardown_duration_seconds: float
    status: str
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BackupCatalogItem:
    backup_id: str
    backup_type: str  # full, differential, wal_archive, object_snapshot, config_vault
    source: str
    timestamp_iso: str
    version: str
    size_bytes: int
    checksum_sha256: str
    encryption_status: str
    is_verified: bool
    dependencies: List[str]


@dataclass
class BackupCatalogReport:
    total_backups_discovered: int
    total_backup_size_bytes: int
    backups: List[BackupCatalogItem]
    sources_audited: List[str]
    all_checksums_verified: bool
    passed: bool


@dataclass
class DatabaseRestoreValidationReport:
    tables_restored: int
    indexes_restored: int
    constraints_restored: int
    extensions_restored: int
    document_count_before_backup: int
    document_count_after_restore: int
    row_count_match: bool
    foreign_key_integrity_verified: bool
    checksum_match: bool
    consistency_tests_passed: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentRestoreValidationReport:
    total_documents_verified: int
    sha256_equality_verified: bool
    metadata_preserved: bool
    permissions_ownership_preserved: bool
    large_files_verified: Dict[str, bool]  # 10MB, 100MB, 1GB+
    total_payload_bytes_verified: int
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConfigurationRestoreValidationReport:
    environment_variables_restored: int
    feature_flags_restored: int
    runtime_policies_restored: int
    original_config_hash: str
    restored_config_hash: str
    config_hashes_identical: bool
    missing_values_count: int
    unexpected_values_count: int
    passed: bool


@dataclass
class SecretRestoreValidationReport:
    jwt_secret_recovered: bool
    jwt_token_validation_successful: bool
    database_credentials_authenticated: bool
    redis_credentials_authenticated: bool
    encryption_key_decryption_successful: bool
    zero_plaintext_leakage: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ServiceHealthStatus:
    service_name: str
    health_endpoint: str
    ready_endpoint: str
    live_endpoint: str
    http_status: int
    response_time_ms: float
    is_healthy: bool


@dataclass
class ServiceStartupReport:
    total_services_started: int
    services: List[ServiceHealthStatus]
    all_endpoints_healthy: bool
    startup_duration_seconds: float
    passed: bool


@dataclass
class SyntheticWorkflowResult:
    workflow_name: str
    description: str
    steps_executed: List[str]
    execution_time_seconds: float
    output_verified: bool
    status: str


@dataclass
class FunctionalRecoveryReport:
    workflows_executed: int
    workflows_passed: int
    document_processing_pipeline_functional: bool
    agent_planner_executor_functional: bool
    authentication_rbac_functional: bool
    results: List[SyntheticWorkflowResult]
    passed: bool


@dataclass
class IntegrityValidationReport:
    backup_checksum: str
    restore_checksum: str
    runtime_checksum: str
    triple_checksum_matched: bool
    corrupted_blocks_found: int
    tamper_evidence_detected: bool
    passed: bool


@dataclass
class RTORPOReport:
    measured_rto_minutes: float
    target_rto_minutes: float
    measured_rpo_minutes: float
    target_rpo_minutes: float
    restore_start_time_iso: str
    restore_end_time_iso: str
    service_ready_time_iso: str
    first_successful_transaction_time_iso: str
    rto_within_sla: bool
    rpo_within_sla: bool
    passed: bool


@dataclass
class FailureSimulationItem:
    scenario_name: str
    injected_fault: str
    expected_action: str
    actual_action: str
    rollback_successful: bool
    passed: bool


@dataclass
class FailureSimulationReport:
    total_scenarios_tested: int
    scenarios_passed: int
    failure_handling_verified: bool
    scenarios: List[FailureSimulationItem]
    passed: bool


@dataclass
class RestoreQualityScorecard:
    backup_recovery_success_score: float  # Weight 25%
    data_integrity_score: float           # Weight 20%
    service_recovery_score: float         # Weight 20%
    functional_validation_score: float    # Weight 15%
    security_validation_score: float      # Weight 10%
    recovery_speed_score: float           # Weight 10%
    composite_score: float                # 0 - 100
    certification_tier: RestoreCertificationTier
    passed: bool
    execution_duration_ms: float
    audit_metadata: Dict[str, Any] = field(default_factory=dict)
