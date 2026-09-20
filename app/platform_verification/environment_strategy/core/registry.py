"""
Environment Metadata Registry.
Maintains live catalog of all 8 enterprise verification environments.
"""
import hashlib
from typing import Dict, List, Optional
from app.platform_verification.environment_strategy.domain.models import (
    EnvironmentDefinition, EnvironmentClassification, EnvironmentSecurityLevel,
    DataClassificationPolicy, DeploymentStrategyType, EnvironmentMetadataRecord,
    EnvironmentHealthState
)
from app.platform_verification.environment_strategy.domain.interfaces import EnvironmentRegistryInterface


class EnvironmentMetadataRegistry(EnvironmentRegistryInterface):
    def __init__(self):
        self._definitions: Dict[str, EnvironmentDefinition] = {}
        self._metadata_records: Dict[str, EnvironmentMetadataRecord] = {}
        self._bootstrap_canonical_environments()

    def _bootstrap_canonical_environments(self):
        canonical = [
            EnvironmentDefinition(
                environment_id="env_dev_01",
                name="Local / Development Verification Environment",
                classification=EnvironmentClassification.DEVELOPMENT,
                purpose="Rapid local development, debugging, and mock-based unit execution",
                security_level=EnvironmentSecurityLevel.LOCAL_PERMISSIVE,
                data_policy=DataClassificationPolicy.SYNTHETIC_ONLY,
                deployment_strategy=DeploymentStrategyType.RECREATE,
                min_cpu_cores=2,
                min_memory_gb=8.0
            ),
            EnvironmentDefinition(
                environment_id="env_int_01",
                name="Integration Verification Environment",
                classification=EnvironmentClassification.INTEGRATION,
                purpose="Component interaction, persistence, and event bus verification with live dependencies",
                security_level=EnvironmentSecurityLevel.ISOLATED_TEST,
                data_policy=DataClassificationPolicy.BENCHMARK_CURATED,
                deployment_strategy=DeploymentStrategyType.ROLLING,
                min_cpu_cores=4,
                min_memory_gb=16.0
            ),
            EnvironmentDefinition(
                environment_id="env_stg_01",
                name="Staging Production-Parity Environment",
                classification=EnvironmentClassification.STAGING,
                purpose="Production simulation, release qualification, load and performance verification",
                security_level=EnvironmentSecurityLevel.STAGING_CONTROLLED,
                data_policy=DataClassificationPolicy.REGRESSION_HISTORICAL,
                deployment_strategy=DeploymentStrategyType.BLUE_GREEN,
                min_cpu_cores=8,
                min_memory_gb=32.0
            ),
            EnvironmentDefinition(
                environment_id="env_shd_01",
                name="Production Shadow Verification Environment",
                classification=EnvironmentClassification.PRODUCTION_SHADOW,
                purpose="Replay real production traffic in read-only mode for zero-impact behavioral validation",
                security_level=EnvironmentSecurityLevel.SHADOW_ANONYMIZED,
                data_policy=DataClassificationPolicy.PRODUCTION_ANONYMIZED,
                deployment_strategy=DeploymentStrategyType.BLUE_GREEN,
                min_cpu_cores=8,
                min_memory_gb=32.0
            ),
            EnvironmentDefinition(
                environment_id="env_prd_01",
                name="Live Production Environment",
                classification=EnvironmentClassification.PRODUCTION,
                purpose="Live operational workload execution with strict change control and continuous verification",
                security_level=EnvironmentSecurityLevel.PRODUCTION_HARDENED,
                data_policy=DataClassificationPolicy.PRODUCTION_LIVE,
                deployment_strategy=DeploymentStrategyType.CANARY,
                min_cpu_cores=16,
                min_memory_gb=64.0
            ),
            EnvironmentDefinition(
                environment_id="env_chs_01",
                name="Chaos Engineering Lab Environment",
                classification=EnvironmentClassification.CHAOS,
                purpose="Controlled failure injection, network partition, and resiliency testing",
                security_level=EnvironmentSecurityLevel.ISOLATED_TEST,
                data_policy=DataClassificationPolicy.SYNTHETIC_ONLY,
                deployment_strategy=DeploymentStrategyType.RECREATE,
                min_cpu_cores=4,
                min_memory_gb=16.0
            ),
            EnvironmentDefinition(
                environment_id="env_sec_01",
                name="Security & Adversarial Testing Lab",
                classification=EnvironmentClassification.SECURITY_LAB,
                purpose="Dedicated adversarial attacks, prompt injection, jailbreaking, and vulnerability fuzzing",
                security_level=EnvironmentSecurityLevel.ADVERSARIAL_SANDBOX,
                data_policy=DataClassificationPolicy.SYNTHETIC_ONLY,
                deployment_strategy=DeploymentStrategyType.RECREATE,
                min_cpu_cores=4,
                min_memory_gb=16.0
            ),
            EnvironmentDefinition(
                environment_id="env_res_01",
                name="Research & AI Experimentation Sandbox",
                classification=EnvironmentClassification.RESEARCH,
                purpose="Experimental AI models, exploratory prompt architectures, and cutting-edge verifiers",
                security_level=EnvironmentSecurityLevel.ISOLATED_TEST,
                data_policy=DataClassificationPolicy.SYNTHETIC_ONLY,
                deployment_strategy=DeploymentStrategyType.RECREATE,
                min_cpu_cores=4,
                min_memory_gb=16.0
            )
        ]
        for env in canonical:
            self.register_environment(env)

    def register_environment(self, definition: EnvironmentDefinition) -> None:
        self._definitions[definition.environment_id] = definition
        self._metadata_records[definition.environment_id] = EnvironmentMetadataRecord(
            environment_id=definition.environment_id,
            classification=definition.classification,
            configuration_hash=hashlib.sha256(f"cfg_{definition.environment_id}".encode("utf-8")).hexdigest(),
            infrastructure_version="tf-v1.8-k8s-1.30",
            deployment_version="v2.4.0",
            health_state=EnvironmentHealthState.HEALTHY
        )

    def get_environment(self, environment_id: str) -> Optional[EnvironmentDefinition]:
        return self._definitions.get(environment_id)

    def get_by_classification(self, classification: EnvironmentClassification) -> Optional[EnvironmentDefinition]:
        for env in self._definitions.values():
            if env.classification == classification:
                return env
        return None

    def list_environments(self, classification: Optional[EnvironmentClassification] = None) -> List[EnvironmentDefinition]:
        envs = list(self._definitions.values())
        if classification:
            envs = [e for e in envs if e.classification == classification]
        return envs

    def get_metadata(self, environment_id: str) -> Optional[EnvironmentMetadataRecord]:
        return self._metadata_records.get(environment_id)


environment_registry = EnvironmentMetadataRegistry()
