"""Enterprise Deployment Platform, Release Engineering & Infrastructure SDK.

Phase 9J Enterprise Platform for DocuTask Agent.
"""
from .artifacts.metadata import ArtifactMetadata
from .artifacts.registry import ArtifactRegistry
from .artifacts.versions import ArtifactVersion
from .cli.commands import build_parser, run_cli
from .core.controller import DeploymentController
from .core.deployment import Deployment, DeploymentStrategyType
from .core.exceptions import (
    ApprovalGateException,
    ArtifactValidationException,
    DeploymentException,
    FlagException,
    MigrationException,
    PromotionBlockedException,
    ReleaseException,
    RollbackException,
    StrategyExecutionException,
)
from .core.lifecycle import DeploymentStateEngine, DeploymentStatus, StateTransitionRecord
from .core.release import Release, ReleaseStatus
from .environments.policies import EnvironmentTierConfig, PromotionPolicy
from .environments.promotion import PromotionManager, PromotionRecord, PromotionStatus
from .environments.validation import EnvironmentValidationReport, EnvironmentValidator, ValidationCheck
from .flags.evaluation import FlagEvaluationContext, FlagEvaluator
from .flags.manager import FeatureFlag, FeatureFlagManager
from .migrations.database import MigrationManager
from .migrations.schema import MigrationPhase, SchemaMigration
from .migrations.validation import ExpandContractValidator
from .pipelines.approvals import ApprovalGate, GateApproval
from .pipelines.engine import PipelineEngine, PipelineRun, PipelineRunStatus
from .pipelines.stages import PipelineStage, PipelineStageResult, PipelineStageType
from .rollback.manager import RollbackManager, RollbackRecord
from .rollback.recovery import AutomatedRecoveryEngine, RecoveryDecision, TelemetryObservation
from .sdk.client import InfrastructureSDK
from .sdk.plugins import DeploymentPlugin, PluginManager
from .strategies.blue_green import BlueGreenPhase, BlueGreenStrategy, EnvironmentSlot
from .strategies.canary import CanaryStep, CanaryStrategy
from .strategies.rolling import RollingStepResult, RollingStrategy
from .strategies.shadow import ShadowComparison, ShadowStrategy

__all__ = [
    # Core
    "DeploymentController",
    "Deployment",
    "DeploymentStrategyType",
    "DeploymentStatus",
    "DeploymentStateEngine",
    "StateTransitionRecord",
    "Release",
    "ReleaseStatus",
    "DeploymentException",
    "ReleaseException",
    "PromotionBlockedException",
    "RollbackException",
    "MigrationException",
    "FlagException",
    "ArtifactValidationException",
    "ApprovalGateException",
    "StrategyExecutionException",
    # Artifacts
    "ArtifactMetadata",
    "ArtifactVersion",
    "ArtifactRegistry",
    # Strategies
    "RollingStrategy",
    "RollingStepResult",
    "BlueGreenStrategy",
    "BlueGreenPhase",
    "EnvironmentSlot",
    "CanaryStrategy",
    "CanaryStep",
    "ShadowStrategy",
    "ShadowComparison",
    # Environments
    "EnvironmentValidator",
    "ValidationCheck",
    "EnvironmentValidationReport",
    "PromotionPolicy",
    "EnvironmentTierConfig",
    "PromotionManager",
    "PromotionRecord",
    "PromotionStatus",
    # Pipelines
    "PipelineStage",
    "PipelineStageType",
    "PipelineStageResult",
    "ApprovalGate",
    "GateApproval",
    "PipelineEngine",
    "PipelineRun",
    "PipelineRunStatus",
    # Rollback
    "AutomatedRecoveryEngine",
    "TelemetryObservation",
    "RecoveryDecision",
    "RollbackManager",
    "RollbackRecord",
    # Migrations
    "MigrationPhase",
    "SchemaMigration",
    "ExpandContractValidator",
    "MigrationManager",
    # Feature Flags
    "FlagEvaluationContext",
    "FlagEvaluator",
    "FeatureFlag",
    "FeatureFlagManager",
    # SDK & Plugins
    "InfrastructureSDK",
    "DeploymentPlugin",
    "PluginManager",
    # CLI
    "build_parser",
    "run_cli",
]
