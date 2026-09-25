"""
Master Unified Runtime Facade for Enterprise Extension Framework & Plugin Architecture.
"""
from typing import Any, Dict, List, Optional
from app.platform_verification.extension_framework.domain.models import (
    PluginMetadata, PluginExecutionContext, PluginExecutionResult, PluginHealthMetrics,
    PluginLifecycleState, PluginSecurityContext, PluginCategory
)
from app.platform_verification.extension_framework.domain.interfaces import (
    BasePluginInterface
)
from app.platform_verification.extension_framework.core.registry import plugin_registry
from app.platform_verification.extension_framework.core.lifecycle import plugin_lifecycle_manager
from app.platform_verification.extension_framework.core.health import plugin_health_monitor
from app.platform_verification.extension_framework.core.executor import plugin_executor
from app.platform_verification.extension_framework.core.marketplace import plugin_marketplace
from app.platform_verification.extension_framework.plugins.ocr_plugin import OCRVerificationPlugin
from app.platform_verification.extension_framework.plugins.ai_extraction_plugin import AIExtractionEvaluationPlugin
from app.platform_verification.extension_framework.plugins.rag_eval_plugin import RAGEvaluationPlugin
from app.platform_verification.extension_framework.plugins.prompt_injection_plugin import PromptInjectionSecurityPlugin
from app.platform_verification.extension_framework.plugins.kubernetes_executor_plugin import KubernetesExecutorPlugin
from app.platform_verification.extension_framework.plugins.synthetic_dataset_plugin import SyntheticDatasetPlugin
from app.platform_verification.extension_framework.plugins.composite_metric_plugin import CompositeMetricEvaluatorPlugin
from app.platform_verification.extension_framework.plugins.gemini_ai_plugin import GeminiAIProviderPlugin
from app.platform_verification.extension_framework.plugins.local_cas_storage_plugin import LocalCASStoragePlugin
from app.platform_verification.extension_framework.plugins.webhook_notification_plugin import WebhookNotificationPlugin


class EnterpriseExtensionFrameworkRuntime:
    """Unified Facade for Enterprise Extension & Plugin Platform."""

    def __init__(self):
        self._bootstrap_reference_plugins()

    def _bootstrap_reference_plugins(self):
        plugins = [
            OCRVerificationPlugin(),
            AIExtractionEvaluationPlugin(),
            RAGEvaluationPlugin(),
            PromptInjectionSecurityPlugin(),
            KubernetesExecutorPlugin(),
            SyntheticDatasetPlugin(),
            CompositeMetricEvaluatorPlugin(),
            GeminiAIProviderPlugin(),
            LocalCASStoragePlugin(),
            WebhookNotificationPlugin(),
        ]
        for p in plugins:
            plugin_registry.register_plugin(p)
            plugin_lifecycle_manager.set_initial_state(p.metadata.plugin_id, PluginLifecycleState.READY)
            plugin_marketplace.publish_plugin(
                plugin_id=p.metadata.plugin_id,
                version=p.metadata.version,
                category=p.metadata.category,
                author=p.metadata.author,
                certification_level=p.metadata.security_classification
            )

    def execute_verification_plugin(
        self,
        plugin_id: str,
        verification_id: str,
        dataset_ref: Optional[Dict[str, Any]] = None,
        config_snapshot: Optional[Dict[str, Any]] = None,
        security_context: Optional[PluginSecurityContext] = None
    ) -> PluginExecutionResult:
        plugin = plugin_registry.get_plugin(plugin_id)
        if not plugin:
            raise KeyError(f"Plugin '{plugin_id}' not found in registry")

        ctx = PluginExecutionContext(
            verification_id=verification_id,
            dataset_reference=dataset_ref or {},
            configuration_snapshot=config_snapshot or {},
            security_context=security_context or PluginSecurityContext(
                caller_identity="ExtensionFrameworkRuntime",
                permissions=plugin.metadata.granted_permissions
            )
        )
        return plugin_executor.execute_plugin(plugin_id, ctx)

    def register_custom_plugin(self, plugin: BasePluginInterface) -> PluginMetadata:
        meta = plugin_registry.register_plugin(plugin)
        plugin_lifecycle_manager.set_initial_state(meta.plugin_id, PluginLifecycleState.READY)
        return meta

    def get_plugin_health(self, plugin_id: str) -> PluginHealthMetrics:
        return plugin_health_monitor.get_health(plugin_id)

    def list_plugins_by_category(self, category: PluginCategory) -> List[PluginMetadata]:
        all_plugins = plugin_registry.list_plugins()
        return [p for p in all_plugins if getattr(p, "category", None) == category]


ExtensionFrameworkRuntime = EnterpriseExtensionFrameworkRuntime
extension_framework_runtime = EnterpriseExtensionFrameworkRuntime()
