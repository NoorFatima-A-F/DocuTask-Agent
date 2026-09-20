"""
FastAPI REST API Router for Multi-Region & Cloud Failover Framework (Part 3G.6).
Exposes endpoints for querying multi-region architecture status, cross-region replication,
traffic failover metrics, chaos simulations, and CI/CD quality gate evaluations.
"""
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.platform_verification.multi_region_failover.runtime.failover_runtime import (
    FailoverRuntime,
)

router = APIRouter(prefix="/api/v1/failover", tags=["Multi-Region & Cloud Failover"])
runtime = FailoverRuntime(base_dir=".")


@router.get("/status", summary="Get Multi-Region Failover Status & Scorecard")
def get_failover_status() -> Dict[str, Any]:
    """
    Returns overall multi-region resilience scorecard, availability tier, and certification verdict.
    """
    result = runtime.execute_failover_verification(export_artifacts=False)
    return {
        "overall_failover_score": result.scorecard.overall_failover_score,
        "availability_tier": result.scorecard.availability_tier.value,
        "certification_verdict": result.scorecard.certification_verdict,
        "ci_cd_deployment_approved": result.scorecard.ci_cd_deployment_approved,
        "passed": result.passed,
        "dimension_scores": {
            "architecture_score": result.scorecard.architecture_score,
            "portability_score": result.scorecard.portability_score,
            "database_failover_score": result.scorecard.database_failover_score,
            "storage_replication_score": result.scorecard.storage_replication_score,
            "traffic_migration_score": result.scorecard.traffic_migration_score,
            "workflow_continuity_score": result.scorecard.workflow_continuity_score,
            "availability_metrics_score": result.scorecard.availability_metrics_score,
        },
    }


@router.get("/architecture", summary="Get Multi-Region Architecture Topology")
def get_architecture_topology() -> Dict[str, Any]:
    """
    Returns primary and secondary region service topology and replication status.
    """
    report = runtime.arch_validator.validate_architecture()
    return {
        "primary_region": report.primary_region.value,
        "secondary_region": report.secondary_region.value,
        "total_services": report.total_critical_services,
        "replicated_count": report.replicated_services_count,
        "passed": report.passed,
        "services": [
            {
                "name": s.service_name,
                "primary": s.primary_status,
                "secondary": s.secondary_status,
                "mode": s.replication_mode,
            }
            for s in report.services
        ],
    }


@router.get("/replication", summary="Get Cross-Region Replication Status")
def get_replication_status() -> Dict[str, Any]:
    """
    Returns database and object storage cross-region synchronization status and lag.
    """
    db_rep = runtime.db_rep_verifier.verify_database_replication()
    storage_rep = runtime.storage_rep_verifier.verify_storage_replication()
    return {
        "database_replication": {
            "health": db_rep.replication_health.value,
            "lag_seconds": db_rep.replication_lag_seconds,
            "primary_lsn": db_rep.current_primary_lsn,
            "replica_lsn": db_rep.replica_replay_lsn,
            "promotion_latency_sec": db_rep.standby_promotion_latency_sec,
            "passed": db_rep.passed,
        },
        "storage_replication": {
            "documents_tested": storage_rep.total_documents_tested,
            "sha256_match_pct": storage_rep.sha256_checksum_match_pct,
            "sync_lag_sec": storage_rep.cross_region_sync_lag_sec,
            "zero_loss": storage_rep.zero_data_loss_verified,
            "passed": storage_rep.passed,
        },
    }


@router.get("/traffic", summary="Get Global Traffic Failover Metrics")
def get_traffic_metrics() -> Dict[str, Any]:
    """
    Returns DNS propagation, traffic shift time, and total failover duration.
    """
    traffic = runtime.traffic_engine.verify_traffic_failover()
    return {
        "global_traffic_manager": traffic.global_traffic_manager,
        "detection_time_sec": traffic.detection_time_sec,
        "dns_propagation_time_sec": traffic.dns_propagation_time_sec,
        "traffic_migration_time_sec": traffic.traffic_migration_time_sec,
        "total_failover_time_sec": traffic.total_failover_time_sec,
        "dropped_requests_pct": traffic.dropped_requests_pct,
        "passed": traffic.passed,
    }


@router.post("/failover/execute", summary="Execute Automated Cloud Failover Pipeline")
def execute_failover() -> Dict[str, Any]:
    """
    Triggers automated regional failover execution and returns stage-by-stage timings.
    """
    execution = runtime.orchestrator.execute_cloud_failover()
    return execution


@router.post("/cicd-gate", summary="Evaluate Multi-Region CI/CD Quality Gate")
def evaluate_cicd_gate() -> Dict[str, Any]:
    """
    Evaluates CI/CD quality gate and returns deployment approval verdict.
    """
    result = runtime.execute_failover_verification(export_artifacts=False)
    return {
        "deployment_approved": result.scorecard.ci_cd_deployment_approved,
        "availability_tier": result.scorecard.availability_tier.value,
        "overall_score": result.scorecard.overall_failover_score,
        "gate_passed": result.passed,
        "certification_verdict": result.scorecard.certification_verdict,
    }
