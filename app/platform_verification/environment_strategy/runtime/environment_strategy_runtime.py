"""
Master Unified Runtime Facade for Enterprise Verification Environment Strategy & Infrastructure.
"""
from typing import Any, Dict, List, Optional
from app.platform_verification.environment_strategy.domain.models import (
    EnvironmentClassification, EnvironmentDefinition, EnvironmentProvisioningRequest,
    EnvironmentProvisioningResult, ChaosExperimentSpec, ChaosExperimentResult,
    SecurityLabExperimentSpec, SecurityLabExperimentResult, DeploymentPromotionRecord,
    EnvironmentHealthState
)
from app.platform_verification.environment_strategy.core.registry import environment_registry
from app.platform_verification.environment_strategy.core.provisioner import environment_provisioner
from app.platform_verification.environment_strategy.core.chaos_engine import chaos_engine
from app.platform_verification.environment_strategy.core.security_lab import security_lab_runner
from app.platform_verification.environment_strategy.core.deployment import deployment_orchestrator
from app.platform_verification.environment_strategy.core.observability import environment_observability


class EnterpriseEnvironmentStrategyRuntime:
    """Master facade for managing the 8 verification environments, chaos testing, security lab, and promotion gates."""

    def provision_environment(self, classification: EnvironmentClassification) -> EnvironmentProvisioningResult:
        req = EnvironmentProvisioningRequest(environment_classification=classification)
        return environment_provisioner.provision_environment(req)

    def run_chaos_test(self, spec: ChaosExperimentSpec) -> ChaosExperimentResult:
        return chaos_engine.execute_chaos_experiment(spec)

    def run_security_scan(self, spec: SecurityLabExperimentSpec) -> SecurityLabExperimentResult:
        return security_lab_runner.execute_security_experiment(spec)

    def promote_release(
        self,
        version: str,
        from_env: EnvironmentClassification,
        to_env: EnvironmentClassification,
        metrics: Optional[Dict[str, Any]] = None
    ) -> DeploymentPromotionRecord:
        return deployment_orchestrator.promote_deployment(version=version, from_env=from_env, to_env=to_env, metrics=metrics)

    def get_all_environments(self) -> List[EnvironmentDefinition]:
        return environment_registry.list_environments()

    def get_health(self, environment_id: str) -> EnvironmentHealthState:
        return environment_observability.get_environment_health(environment_id)


environment_strategy_runtime = EnterpriseEnvironmentStrategyRuntime()
