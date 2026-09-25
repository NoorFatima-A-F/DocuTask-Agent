"""
Domain models for Enterprise Database Backup & Recovery Verification Platform (Part 3G.2B Advanced).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any


class DatabaseBackupStrategyType(str, Enum):
    FULL_BACKUP = "FULL_BACKUP"
    INCREMENTAL_BACKUP = "INCREMENTAL_BACKUP"
    DIFFERENTIAL_BACKUP = "DIFFERENTIAL_BACKUP"
    CONTINUOUS_WAL = "CONTINUOUS_WAL"
    POINT_IN_TIME_RECOVERY = "POINT_IN_TIME_RECOVERY"
    SNAPSHOT_BACKUP = "SNAPSHOT_BACKUP"
    COLD_BACKUP = "COLD_BACKUP"
    HOT_BACKUP = "HOT_BACKUP"
    LOGICAL_BACKUP = "LOGICAL_BACKUP"
    PHYSICAL_BACKUP = "PHYSICAL_BACKUP"


class CorruptionSeverity(str, Enum):
    RECOVERABLE = "Recoverable"
    PARTIALLY_RECOVERABLE = "Partially Recoverable"
    IRRECOVERABLE = "Irrecoverable"


class DBCertificationTier(str, Enum):
    ENTERPRISE_PLATINUM = "Enterprise Platinum"          # 98 - 100
    ENTERPRISE_CERTIFIED = "Enterprise Certified"        # 95 - 97
    PRODUCTION_READY = "Production Ready"                # 90 - 94
    CONDITIONALLY_READY = "Conditionally Ready"          # 80 - 89
    DEVELOPMENT_GRADE = "Development Grade"              # 70 - 79
    FAILED = "Failed"                                    # < 70


@dataclass
class DatabaseInventoryItem:
    object_id: str
    object_name: str
    object_kind: str  # table, index, sequence, view, partition, function, trigger, role, etc.
    schema_name: str
    owner_role: str
    size_bytes: int
    is_protected: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DatabaseInventoryReport:
    total_objects_discovered: int
    objects_by_kind: Dict[str, int]
    schemas_discovered: List[str]
    roles_discovered: List[str]
    replication_slots_count: int
    publications_count: int
    subscriptions_count: int
    inventory_items: List[DatabaseInventoryItem]
    passed: bool


@dataclass
class BackupCoverageReport:
    objects_discovered: int
    objects_backed_up: int
    coverage_percent: float
    missing_objects: List[str]
    coverage_by_kind: Dict[str, float]
    passed: bool


@dataclass
class LogicalBackupReport:
    backup_tool: str
    database_name: str
    total_tables: int
    total_indexes: int
    total_constraints: int
    total_sequences: int
    total_views: int
    total_triggers: int
    total_functions: int
    total_custom_types: int
    total_extensions: int
    formats_tested: List[str] = field(default_factory=lambda: ["custom", "directory", "tar", "plain"])
    schema_names: List[str] = field(default_factory=list)
    roles_and_acls_preserved: bool = True
    roles_and_privileges_captured: bool = True
    generated_columns_preserved: bool = True
    partition_metadata_preserved: bool = True
    schema_completeness_verified: bool = True
    row_counts_verified: bool = True
    execution_duration_seconds: float = 0.0
    archive_size_bytes: int = 0
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PhysicalBackupReport:
    backup_method: str
    cluster_version: str
    data_directory_complete: bool = True
    control_file_valid: bool = True
    wal_segments_consistent: bool = True
    timeline_history_valid: bool = True
    checkpoint_lsn: str = ""
    checkpoint_redo_lsn: str = ""
    tablespaces_captured: List[str] = field(default_factory=list)
    replication_metadata_intact: bool = True
    execution_duration_seconds: float = 0.0
    total_size_bytes: int = 0
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WALVerificationReport:
    timeline_id: int
    start_lsn: str
    end_lsn: str
    archived_segments_count: int
    missing_segments: List[str] = field(default_factory=list)
    missing_segments_detected: List[str] = field(default_factory=list)
    duplicate_segments: List[str] = field(default_factory=list)
    archive_continuity_verified: bool = True
    timeline_integrity_verified: bool = True
    checksum_validity_percent: float = 100.0
    archive_latency_seconds: float = 0.5
    replay_simulation_successful: bool = True
    replay_duration_seconds: float = 0.0
    replay_throughput_mb_s: float = 0.0
    replay_timeline_events: List[Dict[str, Any]] = field(default_factory=list)
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PITRCheckpointResult:
    checkpoint_name: str
    target_time_iso: str
    target_lsn: str
    injected_workload_description: str = ""
    injected_operations_count: int = 0
    restored_record_count: int = 0
    expected_record_count: int = 0
    replay_duration_seconds: float = 0.0
    replay_throughput_mb_s: float = 0.0
    accuracy_percent: float = 100.0
    passed: bool = True


@dataclass
class PITRReport:
    total_checkpoints_tested: int
    passed_checkpoints_count: int
    overall_accuracy_percent: float
    avg_replay_duration_seconds: float
    avg_replay_throughput_mb_s: float
    checkpoints: List[PITRCheckpointResult]
    passed: bool


@dataclass
class TransactionConsistencyReport:
    acid_compliance_verified: bool
    mvcc_snapshot_isolation_verified: bool
    concurrent_writers_tested: int
    savepoints_tested: int
    rollbacks_tested: int
    deadlocks_resolved_gracefully: bool
    zero_partial_transactions: bool
    consistency_score_percent: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReplicationVerificationReport:
    primary_to_standby_replication_verified: bool
    standby_to_backup_verified: bool
    restore_from_standby_backup_verified: bool
    replication_lag_seconds: float
    replication_slots_healthy: bool
    failover_compatibility_verified: bool
    promotion_correctness_verified: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SchemaEvolutionReport:
    alembic_chain_length: int
    forward_migration_verified: bool
    rollback_downgrade_verified: bool
    reapply_forward_idempotent: bool
    cross_version_compatibility: Dict[str, str]
    incompatible_objects: List[str]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CorruptionClassificationItem:
    scenario_id: str
    fault_description: str
    injected_corruption_type: str
    detected_pre_restore: bool
    classification: CorruptionSeverity
    mitigation_action: str


@dataclass
class CorruptionClassificationReport:
    total_faults_injected: int
    detected_faults_count: int
    recoverable_count: int
    partially_recoverable_count: int
    irrecoverable_count: int
    detection_rate_percent: float
    scenarios: List[CorruptionClassificationItem]
    passed: bool


@dataclass
class DataIntegrityReport:
    total_tables_checked: int
    row_count_accuracy_percent: float
    table_checksum_hashes_matched: bool
    foreign_key_violations_count: int
    orphan_rows_count: int
    duplicate_keys_count: int
    sequence_alignment_verified: bool
    field_level_sampling_matches: int
    field_level_sampling_total: int
    field_accuracy_percent: float
    passed: bool


@dataclass
class CryptographicVerificationReport:
    backup_archive_sha256: str
    wal_archive_sha256: str
    metadata_manifest_sha256: str
    digital_signature_algorithm: str
    signature_verified: bool
    tamper_evident_seal_intact: bool
    passed: bool


@dataclass
class DatabaseSecurityReport:
    encryption_at_rest_verified: bool = True  # AES-256-GCM
    encryption_in_transit_verified: bool = True  # TLS 1.3
    tls_in_transit_verified: bool = True
    key_rotation_compatibility_verified: bool = True
    kms_key_management_verified: bool = True
    rbac_least_privilege_enforced: bool = True
    rbac_access_control_enforced: bool = True
    immutable_worm_storage_verified: bool = True
    access_logs_complete: bool = True
    audit_logging_active: bool = True
    audit_trail_provenance_verified: bool = True
    credential_isolation_verified: bool = True
    unauthorized_restore_blocked: bool = True
    passed: bool = True
    security_audit_events: List[str] = field(default_factory=list)
    security_events: List[str] = field(default_factory=list)


@dataclass
class PerformanceBenchmarkingReport:
    backup_duration_seconds: float
    backup_throughput_mb_s: float
    compression_ratio: float
    restore_duration_seconds: float
    restore_throughput_mb_s: float
    wal_replay_speed_mb_s: float = 0.0
    cpu_utilization_percent: float = 0.0
    memory_utilization_mb: float = 0.0
    storage_bandwidth_mb_s: float = 0.0
    storage_io_read_mb_s: float = 0.0
    storage_io_write_mb_s: float = 0.0
    rto_seconds: float = 0.0
    rpo_seconds: float = 0.0
    p95_restore_latency_seconds: float = 0.0
    p99_restore_latency_seconds: float = 0.0
    variance: float = 0.0
    statistical_summary: Dict[str, float] = field(default_factory=dict)
    passed: bool = True


@dataclass
class AutomatedRestoreReport:
    restore_workflow_stages: List[Dict[str, Any]] = field(default_factory=list)
    isolated_instance_provisioned: bool = True
    restore_execution_successful: bool = True
    application_startup_healthy: bool = True
    smoke_tests_passed: bool = True
    health_checks_passed: bool = True
    auth_endpoints_operational: bool = True
    document_upload_verified: bool = True
    workflow_execution_verified: bool = True
    ai_processing_verified: bool = True
    verification_apis_functional: bool = True
    zero_manual_steps: bool = True
    execution_duration_seconds: float = 0.0
    passed: bool = True


@dataclass
class ForensicReport:
    chain_of_custody_id: str
    provenance_timestamp: str
    source_database_host: str
    backup_storage_uri: str
    operator_identity: str
    sha256_digest: str
    digital_signature: str
    verification_audit_trail: List[Dict[str, Any]]
    passed: bool


@dataclass
class ContinuousVerificationScheduleReport:
    daily_logical_verification_active: bool
    weekly_physical_restore_active: bool
    monthly_disaster_simulation_active: bool
    quarterly_recovery_certification_active: bool
    stale_backup_detected: bool
    next_scheduled_runs: Dict[str, str]
    passed: bool


@dataclass
class QualityScorecard:
    recoverability_score: float     # Weight 25%
    consistency_score: float        # Weight 20%
    integrity_score: float          # Weight 15%
    security_score: float           # Weight 15%
    performance_score: float        # Weight 10%
    compatibility_score: float      # Weight 5%
    automation_score: float         # Weight 5%
    evidence_quality_score: float   # Weight 5%
    composite_score: float          # 0 - 100
    certification_tier: DBCertificationTier
    passed: bool
    execution_duration_ms: float
    audit_metadata: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Backwards Compatibility Enums & Models (for core subsystem interfaces)
# ---------------------------------------------------------------------------
class PostgresObjectKind(str, Enum):
    TABLE = "table"
    INDEX = "index"
    CONSTRAINT = "constraint"
    SEQUENCE = "sequence"
    VIEW = "view"
    TRIGGER = "trigger"
    FUNCTION = "function"
    TYPE_ENUM = "type_enum"
    EXTENSION = "extension"
    ROLE = "role"
    SCHEMA = "schema"


class CorruptionType(str, Enum):
    TRUNCATED_ARCHIVE = "TRUNCATED_ARCHIVE"
    MODIFIED_BYTES = "MODIFIED_BYTES"
    DAMAGED_WAL_SEGMENT = "DAMAGED_WAL_SEGMENT"
    MISSING_CONTROL_FILE = "MISSING_CONTROL_FILE"
    ALTERED_METADATA = "ALTERED_METADATA"
    INVALID_COMPRESSION = "INVALID_COMPRESSION"


@dataclass
class DatabaseBackupStrategyEntry:
    strategy_name: str
    strategy_type: DatabaseBackupStrategyType
    supported: bool
    backup_mechanism: str
    target_rpo: str
    target_rto: str
    compression_algorithm: str
    encryption_standard: str
    storage_tier: str
    immutability_enabled: bool
    verification_frequency: str


@dataclass
class SchemaComparisonReport:
    source_database_name: str
    restored_database_name: str
    tables_match: bool
    indexes_match: bool
    constraints_match: bool
    sequences_match: bool
    views_match: bool
    triggers_match: bool
    functions_match: bool
    types_and_enums_match: bool
    extensions_match: bool
    missing_objects: List[str]
    differing_definitions: List[Dict[str, Any]]
    similarity_score_percent: float
    passed: bool


@dataclass
class DataConsistencyReport:
    total_tables_checked: int
    matching_tables_count: int
    row_count_differences: Dict[str, Dict[str, int]]
    checksum_differences: Dict[str, Dict[str, str]]
    foreign_key_violations_count: int
    orphan_records_count: int
    sequence_alignment_verified: bool
    unique_constraints_verified: bool
    transaction_boundary_intact: bool
    no_partial_transactions: bool
    consistency_score_percent: float
    passed: bool


@dataclass
class CorruptionDetectionReport:
    total_faults_injected: int
    detected_faults_count: int
    prevented_restores_count: int
    detection_rate_percent: float
    fault_scenarios: List[Dict[str, Any]]
    passed: bool


@dataclass
class MigrationValidationReport:
    supported_versions_tested: List[str]
    alembic_chain_length: int
    migration_ordering_verified: bool
    schema_valid_after_migration: bool
    rollback_compatibility_verified: bool
    migration_idempotency_verified: bool
    incompatible_objects: List[str]
    passed: bool


@dataclass
class PerformanceMetricsReport:
    backup_duration_seconds: float
    backup_throughput_mb_s: float
    compression_ratio: float
    restore_duration_seconds: float
    restore_throughput_mb_s: float
    wal_replay_speed_mb_s: float = 0.0
    cpu_utilization_percent: float = 0.0
    memory_utilization_mb: float = 0.0
    storage_bandwidth_mb_s: float = 0.0
    storage_io_read_mb_s: float = 0.0
    storage_io_write_mb_s: float = 0.0
    rto_seconds: float = 0.0
    rpo_seconds: float = 0.0
    p95_restore_latency_seconds: float = 0.0
    p99_restore_latency_seconds: float = 0.0
    variance: float = 0.0
    passed: bool = True



@dataclass
class RecoveryMetricsReport:
    target_rto_seconds: float = 300.0
    rto_target_seconds: float = 300.0
    actual_rto_seconds: float = 0.0
    rto_compliant: bool = True
    target_rpo_seconds: float = 60.0
    rpo_target_seconds: float = 60.0
    actual_rpo_seconds: float = 0.0
    rpo_compliant: bool = True
    simulated_failure_scenarios: List[Dict[str, Any]] = field(default_factory=list)
    passed: bool = True



@dataclass
class DatabaseReadinessScorecard:
    recoverability_score: float
    integrity_score: float
    consistency_score: float
    performance_score: float
    security_score: float
    compatibility_score: float
    automation_score: float
    composite_score: float
    certification_tier: DBCertificationTier
    passed: bool
    execution_duration_ms: float
    category_breakdown: Dict[str, float] = field(default_factory=dict)

