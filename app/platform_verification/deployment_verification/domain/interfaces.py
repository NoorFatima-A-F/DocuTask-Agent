"""
Abstract interfaces for Part 3D: Enterprise Deployment & Environment Verification Framework.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from app.platform_verification.deployment_verification.domain.models import (
    BuildReproducibilityReport,
    DependencyLockReport,
    EnvironmentDriftReport,
    IacValidationReport,
    DeploymentAutomationReport,
    ReleaseStrategyReport,
    RollbackVerificationReport,
    SecretDeploymentReport,
    ZeroDowntimeReport,
    DeploymentCertificationReport,
    DeploymentVerificationEvidencePackage,
)


class IBuildPipelineValidator(ABC):
    @abstractmethod
    def validate_build_pipeline(self, build_meta: Dict[str, Any]) -> (BuildReproducibilityReport, DependencyLockReport):
        """Verifies build determinism and lock file dependency pinning."""
        pass


class IEnvironmentParityValidator(ABC):
    @abstractmethod
    def validate_parity(self, env_configs: Dict[str, Dict[str, Any]]) -> EnvironmentDriftReport:
        """Audits environment configs for drift and missing variables."""
        pass


class IIacValidator(ABC):
    @abstractmethod
    def validate_iac(self, iac_manifests: List[Dict[str, Any]]) -> IacValidationReport:
        """Validates IaC definitions and tests environment recreation idempotency."""
        pass


class IDeploymentAutomationValidator(ABC):
    @abstractmethod
    def validate_automation(self, pipeline_steps: List[Dict[str, Any]]) -> DeploymentAutomationReport:
        """Verifies 100% automated CI/CD steps and rejects manual operations."""
        pass


class IRolloutRollbackTester(ABC):
    __test__ = False
    @abstractmethod
    def test_rollout_and_rollback(self, rollout_config: Dict[str, Any]) -> (ReleaseStrategyReport, RollbackVerificationReport, ZeroDowntimeReport):
        """Tests rolling/canary rollouts, automated rollback triggers, and zero downtime availability."""
        pass


class ISecretConfigurationAuditor(ABC):
    @abstractmethod
    def audit_secrets(self, scan_targets: List[str]) -> SecretDeploymentReport:
        """Scans code and artifacts for leaked secrets and validates runtime injection."""
        pass


class IDeploymentScoringEngine(ABC):
    @abstractmethod
    def calculate_scorecard(
        self,
        build_rep: BuildReproducibilityReport,
        lock_rep: DependencyLockReport,
        drift_rep: EnvironmentDriftReport,
        auto_rep: DeploymentAutomationReport,
        sec_rep: SecretDeploymentReport,
        release_rep: ReleaseStrategyReport,
        rollback_rep: RollbackVerificationReport,
        zero_rep: ZeroDowntimeReport,
    ) -> DeploymentCertificationReport:
        """Computes weighted composite score and assigns certification tier."""
        pass


class IDeploymentEvidenceStore(ABC):
    @abstractmethod
    def seal_and_store_evidence(self, package: DeploymentVerificationEvidencePackage) -> str:
        """Persists and seals deployment verification evidence package with SHA-256."""
        pass

    @abstractmethod
    def retrieve_evidence(self, package_id: str) -> Optional[DeploymentVerificationEvidencePackage]:
        """Retrieves stored evidence package."""
        pass
