"""
FastAPI router for Enterprise Backup Security Verification Framework (Part 3G.2F).
"""
from typing import Dict, Any
from dataclasses import asdict
from fastapi import APIRouter, HTTPException
from app.platform_verification.backup_security_verification.runtime.backup_security_runtime import (
    BackupSecurityVerificationRuntime,
)

router = APIRouter(
    prefix="/api/v1/platform-verification/backup-security",
    tags=["Enterprise Backup Security Verification"],
)

_runtime = BackupSecurityVerificationRuntime()


@router.post("/execute", response_model=Dict[str, Any])
async def execute_backup_security_verification(evidence_dir: str = "evidence/backup_security_verification"):
    """
    Triggers an end-to-end Enterprise Backup Security Verification scan.
    """
    try:
        runtime = BackupSecurityVerificationRuntime()
        results = runtime.execute_full_security_verification(output_dir=evidence_dir)
        scorecard = results["scorecard"]
        return {
            "status": "COMPLETED",
            "composite_score": scorecard.composite_score,
            "certification_tier": scorecard.certification_tier.value,
            "passed": scorecard.passed,
            "execution_duration_ms": scorecard.execution_duration_ms,
            "evidence_manifests": results["exported_manifest_paths"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification execution failed: {str(e)}")


@router.get("/scorecard", response_model=Dict[str, Any])
async def get_latest_scorecard():
    """
    Retrieves the latest Backup Security Verification Scorecard.
    """
    try:
        results = _runtime.execute_full_security_verification()
        return asdict(results["scorecard"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate scorecard: {str(e)}")


@router.get("/inventory", response_model=Dict[str, Any])
async def get_backup_security_inventory():
    """
    Returns inventory of protected backup assets and their security classifications.
    """
    inv_report = _runtime.inventory_engine.discover_backup_security_inventory()
    class_report = _runtime.classification_engine.verify_data_classification_controls(inv_report)
    return {
        "inventory": asdict(inv_report),
        "classification": asdict(class_report),
    }


@router.get("/encryption-status", response_model=Dict[str, Any])
async def get_encryption_status():
    """
    Returns encryption compliance status across all backup assets.
    """
    enc_report = _runtime.encryption_engine.verify_backup_encryption()
    return asdict(enc_report)


@router.get("/tamper-resistance", response_model=Dict[str, Any])
async def get_tamper_resistance_status():
    """
    Returns cryptographic tamper resistance and poisoning protection status.
    """
    tamper_report = _runtime.tamper_detector.test_backup_tamper_detection()
    poisoning_report = _runtime.poisoning_protection.verify_backup_poisoning_protection()
    return {
        "tamper_detection": asdict(tamper_report),
        "poisoning_protection": asdict(poisoning_report),
    }


@router.get("/immutability-status", response_model=Dict[str, Any])
async def get_immutability_status():
    """
    Returns S3 Object Lock and WORM retention policy enforcement status.
    """
    imm_report = _runtime.immutability_engine.verify_storage_immutability_and_worm()
    return asdict(imm_report)


@router.get("/compliance", response_model=Dict[str, Any])
async def get_compliance_status():
    """
    Returns regulatory and enterprise framework compliance status.
    """
    comp_report = _runtime.compliance_engine.evaluate_backup_security_compliance()
    return asdict(comp_report)
