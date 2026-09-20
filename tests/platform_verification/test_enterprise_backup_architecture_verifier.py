"""
Comprehensive Unit & Integration Test Suite for Enterprise Backup Architecture Verification (Part 3G.2A).
"""
import os
import pytest
from app.platform_verification.backup_architecture_verification.domain.models import (
    AssetCategory,
    CriticalityTier,
    BackupStrategyType,
    LifecycleStage,
    CertificationTier,
    VerificationStatus,
    AssetInventoryItem,
    BackupStrategyConfig,
    RetentionPolicyConfig,
    DependencyGraphNode,
    BackupDependencyGraph,
)
from app.platform_verification.backup_architecture_verification.runtime.backup_verification_runtime import (
    BackupArchitectureVerificationRuntime,
)
from app.platform_verification.backup_architecture_verification.api.backup_architecture_api import (
    router,
    get_asset_inventory,
    get_classification_matrix,
    get_strategy_report,
    get_dependency_graph,
    get_coverage_report,
    get_retention_report,
    get_lifecycle_report,
    get_ownership_report,
    get_metadata_registry,
    get_policy_validation,
    get_architecture_consistency,
    get_observability_metrics,
    get_readiness_scorecard,
    run_full_backup_verification,
)


@pytest.fixture
def runtime():
    return BackupArchitectureVerificationRuntime()


# ---------------------------------------------------------------------------
# Part 1: Asset Discovery Tests
# ---------------------------------------------------------------------------
def test_asset_discovery_comprehensive(runtime):
    assets = runtime.discovery.discover_assets()
    assert len(assets) >= 20

    asset_map = {a.name: a for a in assets}
    # Infrastructure assets
    assert "postgres_primary" in asset_map
    assert "redis_cache_queue" in asset_map
    assert "docker_named_volumes" in asset_map
    assert "minio_s3_object_store" in asset_map

    # Document & AI assets
    assert "uploaded_documents_raw" in asset_map
    assert "ocr_extracted_text_artifacts" in asset_map
    assert "extracted_structured_json" in asset_map
    assert "ai_verification_evidence" in asset_map

    # Config, secrets & runtime state
    assert "app_environment_variables" in asset_map
    assert "enterprise_secrets_vault" in asset_map
    assert "agent_registry_state" in asset_map
    assert "agent_memory_episodes" in asset_map
    assert "vector_embeddings_index" in asset_map
    assert "system_governance_policies" in asset_map

    # Observability & Rebuildable
    assert "application_audit_logs" in asset_map
    assert "prometheus_metrics_db" in asset_map
    assert "temporary_processing_cache" in asset_map

    json_export = runtime.discovery.export_inventory_json(assets)
    assert json_export["total_assets_discovered"] == len(assets)
    assert len(json_export["assets"]) == len(assets)


# ---------------------------------------------------------------------------
# Part 2: Classification Matrix Tests
# ---------------------------------------------------------------------------
def test_classification_engine(runtime):
    assets = runtime.discovery.discover_assets()
    matrix = runtime.classification.classify_assets(assets)

    assert len(matrix) == len(assets)
    assert matrix["postgres_primary"].criticality == CriticalityTier.TIER_0
    assert matrix["postgres_primary"].max_rpo_seconds == 0  # Near-zero RPO
    assert matrix["postgres_primary"].recovery_priority == "Immediate"

    assert matrix["ocr_extracted_text_artifacts"].criticality == CriticalityTier.TIER_1
    assert matrix["ocr_extracted_text_artifacts"].max_rpo_seconds == 900  # 15 min

    assert matrix["application_audit_logs"].criticality == CriticalityTier.TIER_2
    assert matrix["application_audit_logs"].max_rpo_seconds == 86400  # 24 hours

    assert matrix["temporary_processing_cache"].criticality == CriticalityTier.TIER_3

    json_export = runtime.classification.export_classification_matrix_json(matrix)
    assert json_export["tier_summary"]["Tier0_Mission_Critical"] >= 5
    assert json_export["tier_summary"]["Tier1_Business_Critical"] >= 5


