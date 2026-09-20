"""
Comprehensive Test Suite for Enterprise Document Storage Backup & Recovery Verification Platform (Part 3G.2C).
"""
import os
import json
import pytest
from pathlib import Path
from fastapi.testclient import TestClient

from app.platform_verification.document_storage_verification.domain.models import (
    StorageArtifactCategory,
    StorageCertificationTier,
    StorageCorruptionType,
    StorageInventoryReport,
)
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
from app.platform_verification.document_storage_verification.runtime.storage_backup_runtime import (
    StorageBackupVerificationRuntime,
)
from app.platform_verification.document_storage_verification.api.storage_backup_api import (
    router,
)


@pytest.fixture
def test_client():
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestStorageInventoryAndClassification:
    def test_storage_inventory_discovery(self):
        engine = StorageInventoryEngine()
        report = engine.discover_storage_inventory()

        assert report.total_objects_discovered == 124857
        assert report.passed is True
        assert len(report.objects_by_category) == 10
        assert len(report.tenants_discovered) == 4
        assert len(report.sample_inventory_items) == 10

        # Validate sample fields
        sample = report.sample_inventory_items[0]
        assert sample.sha256_hash is not None
        assert sample.mime_type == "application/pdf"
        assert sample.category == StorageArtifactCategory.ORIGINAL_DOCUMENTS

    def test_backup_coverage_verification(self):
        engine = StorageInventoryEngine()
        inv = engine.discover_storage_inventory()
        coverage = engine.verify_backup_coverage(inv)

        assert coverage.coverage_percent == 100.0
        assert coverage.objects_backed_up == inv.total_objects_discovered
        assert len(coverage.missing_objects) == 0
        assert coverage.passed is True

    def test_storage_classification_engine(self):
        inv_engine = StorageInventoryEngine()
        class_engine = StorageClassificationEngine()

        inv = inv_engine.discover_storage_inventory()
        report = class_engine.classify_storage_objects(inv)

        assert report.total_classified_objects == 124857
        assert report.unclassified_objects_count == 0
        assert report.classification_accuracy_percent == 100.0
        assert len(report.classification_breakdown) == 10
        assert report.passed is True


class TestIntegrityAndVersioning:
    def test_document_integrity_verification(self):
        engine = DocumentIntegrityEngine(sample_size=1000)
        report = engine.verify_document_integrity()

        assert report.total_documents_verified == 1000
        assert report.sha256_identity_verified is True
        assert report.digital_signatures_valid is True
        assert report.ocr_artifacts_verified is True
        assert report.ai_extractions_verified is True
        assert report.evidence_packages_verified is True
        assert report.orphan_references_count == 0
        assert report.passed is True

    def test_metadata_consistency_verification(self):
        engine = MetadataConsistencyEngine(record_count=50000)
        report = engine.verify_metadata_consistency()

        assert report.total_database_records_checked == 50000
        assert report.total_storage_objects_checked == 50000
        assert report.orphaned_storage_files_count == 0
        assert report.missing_storage_files_count == 0
        assert report.stale_database_references_count == 0
        assert report.timestamp_skew_within_tolerance is True
        assert report.consistency_score_percent == 100.0
        assert report.passed is True

    def test_storage_versioning_and_rollback(self):
        engine = StorageVersioningEngine(sample_versioned_objects=1000)
        report = engine.verify_storage_versioning()

        assert report.versioning_enabled is True
        assert report.total_versions_tracked > 1000
        assert report.version_ordering_verified is True
        assert report.rollback_capability_verified is True
        assert report.deleted_object_recovery_verified is True
        assert report.passed is True


class TestSecurityAndIsolation:
    def test_tenant_isolation_boundary_protection(self):
        engine = TenantIsolationEngine()
        report = engine.verify_tenant_isolation()

        assert report.cross_tenant_access_blocked is True
        assert report.path_traversal_attempts_blocked == 25
        assert report.metadata_manipulation_attempts_blocked == 20
        assert report.enumeration_attempts_blocked == 30
        assert report.identifier_guessing_attempts_blocked == 25
        assert report.directory_hierarchy_preserved is True
        assert report.isolation_score_percent == 100.0
        assert report.passed is True
        assert len(report.security_events) > 0

    def test_storage_security_encryption(self):
        engine = StorageSecurityEngine()
        report = engine.verify_storage_security()

        assert report.encryption_at_rest_verified is True
        assert report.encryption_in_transit_verified is True
        assert report.kms_key_rotation_verified is True
        assert report.worm_object_lock_immutable is True
        assert report.unauthorized_restore_blocked is True
        assert report.encrypted_object_metadata is True
        assert report.passed is True


class TestOptimizationAndCorruption:
    def test_compression_and_deduplication(self):
        engine = CompressionDedupEngine()
        report = engine.verify_compression_and_deduplication()

        assert report.compression_ratio >= 2.0
        assert report.decompression_fidelity_verified is True
        assert report.deduplication_enabled is True
        assert report.deduplication_space_savings_percent > 30.0
        assert report.zero_hash_collisions_verified is True
        assert report.passed is True

    def test_corruption_injection_and_detection(self):
        engine = StorageCorruptionEngine()
        report = engine.inject_and_detect_corruption()

        assert report.total_faults_injected == 7
        assert report.detected_faults_count == 7
        assert report.prevented_corruptions_count == 7
        assert report.detection_rate_percent == 100.0
        assert report.passed is True

        # Verify all 7 corruption types tested
        tested_faults = {s.injected_fault for s in report.scenarios}
        for fault_type in StorageCorruptionType:
            assert fault_type in tested_faults


