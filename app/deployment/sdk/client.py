"""Enterprise Infrastructure & Deployment SDK."""
from typing import Any, Dict, List, Optional
from ..artifacts.metadata import ArtifactMetadata
from ..artifacts.registry import ArtifactRegistry
from ..core.controller import DeploymentController
from ..core.deployment import Deployment, DeploymentStrategyType
from ..core.release import Release
from ..environments.promotion import PromotionManager, PromotionRecord
from ..flags.evaluation import FlagEvaluationContext
from ..flags.manager import FeatureFlag, FeatureFlagManager
from ..migrations.database import MigrationManager
from ..migrations.schema import SchemaMigration
from ..pipelines.engine import PipelineEngine, PipelineRun
from ..rollback.manager import RollbackManager, RollbackRecord
from .plugins import DeploymentPlugin, PluginManager


class InfrastructureSDK:
    """Unified developer and platform client for managing deployment operations."""

    def __init__(
        self,
        controller: Optional[DeploymentController] = None,
        artifacts: Optional[ArtifactRegistry] = None,
        promotions: Optional[PromotionManager] = None,
        rollback_manager: Optional[RollbackManager] = None,
        migrations: Optional[MigrationManager] = None,
        flags: Optional[FeatureFlagManager] = None,
        plugins: Optional[PluginManager] = None,
    ):
        self.controller = controller or DeploymentController()
        self.artifacts = artifacts or ArtifactRegistry()
        self.promotions = promotions or PromotionManager()
        self.rollback_mgr = rollback_manager or RollbackManager(controller=self.controller)
        self.migrations = migrations or MigrationManager()
        self.flags = flags or FeatureFlagManager()
        self.plugins = plugins or PluginManager()

    # --- Release Operations ---
    def create_release(
        self,
        version: str,
        name: str,
        commit_sha: str,
        artifact_ids: Optional[List[str]] = None,
        changelog: str = "",
        auto_publish: bool = True,
    ) -> Release:
        """Creates, binds artifacts, and optionally publishes a new release package."""
        rel = self.controller.create_release(
            version=version,
            name=name,
            commit_sha=commit_sha,
            artifact_ids=artifact_ids,
            changelog=changelog,
        )
        if auto_publish:
            rel.publish()
        return rel

    # --- Deployment Operations ---
    def deploy(
        self,
        release_id: str,
        target_environment: str,
        strategy: DeploymentStrategyType = DeploymentStrategyType.ROLLING,
        replicas: int = 3,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Deployment:
        """Executes deployment with plugin lifecycle hooks."""
        context = {
            "release_id": release_id,
            "environment": target_environment,
            "strategy": strategy.value,
            "replicas": replicas,
            "metadata": metadata or {},
        }

        # Pre-deploy plugin hook
        if not self.plugins.run_pre_deploy(context):
            raise RuntimeError("Deployment aborted by pre_deploy plugin hook")

        dep = self.controller.create_deployment(
            release_id=release_id,
            target_environment=target_environment,
            strategy=strategy,
            replicas=replicas,
            metadata=metadata,
        )
        self.controller.execute_deployment(dep.deployment_id)

        context["deployment_id"] = dep.deployment_id
        self.plugins.run_post_deploy(context)
        return dep

    # --- Rollback Operations ---
    def rollback(
        self,
        deployment_id: str,
        target_release_id: Optional[str] = None,
        reason: str = "SDK triggered rollback",
    ) -> RollbackRecord:
        """Executes rollback with plugin lifecycle hooks."""
        context = {"deployment_id": deployment_id, "reason": reason}
        if not self.plugins.run_pre_rollback(context):
            raise RuntimeError("Rollback aborted by pre_rollback plugin hook")

        rec = self.rollback_mgr.execute_rollback(
            deployment_id=deployment_id,
            target_release_id=target_release_id,
            reason=reason,
            initiated_by="sdk",
        )
        self.plugins.run_post_rollback(context)
        return rec

    # --- Promotion Operations ---
    def request_and_promote(
        self,
        release_id: str,
        target_env: str,
        source_env: Optional[str] = None,
        approved_roles: Optional[List[str]] = None,
        strategy: DeploymentStrategyType = DeploymentStrategyType.ROLLING,
    ) -> Deployment:
        """Requests, approves, and executes promotion in a single workflow."""
        record = self.promotions.request_promotion(
            release_id=release_id,
            target_env=target_env,
            source_env=source_env,
        )
        for role in (approved_roles or []):
            self.promotions.approve_promotion(
                promotion_id=record.promotion_id,
                role=role,
                approver_identity="sdk_operator",
            )
        return self.promotions.execute_promotion(
            promotion_id=record.promotion_id,
            controller=self.controller,
            strategy=strategy,
        )

    # --- Feature Flag Operations ---
    def is_feature_enabled(
        self,
        key: str,
        tenant_id: Optional[str] = None,
        user_id: Optional[str] = None,
        environment: str = "prod",
    ) -> bool:
        """Evaluates a feature flag for given runtime context."""
        ctx = FlagEvaluationContext(
            tenant_id=tenant_id,
            user_id=user_id,
            environment=environment,
        )
        return self.flags.is_enabled(key, ctx)

    # --- Database Migrations ---
    def apply_migration(self, target: str, migration: SchemaMigration) -> SchemaMigration:
        """Registers and applies a schema migration."""
        if not self.migrations.get_migration(migration.migration_id):
            self.migrations.register_migration(migration)
        return self.migrations.apply_migration(target, migration.migration_id)

    # --- Artifacts ---
    def register_artifact(
        self,
        name: str,
        version: str,
        data: bytes,
        sbom: Optional[List[Dict[str, str]]] = None,
    ) -> ArtifactMetadata:
        """Registers and signs a new artifact package."""
        return self.artifacts.register_artifact(
            name=name,
            version=version,
            data=data,
            sbom_components=sbom,
        )