# ---------------------------------------------------------------------------
# Part 3: Strategy Validation Tests
# ---------------------------------------------------------------------------
def test_strategy_validation_engine(runtime):
    assets = runtime.discovery.discover_assets()
    matrix = runtime.classification.classify_assets(assets)
    strategies = runtime.strategy_validator.get_default_platform_strategies()

    results = runtime.strategy_validator.validate_strategies(assets, matrix, strategies)
    assert len(results) == len(assets)
    assert all(r.is_adequate for r in results)

    # Test edge case: Tier 0 database without WAL archiving fails validation
    flawed_strategies = strategies.copy()
    flawed_strategies["postgres_primary"] = BackupStrategyConfig(
        asset_name="postgres_primary",
        strategy_type=BackupStrategyType.INCREMENTAL,
        frequency_cron="0 2 * * *",
        estimated_size_mb=10240.0,
        retention_days=30,
        storage_location="s3://docutask-backups/postgres/",
        is_continuous=False,
        wal_archiving_enabled=False,  # FLAW: Missing WAL
    )
    flawed_results = runtime.strategy_validator.validate_strategies(assets, matrix, flawed_strategies)
    pg_result = next(r for r in flawed_results if r.asset_name == "postgres_primary")
    assert pg_result.is_adequate is False
    assert any("continuous WAL archiving" in f for f in pg_result.findings)


# ---------------------------------------------------------------------------
# Part 4: Dependency Graph & Topological Recovery Order Tests
# ---------------------------------------------------------------------------
def test_dependency_graph_and_topological_ordering(runtime):
    assets = runtime.discovery.discover_assets()
    graph = runtime.dep_graph_engine.build_and_validate_graph(assets)

    assert graph.is_dag is True
    assert graph.has_circular_dependency is False
    assert len(graph.validation_errors) == 0

    order = graph.topological_recovery_order
    assert len(order) == len(assets)

    # Validate essential ordering rules:
    # 1. Environment Config before Secrets Vault
    assert order.index("app_environment_variables") < order.index("enterprise_secrets_vault")
    # 2. Secrets Vault before Database
    assert order.index("enterprise_secrets_vault") < order.index("postgres_primary")
    # 3. Database before Storage & Agents
    assert order.index("postgres_primary") < order.index("agent_registry_state")
    assert order.index("postgres_primary") < order.index("agent_memory_episodes")
    assert order.index("postgres_primary") < order.index("extracted_structured_json")

    # Validate custom sequence checker
    valid_seq = ["app_environment_variables", "enterprise_secrets_vault", "postgres_primary"]
    assert runtime.dep_graph_engine.validate_custom_recovery_sequence(graph, valid_seq) is True

    invalid_seq = ["postgres_primary", "enterprise_secrets_vault"]
    assert runtime.dep_graph_engine.validate_custom_recovery_sequence(graph, invalid_seq) is False


# ---------------------------------------------------------------------------
# Part 5: Coverage Analysis Tests
# ---------------------------------------------------------------------------
def test_coverage_analysis_engine(runtime):
    assets = runtime.discovery.discover_assets()
    strategies = runtime.strategy_validator.get_default_platform_strategies()
    retentions = runtime.retention_verifier.get_default_platform_retention_policies()

    report = runtime.coverage_analyzer.analyze_coverage(assets, strategies, retentions)
    assert report.tier0_coverage_percent == 100.0
    assert report.tier1_coverage_percent == 100.0
    assert report.tier2_coverage_percent == 100.0
    assert report.tier0_compliant is True
    assert report.tier1_compliant is True
    assert report.tier2_compliant is True
    assert len(report.unprotected_assets) == 0

    # Test coverage drop when strategy is missing
    flawed_strategies = {k: v for k, v in strategies.items() if k != "postgres_primary"}
    flawed_report = runtime.coverage_analyzer.analyze_coverage(assets, flawed_strategies, retentions)
    assert flawed_report.tier0_compliant is False
    assert "postgres_primary" in flawed_report.unprotected_assets


