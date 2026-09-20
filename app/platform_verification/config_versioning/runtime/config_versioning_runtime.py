"""
Master Unified Runtime Facade for Enterprise Configuration, Versioning & Dependency Management.
"""
from typing import Any, Dict, List, Optional
from app.platform_verification.config_versioning.domain.models import (
    ConfigurationSnapshot, ExecutionSnapshot, SemanticVersion, DependencyItem,
    EnvironmentTier, SBOMManifest, DriftReport, ChangeRequest, RollbackRecord,
    PromptTemplateVersion, AIModelMetadata, FeatureFlag, DatabaseMigrationRecord,
    SecretReference, SecretRotationRecord
)
from app.platform_verification.config_versioning.core.registry import configuration_registry
from app.platform_verification.config_versioning.core.resolver import configuration_resolver
from app.platform_verification.config_versioning.core.validator import configuration_validator
from app.platform_verification.config_versioning.core.snapshot_manager import snapshot_manager
from app.platform_verification.config_versioning.core.diff_engine import configuration_diff_engine
from app.platform_verification.config_versioning.core.dependency_registry import dependency_registry
from app.platform_verification.config_versioning.core.sbom_generator import sbom_generator
from app.platform_verification.config_versioning.core.ai_artifacts import ai_artifact_manager
from app.platform_verification.config_versioning.core.fingerprint import environment_fingerprinter
from app.platform_verification.config_versioning.core.drift_detector import drift_detector
from app.platform_verification.config_versioning.core.change_tracker import change_tracker
from app.platform_verification.config_versioning.core.migrations import migration_manager
from app.platform_verification.config_versioning.core.feature_flags import feature_flag_manager
from app.platform_verification.config_versioning.core.secrets import secret_manager_service
from app.platform_verification.config_versioning.core.reproducibility import reproducibility_engine
from app.platform_verification.config_versioning.core.observability import config_observability


class EnterpriseConfigVersioningRuntime:
    """Unified Facade for Configuration, Versioning, and Dependency Governance."""

    def resolve_and_snapshot(
        self,
        environment: EnvironmentTier = EnvironmentTier.INTEGRATION,
        module_name: Optional[str] = None,
        overrides: Optional[Dict[str, Any]] = None,
        creator: str = "Enterprise Configuration Resolver"
    ) -> ConfigurationSnapshot:
        resolved = configuration_resolver.resolve(
            environment=environment,
            module_name=module_name,
            experiment_override=overrides
        )
        fp = environment_fingerprinter.capture_fingerprint(tier=environment)
        snapshot = snapshot_manager.create_snapshot(
            resolved_config=resolved,
            environment=environment,
            environment_fingerprint=fp,
            creator=creator
        )
        config_observability.record_event(
            event_type="CONFIG_SNAPSHOT_CREATED",
            actor=creator,
            environment=environment.value,
            details={"snapshot_id": snapshot.snapshot_id, "hash": snapshot.configuration_hash}
        )
        return snapshot

    def create_execution_snapshot(
        self,
        verification_id: str,
        code_commit_sha: str,
        config_snapshot: ConfigurationSnapshot,
        dataset_id: str,
        dataset_version: str,
        dataset_hash: str,
        model_identifier: str,
        model_version: str,
        prompt_version: PromptTemplateVersion,
        infrastructure_version: str = "k8s-cluster-v2"
    ) -> ExecutionSnapshot:
        sbom = sbom_generator.generate_cyclonedx_sbom()
        exec_snap = reproducibility_engine.capture_execution_snapshot(
            verification_id=verification_id,
            code_commit_sha=code_commit_sha,
            configuration_snapshot_id=config_snapshot.snapshot_id,
            configuration_hash=config_snapshot.configuration_hash,
            dataset_id=dataset_id,
            dataset_version=dataset_version,
            dataset_hash=dataset_hash,
            model_identifier=model_identifier,
            model_version=model_version,
            prompt_template_id=prompt_version.template_id,
            prompt_version=prompt_version.semantic_version,
            prompt_hash=prompt_version.prompt_hash,
            dependency_lock_hash=sbom.sha256_bom_hash,
            sbom_manifest_id=sbom.sbom_id,
            environment_tier=config_snapshot.environment,
            infrastructure_version=infrastructure_version
        )
        return exec_snap

    def evaluate_feature_flag(
        self,
        flag_key: str,
        environment: EnvironmentTier = EnvironmentTier.PRODUCTION,
        tenant_id: Optional[str] = None
    ) -> bool:
        return feature_flag_manager.is_flag_active(flag_key=flag_key, environment=environment, tenant_id=tenant_id)

    def generate_sbom(self) -> SBOMManifest:
        return sbom_generator.generate_cyclonedx_sbom()


config_versioning_runtime = EnterpriseConfigVersioningRuntime()
