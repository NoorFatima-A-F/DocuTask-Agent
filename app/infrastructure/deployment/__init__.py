"""Enterprise Deployment Platform, Release Engineering & GitOps Automation System."""

# Control Plane
from .control_plane.state import (
    DeploymentStatus,
    DeploymentStrategyType,
    DeploymentRecord,
    DeploymentHistoryTracker,
)
from .control_plane.orchestrator import DeploymentOrchestrator
from .control_plane.manager import DeploymentControlPlaneManager

# Pipelines
from .pipelines.stages import (
    StageType,
    StageStatus,
    StageExecutionResult,
    PipelineStageConfig,
)
from .pipelines.runners import StageRunner
from .pipelines.engine import PipelineRun, PipelineEngine

# Artifacts
from .artifacts.metadata import (
    ArtifactType,
    VulnerabilitySeverity,
    VulnerabilityFinding,
    SBOMComponent,
    ArtifactMetadata,
)
from .artifacts.signing import ArtifactSigner
from .artifacts.registry import ArtifactRegistry

# GitOps
from .gitops.synchronizer import GitOpsManifest, GitOpsSynchronizer
from .gitops.reconciler import DriftType, DriftItem, GitOpsReconciler
from .gitops.controller import GitOpsController

# Environments
from .environments.manager import EnvironmentType, EnvironmentConfig, EnvironmentManager
from .environments.policies import EnvironmentPolicy
from .environments.promotion import PromotionChecklist, EnvironmentPromotionManager

# Releases
from .releases.versions import ReleaseVersion
from .releases.approvals import ApprovalDecision, ReleaseApproval, ReleaseApprovalGate
from .releases.manager import ReleaseLifecycleStatus, ReleaseMetadata, ReleaseManager

# Strategies
from .strategies.rolling import RollingStrategyConfig, RollingDeploymentStrategy
from .strategies.canary import CanaryStep, CanaryDeploymentStrategy
from .strategies.blue_green import BlueGreenDeploymentStrategy
from .strategies.shadow import ShadowDeploymentStrategy

# Rollback
from .rollback.executor import (
    RollbackTriggerType,
    RollbackRequest,
    RollbackResult,
    RollbackExecutor,
)
from .rollback.recovery import PostRollbackRCAReport, RollbackRecoveryManager

# Configuration
from .configuration.templates import ConfigTemplate
from .configuration.manager import ConfigurationBundle, ConfigurationManager

# Features
from .features.flags import RolloutRule, FeatureFlag
from .features.rollout import FeatureRolloutManager

# SDK & API
from .sdk.deployment_sdk import DeploymentSDK
from .api.deployment_routes import router as deployment_router, get_deployment_sdk

__all__ = [
    # Control Plane
    "DeploymentStatus",
    "DeploymentStrategyType",
    "DeploymentRecord",
    "DeploymentHistoryTracker",
    "DeploymentOrchestrator",
    "DeploymentControlPlaneManager",
    # Pipelines
    "StageType",
    "StageStatus",
    "StageExecutionResult",
    "PipelineStageConfig",
    "StageRunner",
    "PipelineRun",
    "PipelineEngine",
    # Artifacts
    "ArtifactType",
    "VulnerabilitySeverity",
    "VulnerabilityFinding",
    "SBOMComponent",
    "ArtifactMetadata",
    "ArtifactSigner",
    "ArtifactRegistry",
    # GitOps
    "GitOpsManifest",
    "GitOpsSynchronizer",
    "DriftType",
    "DriftItem",
    "GitOpsReconciler",
    "GitOpsController",
    # Environments
    "EnvironmentType",
    "EnvironmentConfig",
    "EnvironmentManager",
    "EnvironmentPolicy",
    "PromotionChecklist",
    "EnvironmentPromotionManager",
    # Releases
    "ReleaseVersion",
    "ApprovalDecision",
    "ReleaseApproval",
    "ReleaseApprovalGate",
    "ReleaseLifecycleStatus",
    "ReleaseMetadata",
    "ReleaseManager",
    # Strategies
    "RollingStrategyConfig",
    "RollingDeploymentStrategy",
    "CanaryStep",
    "CanaryDeploymentStrategy",
    "BlueGreenDeploymentStrategy",
    "ShadowDeploymentStrategy",
    # Rollback
    "RollbackTriggerType",
    "RollbackRequest",
    "RollbackResult",
    "RollbackExecutor",
    "PostRollbackRCAReport",
    "RollbackRecoveryManager",
    # Configuration
    "ConfigTemplate",
    "ConfigurationBundle",
    "ConfigurationManager",
    # Features
    "RolloutRule",
    "FeatureFlag",
    "FeatureRolloutManager",
    # SDK & API
    "DeploymentSDK",
    "deployment_router",
    "get_deployment_sdk",
]
