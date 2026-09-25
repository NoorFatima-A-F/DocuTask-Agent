"""
Interfaces and Contracts for Enterprise Verification Environment Infrastructure.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from app.platform_verification.environment_strategy.domain.models import (
    EnvironmentDefinition, EnvironmentProvisioningRequest, EnvironmentProvisioningResult,
    ChaosExperimentSpec, ChaosExperimentResult, SecurityLabExperimentSpec,
    SecurityLabExperimentResult, DeploymentPromotionRecord,
    EnvironmentHealthState, EnvironmentClassification
)


class EnvironmentProvisionerInterface(ABC):
    @abstractmethod
    def provision_environment(self, request: EnvironmentProvisioningRequest) -> EnvironmentProvisioningResult:
        pass

    @abstractmethod
    def deprovision_environment(self, environment_id: str) -> bool:
        pass

    @abstractmethod
    def reset_environment(self, environment_id: str) -> bool:
        pass

    @abstractmethod
    def clone_environment(self, source_id: str, target_classification: EnvironmentClassification) -> EnvironmentProvisioningResult:
        pass


class EnvironmentRegistryInterface(ABC):
    @abstractmethod
    def register_environment(self, definition: EnvironmentDefinition) -> None:
        pass

    @abstractmethod
    def get_environment(self, environment_id: str) -> Optional[EnvironmentDefinition]:
        pass

    @abstractmethod
    def list_environments(self, classification: Optional[EnvironmentClassification] = None) -> List[EnvironmentDefinition]:
        pass


class ChaosInjectionEngineInterface(ABC):
    @abstractmethod
    def execute_chaos_experiment(self, spec: ChaosExperimentSpec) -> ChaosExperimentResult:
        pass


class SecurityLabRunnerInterface(ABC):
    @abstractmethod
    def execute_security_experiment(self, spec: SecurityLabExperimentSpec) -> SecurityLabExperimentResult:
        pass


class DeploymentOrchestratorInterface(ABC):
    @abstractmethod
    def promote_deployment(
        self,
        version: str,
        from_env: EnvironmentClassification,
        to_env: EnvironmentClassification
    ) -> DeploymentPromotionRecord:
        pass


class EnvironmentObservabilityInterface(ABC):
    @abstractmethod
    def get_environment_health(self, environment_id: str) -> EnvironmentHealthState:
        pass

    @abstractmethod
    def get_environment_metrics(self, environment_id: str) -> Dict[str, Any]:
        pass
