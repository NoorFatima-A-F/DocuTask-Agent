"""
Domain models for Enterprise Backup Architecture Verification Framework (Part 3G.2A).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional


class AssetCategory(str, Enum):
    DATABASE = "DATABASE"
    CACHE_QUEUE = "CACHE_QUEUE"
    STORAGE_VOLUME = "STORAGE_VOLUME"
    DOCUMENT_DATA = "DOCUMENT_DATA"
    AI_ARTIFACT = "AI_ARTIFACT"
    CONFIGURATION_SECRETS = "CONFIGURATION_SECRETS"
    RUNTIME_STATE = "RUNTIME_STATE"
    OBSERVABILITY = "OBSERVABILITY"
    KNOWLEDGE_BASE = "KNOWLEDGE_BASE"
    EVIDENCE_REGISTRY = "EVIDENCE_REGISTRY"


class CriticalityTier(str, Enum):
    TIER_0 = "Tier0"  # Mission Critical (Immediate recovery, Near-zero RPO)
    TIER_1 = "Tier1"  # Business Critical (High priority, RPO <= 15m - 1h)
    TIER_2 = "Tier2"  # Operational (Standard priority, RPO <= 24h)
    TIER_3 = "Tier3"  # Rebuildable / Non-critical (Optional backup, rebuild on demand)


class BackupStrategyType(str, Enum):
    FULL = "FULL"
    INCREMENTAL = "INCREMENTAL"
    DIFFERENTIAL = "DIFFERENTIAL"
    SNAPSHOT = "SNAPSHOT"
    CONTINUOUS = "CONTINUOUS"  # WAL archiving / event streaming


class LifecycleStage(str, Enum):
    ASSET = "ASSET"
    BACKUP = "BACKUP"
    VERIFICATION = "VERIFICATION"
    STORAGE = "STORAGE"
    REPLICATION = "REPLICATION"
    RETENTION = "RETENTION"
    EXPIRATION = "EXPIRATION"
    SECURE_DESTRUCTION = "SECURE_DESTRUCTION"


class CertificationTier(str, Enum):
    ENTERPRISE_CERTIFIED = "Enterprise Backup Architecture Certified"  # 95 - 100
    PRODUCTION_READY = "Production Ready"                              # 90 - 94
    CONDITIONALLY_READY = "Conditionally Ready"                        # 80 - 89
    DEVELOPMENT_QUALITY = "Development Quality"                        # 70 - 79
    NOT_READY = "Not Ready"                                            # < 70


class VerificationStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"


@dataclass
class AssetInventoryItem:
    name: str
    category: AssetCategory
    criticality: CriticalityTier
    backup_required: bool
    subsystem: str
    data_type: str
    storage_type: str
    size_bytes_estimate: int = 0
    is_discovered: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ClassificationEntry:
    asset_name: str
    category: AssetCategory
    criticality: CriticalityTier
    recovery_priority: str
    max_rpo_seconds: int
    max_rto_seconds: int
    data_loss_tolerance: str
    recovery_tier_rationale: str


@dataclass
class BackupStrategyConfig:
    asset_name: str
    strategy_type: BackupStrategyType
    frequency_cron: str
    estimated_size_mb: float
    retention_days: int
    storage_location: str
    is_continuous: bool = False
    wal_archiving_enabled: bool = False
    dependency_chain: List[str] = field(default_factory=list)
    base_snapshot_id: Optional[str] = None
    encryption_algorithm: str = "AES-256-GCM"


@dataclass
class StrategyValidationResult:
    asset_name: str
    criticality: CriticalityTier
    configured_strategy: BackupStrategyType
    is_adequate: bool
    findings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class DependencyGraphNode:
    name: str
    category: AssetCategory
    criticality: CriticalityTier
    dependencies: List[str] = field(default_factory=list)
    recovery_stage_order: int = 0


@dataclass
class BackupDependencyGraph:
    nodes: Dict[str, DependencyGraphNode]
    topological_recovery_order: List[str]
    is_dag: bool
    has_circular_dependency: bool
    validation_errors: List[str] = field(default_factory=list)


@dataclass
class CoverageMatrixItem:
    asset_name: str
    category: AssetCategory
    criticality: CriticalityTier
    asset_exists: bool
    backup_configured: bool
    schedule_exists: bool
    retention_exists: bool
    backup_verified: bool
    can_restore_happen: bool
    is_fully_covered: bool
    compliance_status: str


@dataclass
class CoverageReport:
    tier0_coverage_percent: float
    tier1_coverage_percent: float
    tier2_coverage_percent: float
    tier3_coverage_percent: float
    total_coverage_percent: float
    tier0_compliant: bool  # 100% required
    tier1_compliant: bool  # 100% required
    tier2_compliant: bool  # >=95% required
    unprotected_assets: List[str]
    items: List[CoverageMatrixItem]


@dataclass
class RetentionPolicyConfig:
    asset_name: str
    daily_retention_days: int
    weekly_retention_weeks: int
    monthly_retention_months: int
    yearly_retention_years: int
    archival_tier: str
    legal_hold_supported: bool
    immutability_enabled: bool
    auto_expiration_enabled: bool
    secure_deletion_method: str  # Crypto-shredding / NIST 800-88 sanitization


@dataclass
class RetentionValidationResult:
    asset_name: str
    retention_defined: bool
    has_infinite_retention: bool
    has_accidental_purge_risk: bool
    legal_hold_compliant: bool
    immutability_verified: bool
    is_valid: bool
    details: List[str] = field(default_factory=list)


@dataclass
class LifecycleStageRecord:
    stage: LifecycleStage
    is_implemented: bool
    automated: bool
    sla_seconds: int
    verification_method: str
    audit_trail_recorded: bool


@dataclass
class LifecycleValidationReport:
    asset_name: str
    stages: Dict[str, LifecycleStageRecord]
    has_orphaned_backups: bool
    has_expired_backups_retained: bool
    has_missing_deletion_records: bool
    lifecycle_complete: bool
    audit_findings: List[str] = field(default_factory=list)


@dataclass
class BackupOwnershipRecord:
    asset_name: str
    owner_team: str
    subsystem: str
    automation_system: str
    schedule_expression: str
    restore_owner_team: str
    verification_owner_team: str
    escalation_contact: str
    has_assigned_owners: bool


@dataclass
class BackupMetadataEntry:
    backup_uuid: str
    asset_name: str
    timestamp_iso: str
    git_commit_sha: str
    platform_version: str
    environment: str
    encryption_status: str
    encryption_key_id: str
    compression_algorithm: str
    compression_ratio: float
    sha256_checksum: str
    backup_type: BackupStrategyType
    retention_policy_name: str
    verification_status: VerificationStatus
    size_bytes: int


@dataclass
class PolicyValidationResult:
    policy_id: str
    policy_name: str
    asset_pattern: str
    schedule_valid: bool
    destination_valid: bool
    encryption_enforced: bool
    retention_enforced: bool
    validation_hook_configured: bool
    notification_configured: bool
    restore_testing_scheduled: bool
    is_valid: bool
    conflicts_detected: List[str] = field(default_factory=list)


@dataclass
class ArchitectureConsistencyReport:
    no_nonexistent_asset_references: bool
    no_nonexistent_policy_references: bool
    no_deleted_storage_references: bool
    no_cyclic_backup_dependencies: bool
    no_circular_restore_chains: bool
    passed: bool
    inconsistencies: List[str] = field(default_factory=list)


@dataclass
class BackupMetricsReport:
    backup_success_rate_percent: float
    avg_backup_duration_seconds: float
    total_backup_size_gb: float
    avg_compression_ratio: float
    storage_growth_rate_gb_day: float
    retention_utilization_percent: float
    overall_coverage_percent: float
    verification_success_percent: float
    tier0_coverage_percent: float
    tier1_coverage_percent: float
    tier2_coverage_percent: float
    tier3_coverage_percent: float
    avg_backup_age_hours: float
    stale_backup_count: int
    prometheus_metrics: str
    opentelemetry_metrics: Dict[str, Any]
    grafana_dashboard_json: Dict[str, Any]


@dataclass
class BackupReadinessScorecard:
    asset_discovery_score: float         # Weight 10%
    classification_score: float          # Weight 10%
    strategy_quality_score: float        # Weight 20%
    coverage_score: float                # Weight 20%
    retention_score: float               # Weight 10%
    lifecycle_score: float               # Weight 10%
    metadata_score: float                # Weight 10%
    observability_score: float           # Weight 5%
    policy_validation_score: float       # Weight 5%
    readiness_composite_score: float     # 0 - 100
    certification_tier: CertificationTier
    passed: bool
    execution_duration_ms: float
    verification_metadata: Dict[str, Any] = field(default_factory=dict)
