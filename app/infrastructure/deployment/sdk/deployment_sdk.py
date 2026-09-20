"""Unified Deployment SDK providing high-level programmatic release automation capabilities."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional
import uuid

from ..control_plane.state import (
    DeploymentStatus,
    DeploymentStrategyType,
    DeploymentRecord,
    DeploymentHistoryTracker,
)
from ..control_plane.orchestrator import DeploymentOrchestrator
from ..control_plane.manager import DeploymentControlPlaneManager
from ..pipelines.stages import StageType, StageStatus, PipelineStageConfig
from ..pipelines.runners import StageRunner
from ..pipelines.engine import PipelineRun, PipelineEngine
from ..artifacts.metadata import (
    ArtifactType,
    VulnerabilitySeverity,
    VulnerabilityFinding,
    SBOMComponent,
    ArtifactMetadata,
)
from ..artifacts.signing import ArtifactSigner
from ..artifacts.registry import ArtifactRegistry
from ..gitops.synchronizer import GitOpsManifest, GitOpsSynchronizer
from ..gitops.reconciler import DriftType, DriftItem, GitOpsReconciler
from ..gitops.controller import GitOpsController
from ..environments.manager import EnvironmentType, EnvironmentConfig, EnvironmentManager
from ..environments.policies import EnvironmentPolicy
from ..environments.promotion import PromotionChecklist, EnvironmentPromotionManager
from ..releases.versions import ReleaseVersion
from ..releases.approvals import ApprovalDecision, ReleaseApproval, ReleaseApprovalGate
from ..releases.manager import ReleaseLifecycleStatus, ReleaseMetadata, ReleaseManager
from ..strategies.rolling import RollingDeploymentStrategy
from ..strategies.canary import CanaryDeploymentStrategy
from ..strategies.blue_green import BlueGreenDeploymentStrategy
from ..strategies.shadow import ShadowDeploymentStrategy
from ..rollback.executor import RollbackTriggerType, RollbackRequest, RollbackResult, RollbackExecutor
from ..rollback.recovery import PostRollbackRCAReport, RollbackRecoveryManager
from ..configuration.templates import ConfigTemplate
from ..configuration.manager import ConfigurationBundle, ConfigurationManager
from ..features.flags import RolloutRule, FeatureFlag
from ..features.rollout import FeatureRolloutManager


class DeploymentSDK:
    """Central programmatic façade for enterprise deployment, release engineering, and GitOps."""

    def __init__(self) -> None:
        # 1. State & Control Plane
        self.history_tracker = DeploymentHistoryTracker()
        self.orchestrator = DeploymentOrchestrator()
        self.control_plane = DeploymentControlPlaneManager(
            history_tracker=self.history_tracker,
            orchestrator=self.orchestrator,
        )

        # 2. CI/CD Pipelines
        self.stage_runner = StageRunner()
        self.pipeline_engine = PipelineEngine(runner=self.stage_runner)

        # 3. Artifacts & Supply Chain
        self.artifact_signer = ArtifactSigner()
        self.artifact_registry = ArtifactRegistry(signer=self.artifact_signer)

        # 4. GitOps Engine
        self.gitops_synchronizer = GitOpsSynchronizer()
        self.gitops_reconciler = GitOpsReconciler(self.gitops_synchronizer)
        self.gitops_controller = GitOpsController(
            synchronizer=self.gitops_synchronizer,
            reconciler=self.gitops_reconciler,
        )

        # 5. Environments & Promotion
        self.environment_manager = EnvironmentManager()
        self.promotion_manager = EnvironmentPromotionManager(
            env_manager=self.environment_manager,
            artifact_registry=self.artifact_registry,
        )

        # 6. Releases
        self.approval_gate = ReleaseApprovalGate()
        self.release_manager = ReleaseManager(approval_gate=self.approval_gate)

        # 7. Strategies
        self.rolling_strategy = RollingDeploymentStrategy()
        self.canary_strategy = CanaryDeploymentStrategy()
        self.blue_green_strategy = BlueGreenDeploymentStrategy()
        self.shadow_strategy = ShadowDeploymentStrategy()

        # 8. Rollback & Recovery
        self.rollback_executor = RollbackExecutor()
        self.rollback_recovery = RollbackRecoveryManager(executor=self.rollback_executor)

        # 9. Configuration & Features
        self.config_manager = ConfigurationManager()
        self.feature_manager = FeatureRolloutManager()

    # --- Release API ---
    def create_release(
        self,
        version: str,
        components_changed: List[str],
        artifact_ids: List[str],
        changelog: str = "",
        target_environments: Optional[List[str]] = None,
    ) -> ReleaseMetadata:
        """Create and register a release."""
        return self.release_manager.create_release(
            version=version,
            components_changed=components_changed,
            artifact_ids=artifact_ids,
            changelog=changelog,
            target_environments=target_environments,
        )

    # --- Deployment API ---
    def deploy(
        self,
        service_name: str,
        target_environment: str,
        target_version: str,
        release_id: Optional[str] = None,
        strategy: DeploymentStrategyType = DeploymentStrategyType.ROLLING,
        health_checker: Optional[Callable[[], bool]] = None,
    ) -> DeploymentRecord:
        """Trigger a governed deployment."""
        return self.control_plane.trigger_deployment(
            service_name=service_name,
            target_environment=target_environment,
            target_version=target_version,
            release_id=release_id,
            strategy=strategy,
            health_checker=health_checker,
        )

    def rollback(
        self,
        deployment_id: str,
        reason: str = "Operator initiated rollback",
        trigger_type: RollbackTriggerType = RollbackTriggerType.MANUAL,
    ) -> PostRollbackRCAReport:
        """Rollback an active or completed deployment."""
        dep = self.control_plane.get_deployment(deployment_id)
        if not dep:
            raise ValueError(f"Deployment '{deployment_id}' not found")

        return self.rollback_recovery.trigger_and_recover(
            deployment=dep,
            reason=reason,
            trigger_type=trigger_type,
        )

    def promote(
        self,
        from_env: str,
        to_env: str,
        release_id: str,
        artifact_id: str,
        approvers: Optional[List[str]] = None,
    ) -> PromotionChecklist:
        """Promote an artifact to the next environment."""
        art = self.artifact_registry.get_artifact(artifact_id)
        if not art:
            raise ValueError(f"Artifact '{artifact_id}' not found")

        return self.promotion_manager.evaluate_promotion(
            from_env=from_env,
            to_env=to_env,
            release_id=release_id,
            artifact=art,
            approvers=approvers,
        )

    def verify(self, deployment_id: str) -> bool:
        """Verify the health status of a deployment."""
        dep = self.control_plane.get_deployment(deployment_id)
        return dep is not None and dep.status == DeploymentStatus.COMPLETED

    def get_status(self, deployment_id: str) -> Optional[DeploymentRecord]:
        """Fetch deployment status."""
        return self.control_plane.get_deployment(deployment_id)

    def enable_feature(self, flag_key: str, percentage: float = 100.0) -> FeatureFlag:
        """Create or enable a feature flag."""
        flag = self.feature_manager.create_flag(flag_key, name=flag_key, default_enabled=True)
        flag.rules = [RolloutRule(percentage=percentage)]
        return flag

    def run_pipeline(
        self,
        pipeline_name: str,
        commit_sha: str,
        stages: Optional[List[PipelineStageConfig]] = None,
    ) -> PipelineRun:
        """Execute a CI/CD pipeline."""
        pipeline_stages = stages or self.pipeline_engine.build_standard_ci_pipeline(pipeline_name)
        return self.pipeline_engine.execute_pipeline(
            pipeline_name=pipeline_name,
            commit_sha=commit_sha,
            stages=pipeline_stages,
        )
