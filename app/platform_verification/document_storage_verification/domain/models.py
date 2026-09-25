"""
Domain Models for Enterprise Document Storage Backup & Recovery Verification Framework (Part 3G.2C).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any


class StorageArtifactCategory(str, Enum):
    ORIGINAL_DOCUMENTS = "Original Documents"
    OCR_ARTIFACTS = "OCR Artifacts"
    AI_EXTRACTION_RESULTS = "AI Extraction Results"
    EVIDENCE_FILES = "Evidence Files"
    VERIFICATION_REPORTS = "Verification Reports"
    GENERATED_REPORTS = "Generated Reports"
    TEMPORARY_OBJECTS = "Temporary Objects"
    ARCHIVED_OBJECTS = "Archived Objects"
    AUDIT_PACKAGES = "Audit Packages"
    EMBEDDINGS = "Embeddings"


class StorageProviderType(str, Enum):
    LOCAL_FILESYSTEM = "Local Filesystem"
    MINIO = "MinIO Object Storage"
    AMAZON_S3 = "Amazon S3"
    GOOGLE_CLOUD_STORAGE = "Google Cloud Storage"
    AZURE_BLOB_STORAGE = "Azure Blob Storage"
    S3_COMPATIBLE = "S3-Compatible Generic"


class StorageCorruptionType(str, Enum):
    TRUNCATED_FILE = "TRUNCATED_FILE"
    MODIFIED_BYTES = "MODIFIED_BYTES"
    RENAMED_FILE = "RENAMED_FILE"
    INCORRECT_MIME = "INCORRECT_MIME"
    INVALID_ENCODING = "INVALID_ENCODING"
    DAMAGED_PDF = "DAMAGED_PDF"
    MISSING_PAGES = "MISSING_PAGES"


class StorageCertificationTier(str, Enum):
    ENTERPRISE_STORAGE_CERTIFIED = "Enterprise Storage Certified"  # 98 - 100
    ENTERPRISE_READY = "Enterprise Ready"                        # 95 - 97
    PRODUCTION_READY = "Production Ready"                        # 90 - 94
    CONDITIONALLY_READY = "Conditionally Ready"                  # 80 - 89
    DEVELOPMENT_GRADE = "Development Grade"                      # 70 - 79
    FAILED = "Failed"                                            # < 70


@dataclass
class StorageInventoryItem:
    object_id: str
    tenant_id: str
    category: StorageArtifactCategory
    storage_path: str
    file_name: str
    mime_type: str
    size_bytes: int
    created_at_iso: str
    sha256_hash: str
    version_id: str
    is_archived: bool = False
    is_protected: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StorageInventoryReport:
    total_objects_discovered: int
    total_size_bytes: int
    objects_by_category: Dict[str, int]
    objects_by_tenant: Dict[str, int]
    tenants_discovered: List[str]
    storage_prefixes_discovered: List[str]
    sample_inventory_items: List[StorageInventoryItem]
    passed: bool


@dataclass
class StorageClassificationReport:
    total_classified_objects: int
    classification_breakdown: Dict[str, Dict[str, Any]]
    unclassified_objects_count: int
    classification_accuracy_percent: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StorageBackupCoverageReport:
    objects_discovered: int
    objects_backed_up: int
    coverage_percent: float
    missing_objects: List[str]
    coverage_by_category: Dict[str, float]
    passed: bool


@dataclass
class DocumentIntegrityReport:
    total_documents_verified: int
    metadata_preservation_score: float
    ocr_artifacts_verified: bool
    ai_extractions_verified: bool
    evidence_packages_verified: bool
    sha256_identity_verified: bool  # Original == Backup == Restored
    digital_signatures_valid: bool
    signature_algorithm: str
    orphan_references_count: int
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StorageVersioningReport:
    versioning_enabled: bool
    total_versions_tracked: int
    version_ordering_verified: bool
    rollback_capability_verified: bool
    deleted_object_recovery_verified: bool
    historical_versions_retained: int
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MetadataConsistencyReport:
    total_database_records_checked: int
    total_storage_objects_checked: int
    matched_references_count: int
    orphaned_storage_files_count: int
    missing_storage_files_count: int
    stale_database_references_count: int
    timestamp_skew_within_tolerance: bool
    consistency_score_percent: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StorageCorruptionItem:
    scenario_id: str
    file_path: str
    injected_fault: StorageCorruptionType
    detected_pre_restore: bool
    detection_method: str
    containment_action: str


@dataclass
class StorageCorruptionReport:
    total_faults_injected: int
    detected_faults_count: int
    prevented_corruptions_count: int
    detection_rate_percent: float
    scenarios: List[StorageCorruptionItem]
    passed: bool


@dataclass
class TenantIsolationReport:
    tenants_tested: List[str]
    cross_tenant_access_blocked: bool
    path_traversal_attempts_blocked: int
    metadata_manipulation_attempts_blocked: int
    enumeration_attempts_blocked: int
    identifier_guessing_attempts_blocked: int
    directory_hierarchy_preserved: bool  # No directory flattening
    isolation_score_percent: float
    passed: bool
    security_events: List[str] = field(default_factory=list)


@dataclass
class StorageEncryptionReport:
    encryption_at_rest_verified: bool  # AES-256-GCM / KMS
    encryption_in_transit_verified: bool  # TLS 1.3
    kms_key_rotation_verified: bool
    worm_object_lock_immutable: bool
    unauthorized_restore_blocked: bool
    encrypted_object_metadata: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CompressionDeduplicationReport:
    supported_compression_formats: List[str]  # gzip, zstd, zip, tar
    compression_ratio: float
    decompression_fidelity_verified: bool
    deduplication_enabled: bool
    deduplication_space_savings_percent: float
    zero_hash_collisions_verified: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StorageBenchmarkDatasetResult:
    dataset_label: str  # 10 MB, 100 MB, 1 GB, 5 GB, 10 GB
    file_size_bytes: int
    backup_duration_seconds: float
    backup_throughput_mb_s: float
    restore_duration_seconds: float
    restore_throughput_mb_s: float
    cpu_utilization_percent: float
    memory_utilization_mb: float
    storage_io_mb_s: float
    integrity_verified: bool
    passed: bool


@dataclass
class StoragePerformanceReport:
    datasets_tested: List[StorageBenchmarkDatasetResult]
    avg_backup_throughput_mb_s: float
    avg_restore_throughput_mb_s: float
    latency_summary: Dict[str, float]  # mean, median, P95, P99
    rto_seconds: float
    rpo_seconds: float
    chaos_failure_scenarios_handled: int
    total_chaos_scenarios: int
    passed: bool


@dataclass
class RestoreSimulationReport:
    clean_environment_isolated: bool
    metadata_rebuilt_successfully: bool
    application_startup_healthy: bool
    document_access_verified: bool
    ocr_validation_passed: bool
    ai_extraction_validation_passed: bool
    evidence_validation_passed: bool
    workflow_execution_passed: bool
    zero_manual_steps: bool
    execution_duration_seconds: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CrossSystemValidationReport:
    database_to_storage_synced: bool
    storage_to_ocr_synced: bool
    ocr_to_ai_results_synced: bool
    ai_to_evidence_synced: bool
    evidence_to_audit_reports_synced: bool
    total_cross_references_checked: int
    broken_reference_count: int
    cross_system_fidelity_percent: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StorageQualityScorecard:
    recoverability_score: float         # Weight 20%
    integrity_score: float              # Weight 20%
    coverage_score: float               # Weight 15%
    cross_system_consistency_score: float # Weight 15%
    security_score: float               # Weight 10%
    performance_score: float            # Weight 10%
    tenant_isolation_score: float       # Weight 5%
    automation_score: float             # Weight 5%
    composite_score: float              # 0 - 100
    certification_tier: StorageCertificationTier
    passed: bool
    execution_duration_ms: float
    audit_metadata: Dict[str, Any] = field(default_factory=dict)
