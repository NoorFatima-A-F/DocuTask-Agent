"""
Plugin Developer SDK and CLI Generator Tooling.
"""
from typing import Any, Dict, List, Optional, Tuple
from app.platform_verification.extension_framework.domain.models import (
    PluginCategory
)
from app.platform_verification.extension_framework.tooling.scaffolding import plugin_scaffolder
from app.platform_verification.extension_framework.tooling.validator import plugin_contract_validator
from app.platform_verification.extension_framework.tooling.docs_generator import plugin_doc_generator


class PluginDeveloperSDK:
    """Developer SDK for creating, validating, and testing enterprise verification plugins."""

    @staticmethod
    def create_plugin_project(
        plugin_name: str,
        plugin_id: str,
        category: PluginCategory = PluginCategory.VERIFICATION,
        author: str = "Enterprise Developer",
        capabilities: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """Generates standard plugin project layout."""
        return plugin_scaffolder.generate_plugin_scaffold(
            plugin_name=plugin_name,
            plugin_id=plugin_id,
            author=author,
            capabilities=capabilities or ["custom_verification"]
        )

    @staticmethod
    def validate_plugin(plugin_instance: Any) -> Tuple[bool, List[str]]:
        """Validates plugin contract compliance."""
        return plugin_contract_validator.validate_plugin_instance(plugin_instance)

    @staticmethod
    def generate_documentation(plugin_instance: Any) -> str:
        """Generates markdown documentation for plugin."""
        return plugin_doc_generator.generate_markdown(plugin_instance)


plugin_sdk = PluginDeveloperSDK()
