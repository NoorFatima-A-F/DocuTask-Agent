"""
Enterprise Verification Configuration, Versioning & Dependency Management Subsystem.
"""
from app.platform_verification.config_versioning.runtime.config_versioning_runtime import (
    config_versioning_runtime, EnterpriseConfigVersioningRuntime
)
from app.platform_verification.config_versioning.domain.models import (
    ConfigurationSnapshot, ExecutionSnapshot, SemanticVersion, DependencyItem, DependencyCategory,
    DependencyStatus, EnvironmentTier, SBOMManifest, DriftReport, ChangeRequest, RollbackRecord,
    PromptTemplateVersion, AIModelMetadata, FeatureFlag, DatabaseMigrationRecord, SecretReference,
    SecretRotationRecord, ArtifactMetadata, ConfigDomain
)
from app.platform_verification.config_versioning.core.migrations import migration_manager
from app.platform_verification.config_versioning.core.feature_flags import feature_flag_manager
from app.platform_verification.config_versioning.core.secrets import secret_manager_service
from app.platform_verification.config_versioning.core.reproducibility import reproducibility_engine
from app.platform_verification.config_versioning.core.observability import config_observability

__all__ = [
    "config_versioning_runtime", "EnterpriseConfigVersioningRuntime",
    "ConfigurationSnapshot", "ExecutionSnapshot", "SemanticVersion", "DependencyItem",
    "DependencyCategory", "DependencyStatus", "EnvironmentTier", "SBOMManifest",
    "DriftReport", "ChangeRequest", "RollbackRecord", "PromptTemplateVersion",
    "AIModelMetadata", "FeatureFlag", "DatabaseMigrationRecord", "SecretReference",
    "SecretRotationRecord", "ArtifactMetadata", "ConfigDomain",
    "migration_manager", "feature_flag_manager", "secret_manager_service",
    "reproducibility_engine", "config_observability"
]
