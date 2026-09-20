"""
REST API Router for Enterprise Configuration & Secret Backup Verification Platform (Part 3G.2D).
Exposes all configuration audit phases, secret recovery checks, cryptographic validations, and quality scorecards.
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Query

from app.platform_verification.configuration_backup_verification.runtime.configuration_backup_runtime import (
    ConfigurationBackupVerificationRuntime,
)
from app.platform_verification.configuration_backup_verification.evidence.configuration_evidence_manifest_engine import (
    _serialize_obj,
)

router = APIRouter(
    prefix="/api/v1/verification/configuration-backup",
    tags=["Enterprise Configuration, Secret & Cryptographic Backup Verification (Part 3G.2D)"],
)

runtime_instance = ConfigurationBackupVerificationRuntime()


@router.post("/run", response_model=Dict[str, Any])
def run_full_configuration_verification(
    output_dir: str = Query(default="evidence/configuration_backup_verification", description="Evidence export directory")
) -> Dict[str, Any]:
    """Triggers the full enterprise configuration & secret backup verification pipeline."""
    try:
        result = runtime_instance.execute_full_verification(output_dir=output_dir)
        scorecard = result.get("scorecard")
        return {
            "status": "SUCCESS",
            "composite_score": scorecard.composite_score if scorecard else 0.0,
            "certification_tier": scorecard.certification_tier.value if scorecard else "UNKNOWN",
            "passed": result.get("passed", False),
            "manifest_paths": result.get("exported_manifest_paths", {}),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Configuration verification failed: {str(e)}")


@router.get("/inventory")
def get_configuration_inventory() -> Dict[str, Any]:
    """Returns discovery of all 18 configuration sources and environment variables."""
    report = runtime_instance.inventory_engine.discover_configuration_inventory()
    return _serialize_obj(report)


@router.get("/catalog")
def get_configuration_catalog() -> Dict[str, Any]:
    """Returns classification report across all 18 configuration categories."""
    inv = runtime_instance.inventory_engine.discover_configuration_inventory()
    report = runtime_instance.catalog_engine.build_configuration_catalog(inv)
    return _serialize_obj(report)


@router.get("/validation")
def get_configuration_validation() -> Dict[str, Any]:
    """Returns semantic validation for mandatory variables and anti-pattern detection."""
    inv = runtime_instance.inventory_engine.discover_configuration_inventory()
    cat = runtime_instance.catalog_engine.build_configuration_catalog(inv)
    report = runtime_instance.validation_engine.validate_required_configurations(cat)
    return _serialize_obj(report)


@router.get("/secrets")
def get_secret_inventory_and_backup() -> Dict[str, Any]:
    """Returns multi-engine secret discovery and backup policy verification report."""
    inv = runtime_instance.secret_discovery_engine.discover_and_classify_secrets()
    bk = runtime_instance.secret_backup_engine.verify_secret_backup_strategies(inv)
    return {
        "inventory": _serialize_obj(inv),
        "backup_policies": _serialize_obj(bk),
    }


@router.get("/keys")
def get_encryption_key_recovery() -> Dict[str, Any]:
    """Returns cryptographic key recovery and test decryption roundtrip report."""
    report = runtime_instance.key_recovery_engine.verify_encryption_key_recovery()
    return _serialize_obj(report)


@router.get("/certificates")
def get_certificate_recovery() -> Dict[str, Any]:
    """Returns TLS, mTLS, and internal PKI certificate recovery and handshake report."""
    report = runtime_instance.cert_recovery_engine.verify_certificate_recovery_and_handshakes()
    return _serialize_obj(report)


@router.get("/feature-flags")
def get_feature_flag_recovery() -> Dict[str, Any]:
    """Returns feature flag state preservation and rollback safety report."""
    report = runtime_instance.feature_flag_engine.verify_feature_flag_recovery()
    return _serialize_obj(report)


@router.get("/iac")
def get_iac_recovery() -> Dict[str, Any]:
    """Returns Terraform, Helm, K8s, and Compose infrastructure recovery audit."""
    report = runtime_instance.iac_engine.verify_iac_infrastructure_recovery()
    return _serialize_obj(report)


@router.get("/drift")
def get_configuration_drift() -> Dict[str, Any]:
    """Returns 4-tier differential drift report across Prod, Backup, Git, and Runtime."""
    report = runtime_instance.drift_engine.audit_configuration_drift()
    return _serialize_obj(report)


@router.get("/restore-simulation")
def get_restore_simulation() -> Dict[str, Any]:
    """Returns clean-room restore simulation and full pipeline smoke test report."""
    report = runtime_instance.restore_simulation_engine.execute_configuration_restore_simulation()
    return _serialize_obj(report)


@router.get("/compliance")
def get_compliance_report() -> Dict[str, Any]:
    """Returns evaluation across NIST, OWASP, CIS, ISO 27001, SOC 2, and CNCF."""
    report = runtime_instance.compliance_engine.evaluate_compliance_standards()
    return _serialize_obj(report)


@router.get("/security")
def get_security_report() -> Dict[str, Any]:
    """Returns zero-plaintext, encryption at rest/transit, and access control audit."""
    report = runtime_instance.security_engine.verify_configuration_security_controls()
    return _serialize_obj(report)


@router.get("/scorecard")
def get_configuration_scorecard() -> Dict[str, Any]:
    """Executes full verification and returns the weighted Configuration Quality Scorecard."""
    result = runtime_instance.execute_full_verification()
    return _serialize_obj(result["scorecard"])
