"""
Phase 3J.1: Performance Verification REST API Router
Provides endpoints for baseline metrics, load testing results, bottleneck diagnostics, and performance certification.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.platform_verification.performance_capacity_engineering.runtime.performance_verification_runtime import (
    PerformanceVerificationRuntime,
)

router = APIRouter(
    prefix="/api/v1/performance-verification",
    tags=["Performance Infrastructure & Baseline Capacity Engineering"],
)

_runtime_instance = PerformanceVerificationRuntime()


@router.get("/status")
def get_platform_status() -> Dict[str, Any]:
    """Returns the operational status of the Performance Testing & Capacity Engineering framework."""
    return {
        "status": "ONLINE",
        "phase": "Phase 3J.1 — Performance Infrastructure Verification: Load Testing & Baseline Capacity Engineering",
        "system": "DocuTask Agent",
        "environment": "Performance-Testing-Cluster",
        "load_generator": "k6 Distributed Load Generator (v0.50.0)",
    }


@router.post("/run-verification")
def run_full_performance_verification() -> Dict[str, Any]:
    """Executes full verification across all 10 modules, computes 6-category certification, and exports manifests."""
    try:
        pipeline_result = _runtime_instance.run_pipeline()
        cert_report = pipeline_result["certification_report"]
        return {
            "status": "SUCCESS",
            "certification_granted": pipeline_result["success"],
            "composite_performance_score_pct": cert_report.composite_performance_score_pct,
            "certification_tier": cert_report.certification_tier.value,
            "exported_files_count": len(pipeline_result["exported_files"]),
            "exported_files": pipeline_result["exported_files"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Performance verification pipeline failed: {str(e)}")


@router.get("/baseline")
def get_baseline_performance() -> Dict[str, Any]:
    """Returns baseline API latency percentiles, throughput, and resource profiles."""
    report = _runtime_instance.baseline_verifier.verify()
    return report.model_dump()


@router.get("/load-tests")
def get_controlled_load_test_results() -> Dict[str, Any]:
    """Returns progressive 4-stage load testing results (Smoke, Normal, Capacity, Breaking Point)."""
    report = _runtime_instance.load_test_verifier.verify()
    return report.model_dump()


@router.get("/bottlenecks")
def get_bottleneck_diagnostics() -> Dict[str, Any]:
    """Returns bottleneck analysis across API, Database, Queue, Workers, and AI Provider."""
    report = _runtime_instance.bottleneck_verifier.verify()
    return report.model_dump()


@router.get("/ai-pipeline")
def get_ai_pipeline_performance() -> Dict[str, Any]:
    """Returns per-stage AI document workflow latencies, token consumption, and cost metrics."""
    report = _runtime_instance.ai_pipeline_verifier.verify()
    return report.model_dump()


@router.get("/certification")
def get_performance_certification() -> Dict[str, Any]:
    """Computes and returns the 6-category performance certification scorecard."""
    verification_results = _runtime_instance.execute_all_verifications()
    cert_report = _runtime_instance.scorer.compute_certification(verification_results)
    return cert_report.model_dump()
