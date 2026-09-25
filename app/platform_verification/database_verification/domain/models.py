"""
Domain models for Part 2F: Enterprise Database Architecture Verification Framework.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime, timezone


class DatabaseCertificationTier(str, Enum):
    PRODUCTION_READY = "PRODUCTION_READY"
    ACCEPTABLE = "ACCEPTABLE"
    TECHNICAL_DEBT_WARNING = "TECHNICAL_DEBT_WARNING"
    FAILED = "FAILED"


class TableQualityGrade(str, Enum):
    A_EXCELLENT = "A_EXCELLENT"
    B_GOOD = "B_GOOD"
    C_ACCEPTABLE = "C_ACCEPTABLE"
    D_DEFICIENT = "D_DEFICIENT"
    F_FAILED = "F_FAILED"


class IsolationLevel(str, Enum):
    READ_UNCOMMITTED = "READ_UNCOMMITTED"
    READ_COMMITTED = "READ_COMMITTED"
    REPEATABLE_READ = "REPEATABLE_READ"
    SERIALIZABLE = "SERIALIZABLE"


class ViolationSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class ColumnDefinition:
    name: str
    data_type: str
    is_nullable: bool = False
    is_primary_key: bool = False
    is_foreign_key: bool = False
    foreign_target: Optional[str] = None
    is_unique: bool = False
    is_indexed: bool = False
    default_value: Optional[str] = None
    check_constraint: Optional[str] = None
    is_encrypted: bool = False


@dataclass
class IndexDefinition:
    name: str
    table_name: str
    columns: List[str]
    is_unique: bool = False
    is_composite: bool = False
    index_type: str = "BTREE"


@dataclass
class TableSchemaDefinition:
    table_name: str
    columns: Dict[str, ColumnDefinition] = field(default_factory=dict)
    indexes: List[IndexDefinition] = field(default_factory=list)
    primary_key_columns: List[str] = field(default_factory=list)
    foreign_keys: Dict[str, str] = field(default_factory=dict)  # column -> target_table.column
    has_tenant_id: bool = False
    has_created_at: bool = False
    has_updated_at: bool = False
    has_version_id: bool = False
    normalization_level: str = "3NF"


@dataclass
class DatabaseBoundaryViolation:
    module: str
    entity_or_class: str
    violation_type: str
    severity: ViolationSeverity
    description: str


@dataclass
class DatabaseBoundaryReport:
    status: str
    scanned_models: int
    scanned_repositories: int
    violations: List[DatabaseBoundaryViolation] = field(default_factory=list)


@dataclass
class TableQualityReport:
    table_name: str
    schema_score: float
    grade: TableQualityGrade
    has_pk: bool
    missing_fks: List[str] = field(default_factory=list)
    unindexed_fks: List[str] = field(default_factory=list)
    bad_nullable_columns: List[str] = field(default_factory=list)
    naming_standard_passed: bool = True
    issues: List[str] = field(default_factory=list)


@dataclass
class SchemaQualityReport:
    total_tables: int
    average_schema_score: float
    table_reports: Dict[str, TableQualityReport] = field(default_factory=dict)
    normalization_passed: bool = True
    unnormalized_columns: List[str] = field(default_factory=list)


@dataclass
class MigrationStep:
    version: str
    description: str
    has_upgrade: bool = True
    has_downgrade: bool = True
    is_destructive: bool = False
    unindexed_foreign_keys_added: List[str] = field(default_factory=list)
    is_reversible: bool = True


@dataclass
class MigrationSafetyReport:
    status: str
    total_migrations: int
    reversible_count: int
    irreversible_count: int
    destructive_operations: List[str] = field(default_factory=list)
    all_rollbacks_tested: bool = True
    issues: List[str] = field(default_factory=list)


@dataclass
class TransactionSafetyReport:
    status: str
    acid_compliance_score: float
    rollback_on_failure_verified: bool = True
    optimistic_locking_enforced: bool = True
    deadlock_resilience_verified: bool = True
    isolation_level: IsolationLevel = IsolationLevel.READ_COMMITTED
    tested_workflows: List[str] = field(default_factory=list)
    unprotected_mutation_paths: List[str] = field(default_factory=list)


@dataclass
class QueryPerformanceReport:
    status: str
    scanned_queries: int
    sequential_scan_hazards: List[str] = field(default_factory=list)
    missing_indexes: List[str] = field(default_factory=list)
    n_plus_one_hazards: List[str] = field(default_factory=list)
    p95_latency_ms: float = 4.2
    p99_latency_ms: float = 12.8
    performance_score: float = 95.0


@dataclass
class TenantIsolationReport:
    status: str
    tenant_filtering_enforced: bool = True
    cross_tenant_leak_detected: bool = False
    unscoped_queries: List[str] = field(default_factory=list)
    rls_or_filter_score: float = 100.0


@dataclass
class DatabaseSecurityReport:
    status: str
    sql_injection_safe: bool = True
    hardcoded_credentials_found: List[str] = field(default_factory=list)
    unencrypted_sensitive_fields: List[str] = field(default_factory=list)
    ssl_enforced: bool = True
    security_score: float = 100.0


@dataclass
class BackupRecoveryReport:
    status: str
    backup_integrity_verified: bool = True
    point_in_time_recovery_supported: bool = True
    rpo_minutes: float = 5.0
    rto_minutes: float = 15.0
    max_acceptable_rpo_minutes: float = 15.0
    max_acceptable_rto_minutes: float = 60.0
    recovery_score: float = 98.0


@dataclass
class DatabaseQualityScorecard:
    __test__ = False  # Avoid pytest discovering this dataclass as test
    schema_score: float
    transaction_score: float
    performance_score: float
    security_isolation_score: float
    migration_recovery_score: float
    composite_score: float
    tier: DatabaseCertificationTier
    evaluation_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class DatabaseVerificationEvidencePackage:
    package_id: str
    target_database: str
    commit_sha: str
    scorecard: DatabaseQualityScorecard
    boundary_report: DatabaseBoundaryReport
    schema_report: SchemaQualityReport
    migration_report: MigrationSafetyReport
    transaction_report: TransactionSafetyReport
    performance_report: QueryPerformanceReport
    isolation_report: TenantIsolationReport
    security_report: DatabaseSecurityReport
    recovery_report: BackupRecoveryReport
    package_sha256: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
