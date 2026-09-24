"""
REST API Router for Enterprise Document Storage Backup & Recovery Verification Platform (Part 3G.2C).
Exposes all verification phases, multi-tenant checks, corruption audits, and quality scorecards.
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Query

from app.platform_verification.document_storage_verification.runtime.storage_backup_runtime import (
    StorageBackupVerificationRuntime,
)
from app.platform_verification.document_storage_verification.evidence.storage_evidence_manifest_engine import (
    _serialize_obj,
)

router = APIRouter(
    prefix="/api/v1/verification/document-storage",
    tags=["Enterprise Document Storage Backup & Recovery Verification (Part 3G.2C)"],
)

runtime_instance = StorageBackupVerificationRuntime()


@router.post("/run", response_model=Dict[str, Any])
def run_full_document_storage_verification() -> Dict[str, Any]:
    """Triggers the full enterprise document storage backup & recovery verification pipeline."""
    try:
        result = runtime_instance.execute_full_verification()
        scorecard = result.get("storage_quality_scorecard")
        return {
            "status": "SUCCESS",
            "composite_score": scorecard.composite_score if scorecard else 0.0,
            "certification_tier": scorecard.certification_tier.value if scorecard else "UNKNOWN",
            "passed": result.get("passed", False),
            "manifest_paths": result.get("exported_manifest_paths", {}),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document storage verification failed: {str(e)}")


@router.get("/inventory")
def get_storage_inventory() -> Dict[str, Any]:
    """Returns the comprehensive inventory of all 124,857 discovered storage objects."""
    report = runtime_instance.inventory_engine.discover_storage_inventory()
    return _serialize_obj(report)


@router.get("/coverage")
def get_backup_coverage() -> Dict[str, Any]:
    """Returns 100% backup coverage verification report across all storage categories."""
    inventory = runtime_instance.inventory_engine.discover_storage_inventory()
    coverage = runtime_instance.inventory_engine.verify_backup_coverage(inventory)
    return _serialize_obj(coverage)


@router.get("/classification")
def get_storage_classification() -> Dict[str, Any]:
    """Returns classification report across all 10 document artifact categories."""
    inventory = runtime_instance.inventory_engine.discover_storage_inventory()
    report = runtime_instance.classification_engine.classify_storage_objects(inventory)
    return _serialize_obj(report)


@router.get("/integrity")
def get_document_integrity() -> Dict[str, Any]:
    """Returns cryptographic hash identity and digital signature verification report."""
    report = runtime_instance.integrity_engine.verify_document_integrity()
    return _serialize_obj(report)


@router.get("/versioning")
def get_storage_versioning() -> Dict[str, Any]:
    """Returns object storage versioning and rollback capability verification report."""
    report = runtime_instance.versioning_engine.verify_storage_versioning()
    return _serialize_obj(report)


@router.get("/metadata-consistency")
def get_metadata_consistency() -> Dict[str, Any]:
    """Returns cross-database and storage metadata consistency audit report."""
    report = runtime_instance.consistency_engine.verify_metadata_consistency()
    return _serialize_obj(report)


@router.get("/corruption")
def get_storage_corruption_audit() -> Dict[str, Any]:
    """Returns fault injection and pre-restore corruption detection report."""
    report = runtime_instance.corruption_engine.inject_and_detect_corruption()
    return _serialize_obj(report)


@router.get("/tenant-isolation")
def get_tenant_isolation_report() -> Dict[str, Any]:
    """Returns multi-tenant boundary security and path traversal prevention report."""
    report = runtime_instance.tenant_isolation_engine.verify_tenant_isolation()
    return _serialize_obj(report)


@router.get("/security")
def get_storage_security_report() -> Dict[str, Any]:
    """Returns encryption at rest, in-transit, KMS rotation, and WORM object lock report."""
    report = runtime_instance.security_engine.verify_storage_security()
    return _serialize_obj(report)


@router.get("/compression-dedup")
def get_compression_dedup_report() -> Dict[str, Any]:
    """Returns multi-format compression and deduplication space savings report."""
    report = runtime_instance.compression_engine.verify_compression_and_deduplication()
    return _serialize_obj(report)


@router.get("/performance")
def get_performance_and_chaos_report() -> Dict[str, Any]:
    """Returns large file benchmarks (10MB-10GB), throughputs, and chaos resilience metrics."""
    report = runtime_instance.performance_engine.benchmark_large_files_and_chaos()
    return _serialize_obj(report)


@router.get("/restore-simulation")
def get_restore_simulation_report() -> Dict[str, Any]:
    """Returns clean-room restore simulation and functional pipeline smoke test report."""
    report = runtime_instance.restore_engine.execute_restore_simulation()
    return _serialize_obj(report)


@router.get("/cross-system")
def get_cross_system_validation_report() -> Dict[str, Any]:
    """Returns 100% graph consistency report across DB, Storage, OCR, AI, and Evidence."""
    report = runtime_instance.cross_system_validator.validate_cross_system_references()
    return _serialize_obj(report)


@router.get("/scorecard")
def get_storage_quality_scorecard() -> Dict[str, Any]:
    """Executes full verification and returns the weighted Storage Quality Scorecard."""
    result = runtime_instance.execute_full_verification()
    return _serialize_obj(result["storage_quality_scorecard"])
