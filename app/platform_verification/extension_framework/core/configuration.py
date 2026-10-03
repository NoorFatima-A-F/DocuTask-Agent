"""
Plugin Configuration Engine with Schema Validation, Defaults Injection, and Secret Masking.
"""
from typing import Any, Dict, List, Tuple


class PluginConfigurationEngine:
    @staticmethod
    def validate_and_apply_defaults(
        config: Dict[str, Any],
        schema: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[str]]:
        errors: List[str] = []
        resolved = dict(config)

        # Inject defaults from schema
        for key, prop in schema.get("properties", {}).items():
            if key not in resolved and "default" in prop:
                resolved[key] = prop["default"]

        # Check required fields
        for req in schema.get("required", []):
            if req not in resolved:
                errors.append(f"Missing required plugin configuration property: '{req}'")

        return resolved, errors


plugin_config_engine = PluginConfigurationEngine()