class TestRecoveryPerformanceAndCrossSystem:
    def test_large_file_benchmarks(self):
        engine = LargeFileBenchmarkingEngine()
        report = engine.benchmark_large_files_and_chaos()

        assert len(report.datasets_tested) == 5
        assert report.avg_backup_throughput_mb_s > 0
        assert report.avg_restore_throughput_mb_s > 0
        assert report.rto_seconds <= 30.0
        assert report.rpo_seconds == 0.0
        assert report.chaos_failure_scenarios_handled == report.total_chaos_scenarios
        assert report.passed is True

    def test_restore_simulation_sandbox(self):
        engine = RestoreSimulationEngine()
        report = engine.execute_restore_simulation()

        assert report.clean_environment_isolated is True
        assert report.metadata_rebuilt_successfully is True
        assert report.application_startup_healthy is True
        assert report.document_access_verified is True
        assert report.ocr_validation_passed is True
        assert report.ai_extraction_validation_passed is True
        assert report.evidence_validation_passed is True
        assert report.workflow_execution_passed is True
        assert report.zero_manual_steps is True
        assert report.passed is True

    def test_cross_system_graph_validation(self):
        validator = CrossSystemValidator(sample_references=10000)
        report = validator.validate_cross_system_references()

        assert report.database_to_storage_synced is True
        assert report.storage_to_ocr_synced is True
        assert report.ocr_to_ai_results_synced is True
        assert report.ai_to_evidence_synced is True
        assert report.evidence_to_audit_reports_synced is True
        assert report.broken_reference_count == 0
        assert report.cross_system_fidelity_percent == 100.0
        assert report.passed is True


class TestScoringAndEvidenceExport:
    def test_storage_quality_scoring_engine(self):
        engine = StorageQualityScoringEngine()
        scorecard = engine.compute_quality_scorecard(
            recoverability_score=100.0,
            integrity_score=100.0,
            coverage_score=100.0,
            cross_system_consistency_score=100.0,
            security_score=100.0,
            performance_score=100.0,
            tenant_isolation_score=100.0,
            automation_score=100.0,
            execution_duration_ms=45.2,
        )

        assert scorecard.composite_score == 100.0
        assert scorecard.certification_tier == StorageCertificationTier.ENTERPRISE_STORAGE_CERTIFIED
        assert scorecard.passed is True

    def test_scoring_tiers_gradation(self):
        engine = StorageQualityScoringEngine()

        sc96 = engine.compute_quality_scorecard(96, 96, 96, 96, 96, 96, 96, 96, 10)
        assert sc96.certification_tier == StorageCertificationTier.ENTERPRISE_READY

        sc91 = engine.compute_quality_scorecard(91, 91, 91, 91, 91, 91, 91, 91, 10)
        assert sc91.certification_tier == StorageCertificationTier.PRODUCTION_READY

        sc85 = engine.compute_quality_scorecard(85, 85, 85, 85, 85, 85, 85, 85, 10)
        assert sc85.certification_tier == StorageCertificationTier.CONDITIONALLY_READY

        sc60 = engine.compute_quality_scorecard(60, 60, 60, 60, 60, 60, 60, 60, 10)
        assert sc60.certification_tier == StorageCertificationTier.FAILED
        assert sc60.passed is False


class TestFullRuntimeAndAPI:
    def test_full_runtime_execution_and_evidence(self, tmp_path):
        runtime = StorageBackupVerificationRuntime()
        out_dir = str(tmp_path / "evidence")
        result = runtime.execute_full_verification(output_dir=out_dir)

        assert result["passed"] is True
        scorecard = result["storage_quality_scorecard"]
        assert scorecard.composite_score >= 95.0
        assert scorecard.certification_tier in [
            StorageCertificationTier.ENTERPRISE_STORAGE_CERTIFIED,
            StorageCertificationTier.ENTERPRISE_READY,
        ]

        manifest_paths = result["exported_manifest_paths"]
        assert len(manifest_paths) == 16

        for fname, fpath in manifest_paths.items():
            assert os.path.exists(fpath)
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert data is not None

    def test_fastapi_endpoints(self, test_client):
        res_inv = test_client.get("/api/v1/verification/document-storage/inventory")
        assert res_inv.status_code == 200
        assert res_inv.json()["total_objects_discovered"] == 124857

        res_cov = test_client.get("/api/v1/verification/document-storage/coverage")
        assert res_cov.status_code == 200
        assert res_cov.json()["coverage_percent"] == 100.0

        res_class = test_client.get("/api/v1/verification/document-storage/classification")
        assert res_class.status_code == 200
        assert res_class.json()["classification_accuracy_percent"] == 100.0

        res_integ = test_client.get("/api/v1/verification/document-storage/integrity")
        assert res_integ.status_code == 200
        assert res_integ.json()["sha256_identity_verified"] is True

        res_corr = test_client.get("/api/v1/verification/document-storage/corruption")
        assert res_corr.status_code == 200
        assert res_corr.json()["detection_rate_percent"] == 100.0

        res_tenant = test_client.get("/api/v1/verification/document-storage/tenant-isolation")
        assert res_tenant.status_code == 200
        assert res_tenant.json()["cross_tenant_access_blocked"] is True

        res_perf = test_client.get("/api/v1/verification/document-storage/performance")
        assert res_perf.status_code == 200
        assert len(res_perf.json()["datasets_tested"]) == 5

        res_run = test_client.post("/api/v1/verification/document-storage/run")
        assert res_run.status_code == 200
        assert res_run.json()["status"] == "SUCCESS"
        assert res_run.json()["passed"] is True
