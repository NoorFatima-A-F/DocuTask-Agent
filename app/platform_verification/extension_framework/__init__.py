"""
Enterprise Verification Extension Framework, Interfaces & Plugin System.
"""
from app.platform_verification.extension_framework.domain.models import (
    PluginMetadata, PluginManifest, PluginCategory, PluginLifecycleState,
    PluginHealthState, PluginHealthMetrics, PluginPermission, PluginSecurityContext,
    PluginExecutionContext, PluginExecutionResult, PluginDependencyDeclaration,
    SecurityClassification, PluginMarketplaceEntry, PluginQuarantineRecord, PluginEvent
)
from app.platform_verification.extension_framework.domain.interfaces import (
    BasePluginInterface, VerificationPluginInterface, ExecutionBackendPluginInterface,
    DatasetProviderPluginInterface, MetricEvaluatorPluginInterface, AIProviderPluginInterface,
    StorageProviderPluginInterface, NotificationPluginInterface, ComplianceValidatorPluginInterface,
    PluginRegistryInterface, PluginLifecycleManagerInterface, PluginExecutorInterface
)
from app.platform_verification.extension_framework.core.registry import plugin_registry, PluginRegistry
from app.platform_verification.extension_framework.core.lifecycle import plugin_lifecycle_manager, PluginLifecycleManager
from app.platform_verification.extension_framework.core.security import plugin_security_manager
from app.platform_verification.extension_framework.core.health import plugin_health_monitor
from app.platform_verification.extension_framework.core.dependencies import plugin_dependency_validator
from app.platform_verification.extension_framework.core.configuration import plugin_config_engine
from app.platform_verification.extension_framework.core.executor import plugin_executor
from app.platform_verification.extension_framework.core.marketplace import plugin_marketplace, PluginMarketplaceManager
from app.platform_verification.extension_framework.tooling.sdk import plugin_sdk, PluginDeveloperSDK
from app.platform_verification.extension_framework.runtime.extension_framework_runtime import (
    extension_framework_runtime, EnterpriseExtensionFrameworkRuntime, ExtensionFrameworkRuntime
)

__all__ = [
    "extension_framework_runtime", "EnterpriseExtensionFrameworkRuntime", "ExtensionFrameworkRuntime",
    "PluginMetadata", "PluginManifest", "PluginCategory", "PluginLifecycleState",
    "PluginHealthState", "PluginHealthMetrics", "PluginPermission", "PluginSecurityContext",
    "PluginExecutionContext", "PluginExecutionResult", "PluginDependencyDeclaration",
    "SecurityClassification", "PluginMarketplaceEntry", "PluginQuarantineRecord", "PluginEvent",
    "BasePluginInterface", "VerificationPluginInterface", "ExecutionBackendPluginInterface",
    "DatasetProviderPluginInterface", "MetricEvaluatorPluginInterface", "AIProviderPluginInterface",
    "StorageProviderPluginInterface", "NotificationPluginInterface", "ComplianceValidatorPluginInterface",
    "PluginRegistryInterface", "PluginLifecycleManagerInterface", "PluginExecutorInterface",
    "plugin_registry", "PluginRegistry", "plugin_lifecycle_manager", "PluginLifecycleManager",
    "plugin_security_manager", "plugin_health_monitor", "plugin_dependency_validator",
    "plugin_config_engine", "plugin_executor", "plugin_marketplace", "PluginMarketplaceManager",
    "plugin_sdk", "PluginDeveloperSDK"
]
