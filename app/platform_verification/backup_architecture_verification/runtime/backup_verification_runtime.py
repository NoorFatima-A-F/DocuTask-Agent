"""
Unified Runtime Orchestrator for Enterprise Backup Architecture Verification (Part 3G.2A).
Coordinates all 14 verification engines and generates enterprise certification scorecards.
"""
import time
from typing import Dict, Any, Optional

from app.platform_verification.backup_architecture_verification.core.discovery_engine import (
    AssetDiscoveryEngine,
)
from app.platform_verification.backup_architecture_verification.core.classification_engine import (
    ClassificationEngine,
)
from app.platform_verification.backup_architecture_verification.core.strategy_validation_engine import (
    StrategyValidationEngine,
)
from app.platform_verification.backup_architecture_verification.core.dependency_graph_engine import (
    DependencyGraphEngine,
)
from app.platform_verification.backup_architecture_verification.core.coverage_analysis_engine import (
    CoverageAnalysisEngine,
)
from app.platform_verification.backup_architecture_verification.core.retention_verification_engine import (
    RetentionVerificationEngine,
)
from app.platform_verification.backup_architecture_verification.core.lifecycle_validation_engine import (
    LifecycleValidationEngine,
)
from app.platform_verification.backup_architecture_verification.core.ownership_model_engine import (
    OwnershipModelEngine,
)
from app.platform_verification.backup_architecture_verification.core.metadata_engine import (
    BackupMetadataEngine,
)
from app.platform_verification.backup_architecture_verification.core.policy_validation_engine import (
    PolicyValidationEngine,
)
from app.platform_verification.backup_architecture_verification.core.architecture_consistency_engine import (
    ArchitectureConsistencyEngine,
)
from app.platform_verification.backup_architecture_verification.core.observability_engine import (
    ObservabilityEngine,
)
from app.platform_verification.backup_architecture_verification.core.evidence_manifest_engine import (
    EvidenceManifestEngine,
)
from app.platform_verification.backup_architecture_verification.core.readiness_scoring_engine import (
    ReadinessScoringEngine,
)
from app.platform_verification.backup_architecture_verification.domain.models import (
    BackupReadinessScorecard,
)


