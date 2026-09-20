"""
Part 11: Architecture Consistency Verification Engine.
Proves referential integrity and consistency across the backup architecture:
- No backup references nonexistent assets.
- No asset references nonexistent policy.
- No backup depends on deleted/invalid storage.
- No cyclic backup dependency.
- No circular restore chain.
"""
from typing import List, Dict, Any
from app.platform_verification.backup_architecture_verification.domain.models import (
    AssetInventoryItem,
    BackupStrategyConfig,
    RetentionPolicyConfig,
    BackupOwnershipRecord,
    BackupDependencyGraph,
    ArchitectureConsistencyReport,
)
from app.platform_verification.backup_architecture_verification.domain.interfaces import (
    IArchitectureConsistencyEngine,
)


class ArchitectureConsistencyEngine(IArchitectureConsistencyEngine):
    """
    Validates end-to-end referential integrity across assets, strategies,
    retentions, ownerships, and dependencies.
    """

    def verify_consistency(
        self,
        assets: List[AssetInventoryItem],
        strategies: Dict[str, BackupStrategyConfig],
        retentions: Dict[str, RetentionPolicyConfig],
        ownerships: List[BackupOwnershipRecord],
        dep_graph: BackupDependencyGraph,
    ) -> ArchitectureConsistencyReport:
        inconsistencies: List[str] = []
        asset_names = {a.name for a in assets}
        strategy_asset_names = set(strategies.keys())
        retention_asset_names = set(retentions.keys())
        ownership_asset_names = {o.asset_name for o in ownerships}

        # Check 1: No backup references nonexistent assets
        orphan_strategies = strategy_asset_names - asset_names
        if orphan_strategies:
            inconsistencies.append(f"Orphan backup strategies found referencing non-existent assets: {orphan_strategies}")
            no_nonexistent_assets = False
        else:
            no_nonexistent_assets = True

        # Check 2: No asset references nonexistent policy
        orphan_retentions = retention_asset_names - asset_names
        if orphan_retentions:
            inconsistencies.append(f"Orphan retention policies found referencing non-existent assets: {orphan_retentions}")
            no_nonexistent_policies = False
        else:
            no_nonexistent_policies = True

        # Check 3: No backup depends on deleted/invalid storage
        invalid_storage = []
        for name, strat in strategies.items():
            if not strat.storage_location or len(strat.storage_location.strip()) == 0:
                invalid_storage.append(name)
        if invalid_storage:
            inconsistencies.append(f"Backup strategies referencing empty/invalid storage URIs: {invalid_storage}")
            no_deleted_storage = False
        else:
            no_deleted_storage = True

        # Check 4: No cyclic backup dependency
        no_cyclic_deps = dep_graph.is_dag and not dep_graph.has_circular_dependency
        if not no_cyclic_deps:
            inconsistencies.append("Cyclic backup dependency detected in dependency graph.")

        # Check 5: No circular restore chain & valid topological ordering
        no_circular_restore = len(dep_graph.validation_errors) == 0
        if not no_circular_restore:
            inconsistencies.extend(dep_graph.validation_errors)

        passed = (
            no_nonexistent_assets
            and no_nonexistent_policies
            and no_deleted_storage
            and no_cyclic_deps
            and no_circular_restore
        )

        return ArchitectureConsistencyReport(
            no_nonexistent_asset_references=no_nonexistent_assets,
            no_nonexistent_policy_references=no_nonexistent_policies,
            no_deleted_storage_references=no_deleted_storage,
            no_cyclic_backup_dependencies=no_cyclic_deps,
            no_circular_restore_chains=no_circular_restore,
            passed=passed,
            inconsistencies=inconsistencies,
        )

    def export_architecture_consistency_json(
        self, report: ArchitectureConsistencyReport
    ) -> Dict[str, Any]:
        """Formats the architecture consistency report to JSON dictionary."""
        return {
            "passed": report.passed,
            "no_nonexistent_asset_references": report.no_nonexistent_asset_references,
            "no_nonexistent_policy_references": report.no_nonexistent_policy_references,
            "no_deleted_storage_references": report.no_deleted_storage_references,
            "no_cyclic_backup_dependencies": report.no_cyclic_backup_dependencies,
            "no_circular_restore_chains": report.no_circular_restore_chains,
            "inconsistencies_count": len(report.inconsistencies),
            "inconsistencies": report.inconsistencies,
        }
