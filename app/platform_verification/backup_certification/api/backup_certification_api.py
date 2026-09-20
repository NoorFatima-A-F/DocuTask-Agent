"""
FastAPI router for Enterprise Backup Certification Framework (Part 3G.2G).
"""
from typing import Dict, Any
from dataclasses import asdict
from fastapi import APIRouter, HTTPException
from app.platform_verification.backup_certification.runtime.backup_certification_runtime import (
    BackupCertificationRuntime,
)

router = APIRouter(
    prefix="/api/v1/platform-verification/backup-certification",
    tags=["Enterprise Backup Certification"],
)

_runtime = BackupCertificationRuntime()


@router.post("/certify", response_model=Dict[str, Any])
async def execute_backup_certification(output_dir: str = "backup_certification"):
    """
    Executes the complete Backup Readiness Certification pipeline and evaluates CI/CD deployment approval.
    """
    try:
        runtime = BackupCertificationRuntime()
        results = runtime.execute_full_certification(output_dir=output_dir)
        scorecard = results["scorecard"]
        return {
            "status": "COMPLETED",
            "certification_level": scorecard.certification_level.value,
            "overall_score": scorecard.overall_score,
            "passed": scorecard.passed,
            "ci_cd_deployment_approved": scorecard.ci_cd_deployment_approved,
            "artifacts_manifests": results["manifests"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Certification execution failed: {str(e)}")


@router.get("/scorecard", response_model=Dict[str, Any])
async def get_certification_scorecard():
    """
    Returns latest weighted scorecard across all 7 verification categories.
    """
    try:
        results = _runtime.execute_full_certification()
        return asdict(results["scorecard"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch scorecard: {str(e)}")


@router.get("/dashboard", response_model=Dict[str, Any])
async def get_backup_dashboard():
    """
    Returns real-time backup health and recovery metrics for operational dashboard.
    """
    try:
        results = _runtime.execute_full_certification()
        return asdict(results["dashboard"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch dashboard: {str(e)}")


@router.get("/rto-rpo", response_model=Dict[str, Any])
async def get_rto_rpo_metrics():
    """
    Returns Recovery Time Objective (RTO) and Recovery Point Objective (RPO) certification metrics.
    """
    try:
        evidence = _runtime.evidence_collector.collect_all_evidence()
        rto_rpo = _runtime.rto_rpo_certifier.certify_rto_rpo(evidence)
        return asdict(rto_rpo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to evaluate RTO/RPO: {str(e)}")


@router.get("/risk-register", response_model=Dict[str, Any])
async def get_backup_risk_register():
    """
    Returns the comprehensive backup and disaster recovery risk register.
    """
    try:
        results = _runtime.execute_full_certification()
        return asdict(results["risks"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate risk register: {str(e)}")


@router.get("/continuous-schedule", response_model=Dict[str, Any])
async def get_continuous_verification_schedule():
    """
    Returns daily, weekly, monthly, and quarterly scheduled verification jobs.
    """
    try:
        schedule = _runtime.continuous_engine.generate_verification_schedule()
        return asdict(schedule)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch verification schedule: {str(e)}")
