"""
Static & Contract Validator for Verification Plugins.
"""
from typing import Any, List, Tuple
from app.platform_verification.extension_framework.domain.interfaces import VerificationPluginInterface


class PluginContractValidator:
    @staticmethod
    def validate_plugin_instance(plugin: Any) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        if not isinstance(plugin, VerificationPluginInterface):
            errors.append("Plugin does not inherit from VerificationPluginInterface.")
            return False, errors

        # Check required methods
        required_methods = [
            "initialize", "validate", "configure", "execute",
            "collect_evidence", "calculate_metrics", "cleanup", "health_check"
        ]
        for m in required_methods:
            if not hasattr(plugin, m) or not callable(getattr(plugin, m)):
                errors.append(f"Missing required interface method: '{m}'")

        # Validate metadata
        try:
            meta = plugin.metadata
            if not meta.plugin_id:
                errors.append("Metadata missing 'plugin_id'")
            if not meta.capabilities:
                errors.append("Metadata missing declared 'capabilities'")
        except Exception as e:
            errors.append(f"Failed to access plugin metadata: {str(e)}")

        return len(errors) == 0, errors


plugin_contract_validator = PluginContractValidator()
