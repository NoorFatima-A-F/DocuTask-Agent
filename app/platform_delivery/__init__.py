"""Platform Delivery Operating System — Phase 9J.

Enterprise Deployment Control Plane, Release Engineering, Software Supply Chain & Infrastructure Developer Platform.
"""
from .artifacts.digests import DigestCalculator
from .artifacts.metadata import OCIManifest, OCIReferrerDescriptor
from .artifacts.models import ArtifactIdentity, ArtifactQuarantineStatus, ArtifactType
from .artifacts.oci import GenericOCIRegistryAdapter, OCIRegistryAdapter
from .artifacts.registry import ArtifactRegistry
from .builds.executor import BuildPipelineEngine
from .builds.models import BuildResult, BuildStageResult, PipelineStageType, TestEvidence
from .builds.planner import BuildPlanner
from .builds.validation import BuildValidator
from .cli.main import build_parser, run_cli
from .configuration.validation import SecretReferenceResolver
from .configuration.versions import VersionedConfiguration
from .control_plane.commands import (
    ApproveDeploymentCommand,
    QuarantineArtifactCommand,
    RequestDeploymentCommand,
    RollbackDeploymentCommand,
)
from .control_plane.controller import DeploymentControlPlane, DeploymentRecord
from .control_plane.orchestrator import DeliveryOrchestrator
from .control_plane.state_machine import (
    DeploymentState,
    DeploymentStateMachine,
    ReleaseState,
    TransitionLog,
)
from .environments.models import DeploymentEnvironmentType, EnvironmentConfiguration
from .environments.policies import EnvironmentHierarchyPolicy
from .environments.promotion import PromotionManager, PromotionRecord
from .feature_flags.rollout import FeatureFlagRolloutEngine, FlagEvaluationContext
from .gitops.drift import DriftClassification, DriftDetector, DriftPolicyAction, DriftReport
from .gitops.providers.argocd import ArgoCDProvider
from .gitops.providers.base import GitOpsProvider, GitOpsSyncResult
from .gitops.providers.flux import FluxProvider
from .gitops.reconciler import GitOpsApplicationRecord, GitOpsController
from .governance.enforcement import DeploymentGovernanceEnforcer
from .governance.policies import FreezeScope, ReleaseFreezeManager
from .governance.risk import ReleaseRiskEvaluator, RiskLevel
from .migrations.coordinator import MigrationCoordinator
from .migrations.expand_contract import ExpandContractPhase, MigrationSafetyValidator, MigrationStep
from .plugins.contracts import PlatformPlugin, PluginMetadata
from .plugins.lifecycle import PluginLifecycleState
from .plugins.registry import PluginRegistry
from .plugins.sandbox import PluginSandbox, PluginSandboxPolicy
from .provenance.builder import ProvenanceManager, SLSAProvenanceStatement
from .provenance.verification import ProvenanceVerifier
from .releases.compatibility import ReleaseCompatibilityMatrix
from .releases.manager import ReleaseManager
from .releases.models import Release, ReleaseComponent, ReleaseManifest
from .rollback.policies import RollbackTriggerType
from .rollback.recovery import RollbackController, RollbackIncidentReport
from .rollout.analysis import CanaryAnalysisEngine, QualityGatePolicy, RolloutDecision
from .rollout.controller import ProgressiveDeliveryController
from .sbom.generator import SBOMComponent, SBOMDocument, SBOMFormat, SBOMManager
from .sbom.policy import SBOMPolicyEvaluator
from .sdk.client import InfrastructureSDK
from .signing.policies import SupplyChainPolicyEnforcer, SupplyChainVerificationReport
from .signing.sigstore_adapter import CosignSignatureBundle, SigningMechanism, SigstoreCosignAdapter
from .strategies.blue_green import BlueGreenStrategy, EnvironmentSlot
from .strategies.canary import CanaryStepEvaluation, CanaryStrategy
from .strategies.rolling import RollingStep, RollingStrategy
from .strategies.shadow import ShadowStrategy, ShadowTrace
from .telemetry.metrics import DeliveryMetricsCollector, DORAMetrics

__all__ = [
    # Control Plane
    "DeploymentState",
    "ReleaseState",
    "TransitionLog",
    "DeploymentStateMachine",
    "DeploymentRecord",
    "DeploymentControlPlane",
    "DeliveryOrchestrator",
    "RequestDeploymentCommand",
    "ApproveDeploymentCommand",
    "RollbackDeploymentCommand",
    "QuarantineArtifactCommand",
    # Builds & Evidence
    "PipelineStageType",
    "TestEvidence",
    "BuildStageResult",
    "BuildResult",
    "BuildPlanner",
    "BuildPipelineEngine",
    "BuildValidator",
    # Artifacts & OCI
    "ArtifactType",
    "ArtifactQuarantineStatus",
    "ArtifactIdentity",
    "DigestCalculator",
    "OCIReferrerDescriptor",
    "OCIManifest",
    "OCIRegistryAdapter",
    "GenericOCIRegistryAdapter",
    "ArtifactRegistry",
    # Supply Chain
    "SBOMFormat",
    "SBOMComponent",
    "SBOMDocument",
    "SBOMManager",
    "SBOMPolicyEvaluator",
    "SLSAProvenanceStatement",
    "ProvenanceManager",
    "ProvenanceVerifier",
    "SigningMechanism",
    "CosignSignatureBundle",
    "SigstoreCosignAdapter",
    "SupplyChainVerificationReport",
    "SupplyChainPolicyEnforcer",
    # Releases
    "ReleaseComponent",
    "ReleaseManifest",
    "Release",
    "ReleaseCompatibilityMatrix",
    "ReleaseManager",
    # Environments
    "DeploymentEnvironmentType",
    "EnvironmentConfiguration",
    "EnvironmentHierarchyPolicy",
    "PromotionRecord",
    "PromotionManager",
    # GitOps
    "DriftClassification",
    "DriftPolicyAction",
    "DriftReport",
    "DriftDetector",
    "GitOpsSyncResult",
    "GitOpsProvider",
    "ArgoCDProvider",
    "FluxProvider",
    "GitOpsApplicationRecord",
    "GitOpsController",
    # Strategies & Progressive Delivery
    "RollingStep",
    "RollingStrategy",
    "EnvironmentSlot",
    "BlueGreenStrategy",
    "CanaryStepEvaluation",
    "CanaryStrategy",
    "ShadowTrace",
    "ShadowStrategy",
    "RolloutDecision",
    "QualityGatePolicy",
    "CanaryAnalysisEngine",
    "ProgressiveDeliveryController",
    # Rollback
    "RollbackTriggerType",
    "RollbackIncidentReport",
    "RollbackController",
    # Migrations & Config & Flags
    "ExpandContractPhase",
    "MigrationStep",
    "MigrationSafetyValidator",
    "MigrationCoordinator",
    "VersionedConfiguration",
    "SecretReferenceResolver",
    "FlagEvaluationContext",
    "FeatureFlagRolloutEngine",
    # Governance
    "RiskLevel",
    "ReleaseRiskEvaluator",
    "FreezeScope",
    "ReleaseFreezeManager",
    "DeploymentGovernanceEnforcer",
    # Plugins
    "PluginMetadata",
    "PlatformPlugin",
    "PluginLifecycleState",
    "PluginSandboxPolicy",
    "PluginSandbox",
    "PluginRegistry",
    # SDK & CLI & Telemetry
    "InfrastructureSDK",
    "build_parser",
    "run_cli",
    "DORAMetrics",
    "DeliveryMetricsCollector",
]
