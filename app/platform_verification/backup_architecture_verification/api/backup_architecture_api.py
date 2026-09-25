"""
REST API Router for Enterprise Backup Architecture Verification (Part 3G.2A).
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Query
from app.platform_verification.backup_architecture_verification.runtime.backup_verification_runtime import (
    BackupArchitectureVerificationRuntime,
)

router = APIRouter(
    prefix="/api/v1/verification/backup-architecture",
    tags=["Enterprise Backup Architecture Verification (Part 3G.2A)"],
)

runtime_instance = BackupArchitectureVerificationRuntime()


@router.post("/run", response_model=Dict[str, Any])
def run_full_backup_verification(
    export_evidence: bool = Query(default=True, description="Whether to export evidence JSON artifacts to disk")
) -> Dict[str, Any]:
    """Triggers the full 14-part backup architecture verification pipeline."""
    try:
        result = runtime_instance.run_full_verification(export_evidence=export_evidence)
        return {
            "status": "SUCCESS",
            "scorecard": result["scorecard_dict"],
            "exported_artifacts": result["exported_artifacts"],
            "consistency_passed": result["consistency_passed"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification execution failed: {str(e)}")


@router.get("/inventory")
def get_asset_inventory() -> Dict[str, Any]:
    """Returns the automatically discovered platform asset inventory (Part 1)."""
    assets = runtime_instance.discovery.discover_assets()
    return runtime_instance.discovery.export_inventory_json(assets)


@router.get("/classification")
def get_classification_matrix() -> Dict[str, Any]:
    """Returns the multi-tier asset classification matrix (Part 2)."""
    assets = runtime_instance.discovery.discover_assets()
    matrix = runtime_instance.classification.classify_assets(assets)
    return runtime_instance.classification.export_classification_matrix_json(matrix)


@router.get("/strategy")
def get_strategy_report() -> Dict[str, Any]:
    """Returns the backup strategy validation report (Part 3)."""
    assets = runtime_instance.discovery.discover_assets()
    matrix = runtime_instance.classification.classify_assets(assets)
    strategies = runtime_instance.strategy_validator.get_default_platform_strategies()
    results = runtime_instance.strategy_validator.validate_strategies(assets, matrix, strategies)
    return runtime_instance.strategy_validator.export_strategy_report_json(results)


@router.get("/dependency-graph")
def get_dependency_graph() -> Dict[str, Any]:
    """Returns the recovery dependency DAG and topological restore order (Part 4)."""
    assets = runtime_instance.discovery.discover_assets()
    graph = runtime_instance.dep_graph_engine.build_and_validate_graph(assets)
    return runtime_instance.dep_graph_engine.export_dependency_graph_json(graph)


@router.get("/coverage")
def get_coverage_report() -> Dict[str, Any]:
    """Returns the backup coverage analysis and tier target verification (Part 5)."""
    assets = runtime_instance.discovery.discover_assets()
    strategies = runtime_instance.strategy_validator.get_default_platform_strategies()
    retentions = runtime_instance.retention_verifier.get_default_platform_retention_policies()
    report = runtime_instance.coverage_analyzer.analyze_coverage(assets, strategies, retentions)
    return runtime_instance.coverage_analyzer.export_coverage_report_json(report)


@router.get("/retention")
def get_retention_report() -> Dict[str, Any]:
    """Returns the GFS retention policy validation report (Part 6)."""
    assets = runtime_instance.discovery.discover_assets()
    retentions = runtime_instance.retention_verifier.get_default_platform_retention_policies()
    results = runtime_instance.retention_verifier.verify_retention_policies(assets, retentions)
    return runtime_instance.retention_verifier.export_retention_report_json(results)


@router.get("/lifecycle")
def get_lifecycle_report() -> Dict[str, Any]:
    """Returns the 8-stage backup lifecycle validation report (Part 7)."""
    assets = runtime_instance.discovery.discover_assets()
    reports = runtime_instance.lifecycle_validator.validate_lifecycles(assets)
    return runtime_instance.lifecycle_validator.export_lifecycle_report_json(reports)


@router.get("/ownership")
def get_ownership_report() -> Dict[str, Any]:
    """Returns the backup ownership, restore owner, and escalation matrix (Part 8)."""
    assets = runtime_instance.discovery.discover_assets()
    records = runtime_instance.ownership_engine.verify_ownership(assets)
    return runtime_instance.ownership_engine.export_ownership_report_json(records)


@router.get("/metadata-registry")
def get_metadata_registry() -> Dict[str, Any]:
    """Returns the cryptographic metadata registry for all backups (Part 9)."""
    assets = runtime_instance.discovery.discover_assets()
    entries = runtime_instance.metadata_engine.generate_metadata_registry(assets)
    return runtime_instance.metadata_engine.export_metadata_registry_json(entries)


@router.get("/policies")
def get_policy_validation() -> Dict[str, Any]:
    """Returns the backup policy validation results (Part 10)."""
    policies = runtime_instance.policy_validator.get_default_platform_policies()
    results = runtime_instance.policy_validator.validate_policies(policies)
    return runtime_instance.policy_validator.export_policy_validation_json(results)


@router.get("/consistency")
def get_architecture_consistency() -> Dict[str, Any]:
    """Returns the architectural consistency and referential integrity report (Part 11)."""
    assets = runtime_instance.discovery.discover_assets()
    strategies = runtime_instance.strategy_validator.get_default_platform_strategies()
    retentions = runtime_instance.retention_verifier.get_default_platform_retention_policies()
    ownerships = runtime_instance.ownership_engine.verify_ownership(assets)
    graph = runtime_instance.dep_graph_engine.build_and_validate_graph(assets)
    report = runtime_instance.consistency_engine.verify_consistency(assets, strategies, retentions, ownerships, graph)
    return runtime_instance.consistency_engine.export_architecture_consistency_json(report)


@router.get("/metrics")
def get_observability_metrics() -> Dict[str, Any]:
    """Returns observability metrics in Prometheus, OpenTelemetry, and Grafana formats (Part 12)."""
    assets = runtime_instance.discovery.discover_assets()
    strategies = runtime_instance.strategy_validator.get_default_platform_strategies()
    retentions = runtime_instance.retention_verifier.get_default_platform_retention_policies()
    coverage = runtime_instance.coverage_analyzer.analyze_coverage(assets, strategies, retentions)
    entries = runtime_instance.metadata_engine.generate_metadata_registry(assets)
    report = runtime_instance.observability.generate_metrics_report(coverage, entries)
    return runtime_instance.observability.export_metrics_json(report)


@router.get("/scorecard")
def get_readiness_scorecard() -> Dict[str, Any]:
    """Returns the latest Backup Readiness Scorecard and Enterprise Certification Tier (Part 14)."""
    result = runtime_instance.run_full_verification(export_evidence=False)
    return result["scorecard_dict"]
