"""
Abstract Interfaces for Enterprise Document Storage Backup & Recovery Verification (Part 3G.2C).
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

from app.platform_verification.document_storage_verification.domain.models import (
    StorageInventoryReport,
    StorageClassificationReport,
    StorageBackupCoverageReport,
    DocumentIntegrityReport,
    StorageVersioningReport,
    MetadataConsistencyReport,
    StorageCorruptionReport,
    TenantIsolationReport,
    StorageEncryptionReport,
    CompressionDeduplicationReport,
    StoragePerformanceReport,
    RestoreSimulationReport,
    CrossSystemValidationReport,
    StorageQualityScorecard,
)


class IStorageInventoryEngine(ABC):
    @abstractmethod
    def discover_storage_inventory(self) -> StorageInventoryReport:
        pass

    @abstractmethod
    def verify_backup_coverage(
        self, inventory: StorageInventoryReport
    ) -> StorageBackupCoverageReport:
        pass


class IStorageClassificationEngine(ABC):
    @abstractmethod
    def classify_storage_objects(
        self, inventory: StorageInventoryReport
    ) -> StorageClassificationReport:
        pass


class IDocumentIntegrityEngine(ABC):
    @abstractmethod
    def verify_document_integrity(self) -> DocumentIntegrityReport:
        pass


class IStorageVersioningEngine(ABC):
    @abstractmethod
    def verify_storage_versioning(self) -> StorageVersioningReport:
        pass


class IMetadataConsistencyEngine(ABC):
    @abstractmethod
    def verify_metadata_consistency(self) -> MetadataConsistencyReport:
        pass


class IStorageCorruptionEngine(ABC):
    @abstractmethod
    def inject_and_detect_corruption(self) -> StorageCorruptionReport:
        pass


class ITenantIsolationEngine(ABC):
    @abstractmethod
    def verify_tenant_isolation(self) -> TenantIsolationReport:
        pass


class IStorageSecurityEngine(ABC):
    @abstractmethod
    def verify_storage_security(self) -> StorageEncryptionReport:
        pass


class ICompressionDedupEngine(ABC):
    @abstractmethod
    def verify_compression_and_deduplication(
        self,
    ) -> CompressionDeduplicationReport:
        pass


class IStoragePerformanceEngine(ABC):
    @abstractmethod
    def benchmark_large_files_and_chaos(self) -> StoragePerformanceReport:
        pass


class IRestoreSimulationEngine(ABC):
    @abstractmethod
    def execute_restore_simulation(self) -> RestoreSimulationReport:
        pass


class ICrossSystemValidator(ABC):
    @abstractmethod
    def validate_cross_system_references(self) -> CrossSystemValidationReport:
        pass


class IStorageQualityScoringEngine(ABC):
    @abstractmethod
    def compute_quality_scorecard(
        self,
        recoverability_score: float,
        integrity_score: float,
        coverage_score: float,
        cross_system_consistency_score: float,
        security_score: float,
        performance_score: float,
        tenant_isolation_score: float,
        automation_score: float,
        execution_duration_ms: float,
    ) -> StorageQualityScorecard:
        pass


class IStorageEvidenceManifestEngine(ABC):
    @abstractmethod
    def export_all_evidence_artifacts(
        self,
        verification_data: Dict[str, Any],
        output_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        pass