# ---------------------------------------------------------------------------
# Part 6: Retention Verification Tests
# ---------------------------------------------------------------------------
def test_retention_verification_engine(runtime):
    assets = runtime.discovery.discover_assets()
    retentions = runtime.retention_verifier.get_default_platform_retention_policies()

    results = runtime.retention_verifier.verify_retention_policies(assets, retentions)
    assert all(r.is_valid for r in results)

    # Test edge case: Inadequate retention on Tier 0 asset
    flawed_retentions = retentions.copy()
    flawed_retentions["postgres_primary"] = RetentionPolicyConfig(
        asset_name="postgres_primary",
        daily_retention_days=3,  # FLAW: < 14 days
        weekly_retention_weeks=0,
        monthly_retention_months=0,
        yearly_retention_years=0,
        archival_tier="standard",
        legal_hold_supported=False,  # FLAW: No legal hold
        immutability_enabled=False,   # FLAW: No immutability
        auto_expiration_enabled=True,
        secure_deletion_method="simple_delete",
    )
    flawed_results = runtime.retention_verifier.verify_retention_policies(assets, flawed_retentions)
    pg_res = next(r for r in flawed_results if r.asset_name == "postgres_primary")
    assert pg_res.is_valid is False
    assert pg_res.has_accidental_purge_risk is True


# ---------------------------------------------------------------------------
# Part 7: Lifecycle Validation Tests
# ---------------------------------------------------------------------------
def test_lifecycle_validation_engine(runtime):
    assets = runtime.discovery.discover_assets()
    reports = runtime.lifecycle_validator.validate_lifecycles(assets)

    assert len(reports) == len(assets)
    assert all(r.lifecycle_complete for r in reports)

    protected_reports = [r for r in reports if r.stages]
    for rep in protected_reports:
        assert len(rep.stages) == 8
        assert LifecycleStage.ASSET.value in rep.stages
        assert LifecycleStage.BACKUP.value in rep.stages
        assert LifecycleStage.VERIFICATION.value in rep.stages
        assert LifecycleStage.STORAGE.value in rep.stages
        assert LifecycleStage.REPLICATION.value in rep.stages
        assert LifecycleStage.RETENTION.value in rep.stages
        assert LifecycleStage.EXPIRATION.value in rep.stages
        assert LifecycleStage.SECURE_DESTRUCTION.value in rep.stages


# ---------------------------------------------------------------------------
# Part 8: Ownership Model Tests
# ---------------------------------------------------------------------------
def test_ownership_model_engine(runtime):
    assets = runtime.discovery.discover_assets()
    records = runtime.ownership_engine.verify_ownership(assets)

    assert len(records) == len(assets)
    assert all(r.has_assigned_owners for r in records)
    assert all(r.owner_team != "UNASSIGNED" for r in records)
    assert all(r.restore_owner_team != "UNASSIGNED" for r in records)
    assert all(r.verification_owner_team != "UNASSIGNED" for r in records)


# ---------------------------------------------------------------------------
# Part 9: Metadata Engine Tests
# ---------------------------------------------------------------------------
def test_metadata_engine(runtime):
    assets = runtime.discovery.discover_assets()
    entries = runtime.metadata_engine.generate_metadata_registry(assets)

    assert len(entries) >= 20
    for e in entries:
        assert len(e.backup_uuid) == 36  # UUID v4/v5 format
        assert len(e.sha256_checksum) == 64  # SHA256 hex length
        assert e.encryption_status == "ENCRYPTED_AES256_GCM"
        assert e.verification_status == VerificationStatus.PASSED
        assert e.compression_ratio >= 1.0


# ---------------------------------------------------------------------------
# Part 10: Policy Validation Tests
# ---------------------------------------------------------------------------
def test_policy_validation_engine(runtime):
    policies = runtime.policy_validator.get_default_platform_policies()
    results = runtime.policy_validator.validate_policies(policies)

    assert len(results) == len(policies)
    assert all(r.is_valid for r in results)
    assert all(r.encryption_enforced for r in results)
    assert all(r.validation_hook_configured for r in results)


# ---------------------------------------------------------------------------
# Part 11: Architecture Consistency Tests
# ---------------------------------------------------------------------------
def test_architecture_consistency_engine(runtime):
    assets = runtime.discovery.discover_assets()
    strategies = runtime.strategy_validator.get_default_platform_strategies()
    retentions = runtime.retention_verifier.get_default_platform_retention_policies()
    ownerships = runtime.ownership_engine.verify_ownership(assets)
    dep_graph = runtime.dep_graph_engine.build_and_validate_graph(assets)

    report = runtime.consistency_engine.verify_consistency(
        assets, strategies, retentions, ownerships, dep_graph
    )
    assert report.passed is True
    assert report.no_nonexistent_asset_references is True
    assert report.no_nonexistent_policy_references is True
    assert report.no_deleted_storage_references is True
    assert report.no_cyclic_backup_dependencies is True
    assert report.no_circular_restore_chains is True
    assert len(report.inconsistencies) == 0


