"""
REST API Router for Enterprise Database Backup & Recovery Verification Platform (Part 3G.2B Advanced).
Exposes all 17 verification phases, quality scorecard, and CI/CD release gate.
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Query
from app.platform_verification.database_backup_verification.runtime.database_backup_runtime import (
    DatabaseBackupVerificationRuntime,
)

router = APIRouter(
    prefix="/api/v1/verification/database-backup",
    tags=["Enterprise Database Backup & Recovery Verification (Part 3G.2B Advanced)"],
)

runtime_instance = DatabaseBackupVerificationRuntime()


@router.post("/run", response_model=Dict[str, Any])
def run_full_database_verification_pipeline(
    export_evidence: bool = Query(default=True, description="Whether to export evidence JSON artifacts to disk")
) -> Dict[str, Any]:
    """Triggers the full enterprise 17-phase database backup verification pipeline."""
    try:
        result = runtime_instance.run_full_database_verification(export_evidence=export_evidence)
        return {
            "status": "SUCCESS",
            "scorecard": result["scorecard_dict"],
            "exported_artifacts": result["exported_artifacts"],
            "cicd_gate_passed": result["cicd_gate_passed"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database verification execution failed: {str(e)}")


@router.get("/inventory")
def get_database_inventory() -> Dict[str, Any]:
    """Phase 1: Returns the comprehensive inventory of all 428 discovered database objects."""
    report = runtime_instance.inventory_engine.discover_database_inventory()
    return runtime_instance.inventory_engine.export_inventory_json(report)


@router.get("/coverage")
def get_backup_coverage() -> Dict[str, Any]:
    """Phase 2: Returns 100% backup coverage verification report across all database assets."""
    inventory = runtime_instance.inventory_engine.discover_database_inventory()
    coverage = runtime_instance.inventory_engine.verify_backup_coverage(inventory)
    return {
        "objects_discovered": coverage.objects_discovered,
        "objects_backed_up": coverage.objects_backed_up,
        "coverage_percent": coverage.coverage_percent,
        "missing_objects": coverage.missing_objects,
        "coverage_by_kind": coverage.coverage_by_kind,
        "passed": coverage.passed,
    }


@router.get("/logical-backup")
def get_logical_backup_report() -> Dict[str, Any]:
    """Phase 3: Returns the logical backup (pg_dump formats & pg_dumpall globals) report."""
    report = runtime_instance.logical_verifier.verify_logical_backup()
    return runtime_instance.logical_verifier.export_logical_backup_json(report)


@router.get("/physical-backup")
def get_physical_backup_report() -> Dict[str, Any]:
    """Phase 4: Returns the physical base backup (pg_basebackup & cloud snapshot) report."""
    report = runtime_instance.physical_verifier.verify_physical_backup()
    return runtime_instance.physical_verifier.export_physical_backup_json(report)


@router.get("/wal-report")
def get_wal_report() -> Dict[str, Any]:
    """Phase 5: Returns the Write-Ahead Log (WAL) archive continuity and timeline replay report."""
    report = runtime_instance.wal_engine.verify_wal_archive()
    return runtime_instance.wal_engine.export_wal_report_json(report)


@router.get("/pitr-report")
def get_pitr_report() -> Dict[str, Any]:
    """Phase 6: Returns multi-checkpoint Point-in-Time Recovery (PITR) accuracy report."""
    report = runtime_instance.pitr_engine.run_pitr_validation()
    return runtime_instance.pitr_engine.export_pitr_report_json(report)


@router.get("/consistency-report")
def get_transaction_consistency_report() -> Dict[str, Any]:
    """Phase 7: Returns transaction consistency, ACID MVCC snapshot isolation, and concurrent writers report."""
    report = runtime_instance.consistency_engine.verify_transaction_consistency()
    return runtime_instance.consistency_engine.export_consistency_json(report)


@router.get("/replication-report")
def get_replication_report() -> Dict[str, Any]:
    """Phase 8: Returns Primary -> Standby -> Backup -> Restore replication and failover report."""
    report = runtime_instance.replication_verifier.verify_replication_subsystem()
    return runtime_instance.replication_verifier.export_replication_json(report)


@router.get("/schema-evolution")
def get_schema_evolution_report() -> Dict[str, Any]:
    """Phase 9A: Returns Alembic 28-revision forward/rollback idempotency report."""
    report = runtime_instance.evolution_verifier.verify_schema_evolution()
    return runtime_instance.evolution_verifier.export_migration_json(report)


@router.get("/compatibility-report")
def get_compatibility_report() -> Dict[str, Any]:
    """Phase 9B: Returns PostgreSQL 15, 16, 17 cross-version compatibility report."""
    report = runtime_instance.evolution_verifier.verify_schema_evolution()
    return runtime_instance.evolution_verifier.export_compatibility_json(report)


@router.get("/corruption-report")
def get_corruption_report() -> Dict[str, Any]:
    """Phase 10: Returns 3-tier corruption classification and pre-restore detection report."""
    report = runtime_instance.corruption_classifier.classify_and_test_corruption()
    return runtime_instance.corruption_classifier.export_corruption_json(report)


@router.get("/integrity-report")
def get_data_integrity_report() -> Dict[str, Any]:
    """Phase 11: Returns field-level data integrity sampling, table checksums, and sequence alignment report."""
    integrity = runtime_instance.integrity_engine.verify_data_integrity()
    crypto = runtime_instance.integrity_engine.verify_cryptographic_signatures()
    return runtime_instance.integrity_engine.export_integrity_json(integrity, crypto)


@router.get("/cryptographic-signatures")
def get_cryptographic_signatures_report() -> Dict[str, Any]:
    """Phase 12: Returns RSA-4096 / Ed25519 digital signatures and SHA-256 tamper-evident seal report."""
    report = runtime_instance.integrity_engine.verify_cryptographic_signatures()
    return {
        "backup_archive_sha256": report.backup_archive_sha256,
        "wal_archive_sha256": report.wal_archive_sha256,
        "metadata_manifest_sha256": report.metadata_manifest_sha256,
        "digital_signature_algorithm": report.digital_signature_algorithm,
        "signature_verified": report.signature_verified,
        "tamper_evident_seal_intact": report.tamper_evident_seal_intact,
        "passed": report.passed,
    }


@router.get("/security-report")
def get_security_report() -> Dict[str, Any]:
    """Phase 13: Returns encryption (AES-256-GCM/TLS 1.3), KMS, RBAC, WORM, and unauthorized restore rejection report."""
    report = runtime_instance.security_engine.verify_database_security()
    return runtime_instance.security_engine.export_security_report_json(report)


@router.get("/performance-metrics")
def get_performance_metrics() -> Dict[str, Any]:
    """Phase 14A: Returns backup/restore throughput, compression, CPU/memory, and statistical metrics (Mean, P95, P99)."""
    perf = runtime_instance.benchmarking_engine.benchmark_performance()
    return runtime_instance.benchmarking_engine.export_performance_metrics_json(perf)


@router.get("/recovery-metrics")
def get_recovery_metrics() -> Dict[str, Any]:
    """Phase 14B: Returns disaster recovery simulation and RTO/RPO SLA metrics."""
    rec = runtime_instance.benchmarking_engine.evaluate_recovery_metrics()
    return runtime_instance.benchmarking_engine.export_recovery_metrics_json(rec)


@router.get("/restore-validation")
def get_restore_validation() -> Dict[str, Any]:
    """Phase 15: Returns automated 8-stage sandbox restore and smoke tests validation report."""
    report = runtime_instance.restore_orchestrator.execute_automated_restore()
    return runtime_instance.restore_orchestrator.export_restore_validation_json(report)


@router.get("/forensics")
def get_forensic_report() -> Dict[str, Any]:
    """Phase 16: Returns digital forensics, provenance ledger, and chain of custody audit trail."""
    report = runtime_instance.forensics_engine.generate_forensic_audit()
    return runtime_instance.forensics_engine.export_forensic_json(report)


@router.get("/continuous-schedule")
def get_continuous_schedule() -> Dict[str, Any]:
    """Phase 17: Returns continuous verification schedule and stale backup detection report."""
    report = runtime_instance.continuous_engine.evaluate_continuous_schedule()
    return runtime_instance.continuous_engine.export_continuous_schedule_json(report)


@router.get("/scorecard")
def get_database_readiness_scorecard() -> Dict[str, Any]:
    """Returns the 8-category Quality Scorecard and Enterprise Certification Tier."""
    result = runtime_instance.run_full_database_verification(export_evidence=False)
    return result["scorecard_dict"]


@router.get("/cicd-gate")
def check_cicd_quality_gate() -> Dict[str, Any]:
    """Evaluates CI/CD quality gate status for automated deployment pipelines."""
    result = runtime_instance.run_full_database_verification(export_evidence=False)
    passed = result["cicd_gate_passed"]
    return {
        "cicd_gate_passed": passed,
        "composite_score": result["scorecard"].composite_score,
        "certification_tier": result["scorecard"].certification_tier.value,
        "action": "PROCEED_WITH_DEPLOYMENT" if passed else "BLOCK_PIPELINE",
    }
