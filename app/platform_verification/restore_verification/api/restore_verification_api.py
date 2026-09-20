"""
REST API Router for Enterprise Automated Restore Verification System (Part 3G.2E).
Exposes disaster recovery orchestration, clean-room simulation, and audit certification endpoints.
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Query

from app.platform_verification.restore_verification.runtime.restore_verification_runtime import (
    RestoreVerificationRuntime,
)
from app.platform_verification.restore_verification.evidence_generator.restore_evidence_manifest_engine import (
    _serialize_obj,
)

router = APIRouter(
    prefix="/api/v1/verification/restore",
    tags=["Enterprise Automated Restore Verification System (Part 3G.2E)"],
)

runtime_instance = RestoreVerificationRuntime()


@router.post("/run", response_model=Dict[str, Any])
def run_full_restore_verification(
    output_dir: str = Query(default="evidence/restore_verification", description="Evidence export directory")
) -> Dict[str, Any]:
    """Triggers the full enterprise automated restore verification pipeline."""
    try:
        result = runtime_instance.execute_full_restore_verification(output_dir=output_dir)
        scorecard = result.get("scorecard")
        return {
            "status": "SUCCESS",
            "composite_score": scorecard.composite_score if scorecard else 0.0,
            "certification_tier": scorecard.certification_tier.value if scorecard else "UNKNOWN",
            "passed": result.get("passed", False),
            "manifest_paths": result.get("exported_manifest_paths", {}),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Restore verification failed: {str(e)}")


@router.get("/catalog")
def get_backup_catalog() -> Dict[str, Any]:
    """Returns the comprehensive multi-source recovery points catalog."""
    report = runtime_instance.backup_discovery.discover_and_catalog_backups()
    return _serialize_obj(report)


@router.get("/environment")
def get_recovery_environment_status() -> Dict[str, Any]:
    """Returns ephemeral clean-room sandbox provisioning and resource audit report."""
    report = runtime_instance.env_manager.provision_recovery_environment()
    return _serialize_obj(report)


@router.get("/database")
def get_database_restore_validation() -> Dict[str, Any]:
    """Returns PostgreSQL schema, row count (10k docs), and consistency audit report."""
    report = runtime_instance.db_validator.validate_database_restore()
    return _serialize_obj(report)


@router.get("/documents")
def get_document_restore_validation() -> Dict[str, Any]:
    """Returns document artifact SHA-256 hash equality and large-file validation report."""
    report = runtime_instance.doc_validator.validate_document_restore()
    return _serialize_obj(report)


@router.get("/configuration-secrets")
def get_config_and_secret_restore_validation() -> Dict[str, Any]:
    """Returns configuration hash comparison and zero-leakage indirect secret validation."""
    cfg, sec = runtime_instance.config_secret_validator.validate_configuration_and_secrets()
    return {
        "configuration": _serialize_obj(cfg),
        "secrets": _serialize_obj(sec),
    }


@router.get("/services")
def get_service_startup_status() -> Dict[str, Any]:
    """Returns /health, /ready, and /live probe evaluations across all 7 platform services."""
    report = runtime_instance.health_validator.validate_service_health_and_readiness()
    return _serialize_obj(report)


@router.get("/functional-tests")
def get_functional_recovery_tests() -> Dict[str, Any]:
    """Returns synthetic document ingest, agent lifecycle, and auth RBAC execution report."""
    report = runtime_instance.workflow_runner.execute_synthetic_business_workflows()
    return _serialize_obj(report)


@router.get("/integrity")
def get_integrity_checksum_report() -> Dict[str, Any]:
    """Returns triple checksum comparison across backup, restored, and runtime graphs."""
    report = runtime_instance.integrity_checker.verify_triple_checksum_integrity()
    return _serialize_obj(report)


@router.get("/rto-rpo")
def get_rto_rpo_performance() -> Dict[str, Any]:
    """Returns RTO and RPO measured metrics against enterprise SLAs."""
    report = runtime_instance.performance_engine.measure_rto_rpo_performance()
    return _serialize_obj(report)


@router.get("/failures")
def get_failure_simulation_report() -> Dict[str, Any]:
    """Returns disaster recovery failure injection, rollback, and containment report."""
    report = runtime_instance.failure_simulator.simulate_failure_scenarios_and_rollbacks()
    return _serialize_obj(report)


@router.get("/drills")
def get_continuous_drills_config() -> Dict[str, Any]:
    """Returns recurring automated disaster recovery drill configuration and schedule."""
    return runtime_instance.scheduler.configure_recovery_drills()


@router.get("/scorecard")
def get_restore_quality_scorecard() -> Dict[str, Any]:
    """Executes full verification and returns the weighted Disaster Recovery Quality Scorecard."""
    result = runtime_instance.execute_full_restore_verification()
    return _serialize_obj(result["scorecard"])