# ---------------------------------------------------------------------------
# Part 12: Observability Tests
# ---------------------------------------------------------------------------
def test_observability_engine(runtime):
    assets = runtime.discovery.discover_assets()
    strategies = runtime.strategy_validator.get_default_platform_strategies()
    retentions = runtime.retention_verifier.get_default_platform_retention_policies()
    coverage = runtime.coverage_analyzer.analyze_coverage(assets, strategies, retentions)
    metadata_list = runtime.metadata_engine.generate_metadata_registry(assets)

    metrics = runtime.observability.generate_metrics_report(coverage, metadata_list)
    assert metrics.backup_success_rate_percent == 100.0
    assert metrics.verification_success_percent == 100.0
    assert metrics.stale_backup_count == 0
    assert "docutask_backup_coverage_ratio 100.0" in metrics.prometheus_metrics
    assert "docutask_backup_total_storage_bytes" in metrics.prometheus_metrics
    assert "resourceMetrics" in metrics.opentelemetry_metrics
    assert "dashboard" in metrics.grafana_dashboard_json


# ---------------------------------------------------------------------------
# Part 13 & 14: Evidence Manifest & Full Scorecard Tests
# ---------------------------------------------------------------------------
def test_readiness_scorecard_and_evidence_generation(runtime, tmp_path):
    result = runtime.run_full_verification(export_evidence=True, output_dir=str(tmp_path))
    scorecard = result["scorecard"]

    # Verify score weights & thresholds
    assert scorecard.readiness_composite_score >= 95.0
    assert scorecard.certification_tier == CertificationTier.ENTERPRISE_CERTIFIED
    assert scorecard.passed is True

    # Verify all 14 evidence files generated on disk
    expected_files = [
        "asset_inventory.json",
        "classification_matrix.json",
        "strategy_report.json",
        "dependency_graph.json",
        "coverage_report.json",
        "retention_report.json",
        "lifecycle_report.json",
        "ownership_report.json",
        "metadata_registry.json",
        "policy_validation.json",
        "architecture_consistency.json",
        "metrics.json",
        "verification_metadata.json",
        "evidence_manifest.json",
    ]

    for filename in expected_files:
        filepath = tmp_path / filename
        assert filepath.exists(), f"Missing artifact: {filename}"
        assert filepath.stat().st_size > 0


# ---------------------------------------------------------------------------
# API Layer Tests
# ---------------------------------------------------------------------------
def test_api_endpoints_direct_calls():
    inv = get_asset_inventory()
    assert inv["total_assets_discovered"] >= 20

    cls_mat = get_classification_matrix()
    assert len(cls_mat["classification_matrix"]) >= 20

    strat = get_strategy_report()
    assert strat["overall_strategy_compliance_percent"] == 100.0

    dep = get_dependency_graph()
    assert dep["is_valid_dag"] is True

    cov = get_coverage_report()
    assert cov["total_coverage_percent"] == 100.0

    ret = get_retention_report()
    assert ret["retention_compliance_percent"] == 100.0

    life = get_lifecycle_report()
    assert life["lifecycle_compliance_percent"] == 100.0

    own = get_ownership_report()
    assert own["ownership_compliance_percent"] == 100.0

    meta = get_metadata_registry()
    assert meta["all_backups_verified"] is True

    pol = get_policy_validation()
    assert pol["policy_compliance_percent"] == 100.0

    cons = get_architecture_consistency()
    assert cons["passed"] is True

    metr = get_observability_metrics()
    assert metr["summary_metrics"]["backup_success_rate_percent"] == 100.0

    sc = get_readiness_scorecard()
    assert sc["readiness_composite_score"] >= 95.0

    run_res = run_full_backup_verification(export_evidence=False)
    assert run_res["status"] == "SUCCESS"