class BackupArchitectureVerificationRuntime:
    """
    Master Runtime Orchestrator for Enterprise Backup Architecture Verification.
    """

    def __init__(
        self,
        git_commit_sha: str = "d8e41a9bf73298c56e290fbbd0e82c7a1092a3f1",
        platform_version: str = "2.4.0",
        environment: str = "production-enterprise",
    ):
        self.git_commit_sha = git_commit_sha
        self.platform_version = platform_version
        self.environment = environment

        # Initialize engines
        self.discovery = AssetDiscoveryEngine()
        self.classification = ClassificationEngine()
        self.strategy_validator = StrategyValidationEngine()
        self.dep_graph_engine = DependencyGraphEngine()
        self.coverage_analyzer = CoverageAnalysisEngine()
        self.retention_verifier = RetentionVerificationEngine()
        self.lifecycle_validator = LifecycleValidationEngine()
        self.ownership_engine = OwnershipModelEngine()
        self.metadata_engine = BackupMetadataEngine(
            git_commit_sha=git_commit_sha,
            platform_version=platform_version,
            environment=environment,
        )
        self.policy_validator = PolicyValidationEngine()
        self.consistency_engine = ArchitectureConsistencyEngine()
        self.observability = ObservabilityEngine()
        self.manifest_engine = EvidenceManifestEngine(
            git_commit_sha=git_commit_sha,
            platform_version=platform_version,
            environment=environment,
        )
        self.scoring_engine = ReadinessScoringEngine()

    def run_full_verification(
        self, export_evidence: bool = True, output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        start_time = time.perf_counter()

        # 1. Asset Discovery (10% weight)
        assets = self.discovery.discover_assets()
        asset_discovery_score = 100.0 if len(assets) >= 20 else 70.0
        inventory_json = self.discovery.export_inventory_json(assets)

        # 2. Classification Engine (10% weight)
        classification_matrix = self.classification.classify_assets(assets)
        classification_score = 100.0 if len(classification_matrix) == len(assets) else 75.0
        classification_json = self.classification.export_classification_matrix_json(classification_matrix)

        # 3. Strategy Validation (20% weight)
        strategies = self.strategy_validator.get_default_platform_strategies()
        strategy_results = self.strategy_validator.validate_strategies(
            assets=assets,
            classifications=classification_matrix,
            strategies=strategies,
        )
        strategy_report_json = self.strategy_validator.export_strategy_report_json(strategy_results)
        strategy_score = strategy_report_json["overall_strategy_compliance_percent"]

        # 4. Dependency Graph Engine
        dep_graph = self.dep_graph_engine.build_and_validate_graph(assets)
        dep_graph_json = self.dep_graph_engine.export_dependency_graph_json(dep_graph)

        # 5. Coverage Analysis (20% weight)
        retentions = self.retention_verifier.get_default_platform_retention_policies()
        coverage_report = self.coverage_analyzer.analyze_coverage(
            assets=assets,
            strategies=strategies,
            retentions=retentions,
        )
        coverage_report_json = self.coverage_analyzer.export_coverage_report_json(coverage_report)
        coverage_score = coverage_report.total_coverage_percent

        # 6. Retention Verification (10% weight)
        retention_results = self.retention_verifier.verify_retention_policies(
            assets=assets,
            retentions=retentions,
        )
        retention_report_json = self.retention_verifier.export_retention_report_json(retention_results)
        retention_score = retention_report_json["retention_compliance_percent"]

        # 7. Lifecycle Validation (10% weight)
        lifecycle_reports = self.lifecycle_validator.validate_lifecycles(assets)
        lifecycle_report_json = self.lifecycle_validator.export_lifecycle_report_json(lifecycle_reports)
        lifecycle_score = lifecycle_report_json["lifecycle_compliance_percent"]

        # 8. Ownership Model
        ownership_records = self.ownership_engine.verify_ownership(assets)
        ownership_report_json = self.ownership_engine.export_ownership_report_json(ownership_records)

        # 9. Metadata Engine (10% weight)
        metadata_entries = self.metadata_engine.generate_metadata_registry(assets)
        metadata_registry_json = self.metadata_engine.export_metadata_registry_json(metadata_entries)
        metadata_score = 100.0 if metadata_registry_json["all_backups_verified"] else 60.0

        # 10. Policy Validation Engine (5% weight)
        policies = self.policy_validator.get_default_platform_policies()
        policy_results = self.policy_validator.validate_policies(policies)
        policy_validation_json = self.policy_validator.export_policy_validation_json(policy_results)
        policy_score = policy_validation_json["policy_compliance_percent"]

        # 11. Architecture Consistency Engine
        consistency_report = self.consistency_engine.verify_consistency(
            assets=assets,
            strategies=strategies,
            retentions=retentions,
            ownerships=ownership_records,
            dep_graph=dep_graph,
        )
        consistency_json = self.consistency_engine.export_architecture_consistency_json(consistency_report)

        # 12. Observability Engine (5% weight)
        metrics_report = self.observability.generate_metrics_report(
            coverage=coverage_report,
            metadata_list=metadata_entries,
        )
        metrics_json = self.observability.export_metrics_json(metrics_report)
        observability_score = 100.0 if metrics_report.backup_success_rate_percent >= 99.0 else 80.0

        # End execution timer
        end_time = time.perf_counter()
        execution_duration_ms = round((end_time - start_time) * 1000.0, 2)

        # 14. Readiness Scoring Engine
        scorecard: BackupReadinessScorecard = self.scoring_engine.calculate_readiness_score(
            discovery_score=asset_discovery_score,
            classification_score=classification_score,
            strategy_score=strategy_score,
            coverage_score=coverage_score,
            retention_score=retention_score,
            lifecycle_score=lifecycle_score,
            metadata_score=metadata_score,
            observability_score=observability_score,
            policy_score=policy_score,
            execution_duration_ms=execution_duration_ms,
        )
        scorecard_json = self.scoring_engine.export_scorecard_json(scorecard)

        full_verification_data = {
            "execution_duration_ms": execution_duration_ms,
            "scorecard": scorecard_json,
            "asset_inventory": inventory_json,
            "classification_matrix": classification_json,
            "strategy_report": strategy_report_json,
            "dependency_graph": dep_graph_json,
            "coverage_report": coverage_report_json,
            "retention_report": retention_report_json,
            "lifecycle_report": lifecycle_report_json,
            "ownership_report": ownership_report_json,
            "metadata_registry": metadata_registry_json,
            "policy_validation": policy_validation_json,
            "architecture_consistency": consistency_json,
            "metrics": metrics_json,
        }

        # 13. Evidence Generation & Manifest Engine
        exported_artifacts: Dict[str, str] = {}
        if export_evidence:
            exported_artifacts = self.manifest_engine.export_evidence_artifacts(
                verification_data=full_verification_data,
                output_dir=output_dir,
            )

        return {
            "scorecard": scorecard,
            "scorecard_dict": scorecard_json,
            "verification_data": full_verification_data,
            "exported_artifacts": exported_artifacts,
            "consistency_passed": consistency_report.passed,
        }
