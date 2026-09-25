"""
Verification Runtime Orchestrator for Enterprise Document Storage (Part 3G.2C).
"""
import time
from typing import Dict, Any, Optional

from app.platform_verification.document_storage_verification.discovery.storage_inventory_engine import (
    StorageInventoryEngine,
)
from app.platform_verification.document_storage_verification.discovery.storage_classification_engine import (
    StorageClassificationEngine,
)
from app.platform_verification.document_storage_verification.integrity.document_integrity_engine import (
    DocumentIntegrityEngine,
)
from app.platform_verification.document_storage_verification.integrity.metadata_consistency_engine import (
    MetadataConsistencyEngine,
)
from app.platform_verification.document_storage_verification.versioning.storage_versioning_engine import (
    StorageVersioningEngine,
)
from app.platform_verification.document_storage_verification.security.tenant_isolation_engine import (
    TenantIsolationEngine,
)
from app.platform_verification.document_storage_verification.security.storage_security_engine import (
    StorageSecurityEngine,
)
from app.platform_verification.document_storage_verification.optimization.compression_dedup_engine import (
    CompressionDedupEngine,
)
from app.platform_verification.document_storage_verification.corruption.storage_corruption_engine import (
    StorageCorruptionEngine,
)
from app.platform_verification.document_storage_verification.recovery.large_file_benchmarking_engine import (
    LargeFileBenchmarkingEngine,
)
from app.platform_verification.document_storage_verification.recovery.restore_simulation_engine import (
    RestoreSimulationEngine,
)
from app.platform_verification.document_storage_verification.recovery.cross_system_validator import (
    CrossSystemValidator,
)
from app.platform_verification.document_storage_verification.scoring.storage_quality_scoring_engine import (
    StorageQualityScoringEngine,
)
from app.platform_verification.document_storage_verification.evidence.storage_evidence_manifest_engine import (
    StorageEvidenceManifestEngine,
)


class StorageBackupVerificationRuntime:
    """
    Master orchestrator for the Enterprise Document Storage Backup & Recovery Verification Framework.
    Runs all 9 verification phases end-to-end and outputs signed certification evidence.
    """

    def __init__(
        self,
        inventory_engine: Optional[StorageInventoryEngine] = None,
        classification_engine: Optional[StorageClassificationEngine] = None,
        integrity_engine: Optional[DocumentIntegrityEngine] = None,
        consistency_engine: Optional[MetadataConsistencyEngine] = None,
        versioning_engine: Optional[StorageVersioningEngine] = None,
        tenant_isolation_engine: Optional[TenantIsolationEngine] = None,
        security_engine: Optional[StorageSecurityEngine] = None,
        compression_engine: Optional[CompressionDedupEngine] = None,
        corruption_engine: Optional[StorageCorruptionEngine] = None,
        performance_engine: Optional[LargeFileBenchmarkingEngine] = None,
        restore_engine: Optional[RestoreSimulationEngine] = None,
        cross_system_validator: Optional[CrossSystemValidator] = None,
        scoring_engine: Optional[StorageQualityScoringEngine] = None,
        evidence_engine: Optional[StorageEvidenceManifestEngine] = None,
    ):
        self.inventory_engine = inventory_engine or StorageInventoryEngine()
        self.classification_engine = classification_engine or StorageClassificationEngine()
        self.integrity_engine = integrity_engine or DocumentIntegrityEngine()
        self.consistency_engine = consistency_engine or MetadataConsistencyEngine()
        self.versioning_engine = versioning_engine or StorageVersioningEngine()
        self.tenant_isolation_engine = tenant_isolation_engine or TenantIsolationEngine()
        self.security_engine = security_engine or StorageSecurityEngine()
        self.compression_engine = compression_engine or CompressionDedupEngine()
        self.corruption_engine = corruption_engine or StorageCorruptionEngine()
        self.performance_engine = performance_engine or LargeFileBenchmarkingEngine()
        self.restore_engine = restore_engine or RestoreSimulationEngine()
        self.cross_system_validator = cross_system_validator or CrossSystemValidator()
        self.scoring_engine = scoring_engine or StorageQualityScoringEngine()
        self.evidence_engine = evidence_engine or StorageEvidenceManifestEngine()

    def execute_full_verification(
        self, output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end document storage verification suite across all 9 phases.
        """
        start_time = time.perf_counter()

        # Phase 1: Storage Discovery & Inventory
        inventory_report = self.inventory_engine.discover_storage_inventory()
        coverage_report = self.inventory_engine.verify_backup_coverage(inventory_report)

        # Phase 2: Classification Taxonomy
        classification_report = self.classification_engine.classify_storage_objects(inventory_report)

        # Phase 3: Cryptographic Integrity & Metadata Consistency
        integrity_report = self.integrity_engine.verify_document_integrity()
        consistency_report = self.consistency_engine.verify_metadata_consistency()

        # Phase 4: Storage Versioning & Retention
        versioning_report = self.versioning_engine.verify_storage_versioning()

        # Phase 5: Tenant Isolation & Cryptographic Security
        tenant_isolation_report = self.tenant_isolation_engine.verify_tenant_isolation()
        security_report = self.security_engine.verify_storage_security()

        # Phase 6: Optimization & Chaos Fault Injection
        compression_report = self.compression_engine.verify_compression_and_deduplication()
        corruption_report = self.corruption_engine.inject_and_detect_corruption()

        # Phase 7: Benchmarking, Clean-Room Restore & Cross-System Reference Validation
        performance_report = self.performance_engine.benchmark_large_files_and_chaos()
        restore_report = self.restore_engine.execute_restore_simulation()
        cross_system_report = self.cross_system_validator.validate_cross_system_references()

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        # Phase 8: Quality Scoring & Enterprise Tier Certification
        # Derive scores from each engine report
        recoverability_score = 100.0 if restore_report.passed and versioning_report.passed else 75.0
        integrity_score = (
            100.0 if integrity_report.passed and corruption_report.detection_rate_percent == 100.0 else 70.0
        )
        coverage_score = coverage_report.coverage_percent
        cross_system_score = cross_system_report.cross_system_fidelity_percent
        security_score = 100.0 if security_report.passed else 60.0
        performance_score = 100.0 if performance_report.passed else 70.0
        tenant_isolation_score = tenant_isolation_report.isolation_score_percent
        automation_score = 100.0 if restore_report.zero_manual_steps else 50.0

        scorecard = self.scoring_engine.compute_quality_scorecard(
            recoverability_score=recoverability_score,
            integrity_score=integrity_score,
            coverage_score=coverage_score,
            cross_system_consistency_score=cross_system_score,
            security_score=security_score,
            performance_score=performance_score,
            tenant_isolation_score=tenant_isolation_score,
            automation_score=automation_score,
            execution_duration_ms=elapsed_ms,
        )

        verification_data = {
            "storage_inventory": inventory_report,
            "backup_coverage": coverage_report,
            "storage_classification": classification_report,
            "document_integrity": integrity_report,
            "storage_versioning": versioning_report,
            "metadata_consistency": consistency_report,
            "storage_corruption": corruption_report,
            "tenant_isolation": tenant_isolation_report,
            "storage_encryption": security_report,
            "compression_dedup": compression_report,
            "storage_performance": performance_report,
            "restore_simulation": restore_report,
            "cross_system_validation": cross_system_report,
            "storage_quality_scorecard": scorecard,
        }

        # Phase 9: Evidence Serialization & Manifest Export
        manifest_paths = self.evidence_engine.export_all_evidence_artifacts(
            verification_data, output_dir=output_dir
        )

        verification_data["exported_manifest_paths"] = manifest_paths
        verification_data["passed"] = scorecard.passed

        return verification_data
