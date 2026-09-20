"""
Enterprise Configuration Provider.
Resolves configuration values across the 11-tier precedence hierarchy with origin tracking.
"""

import os
from typing import Any, Dict, List, Optional
from .schema import ConfigDomain, ConfigEntrySchema, ConfigSource, ResolvedConfigValue
from .validator import ConfigurationValidator
from .registry import ConfigurationRegistry


class ConfigurationProvider:
    """
    11-Tier Enterprise Configuration Resolution Provider.
    """

    def __init__(self, registry: Optional[ConfigurationRegistry] = None):
        self.registry = registry or ConfigurationRegistry()
        self._layers: Dict[ConfigSource, Dict[str, Any]] = {source: {} for source in ConfigSource}
        self._load_environment_layer()

    def set_layer_value(self, source: ConfigSource, key: str, value: Any) -> None:
        """Set a configuration value at a specific precedence layer."""
        self._layers[source][key] = value

    def set_layer_values(self, source: ConfigSource, values: Dict[str, Any]) -> None:
        """Batch set values at a specific precedence layer."""
        self._layers[source].update(values)

    def clear_layer(self, source: ConfigSource) -> None:
        """Clear all entries in a specific precedence layer."""
        self._layers[source].clear()

    def _load_environment_layer(self) -> None:
        """Load matching environment variables (e.g. DOCUTASK_DATABASE_POOL_SIZE -> database.pool_size)."""
        prefix = "DOCUTASK_"
        for env_k, env_v in os.environ.items():
            if env_k.startswith(prefix):
                key = env_k[len(prefix):].lower().replace("__", ".").replace("_", ".")
                self._layers[ConfigSource.ENVIRONMENT][key] = env_v

    def get(
        self,
        key: str,
        default: Any = None,
        execution_overrides: Optional[Dict[str, Any]] = None,
        workflow_overrides: Optional[Dict[str, Any]] = None,
        workspace_overrides: Optional[Dict[str, Any]] = None,
        org_overrides: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Resolve a configuration value following the strict 11-tier precedence hierarchy.
        """
        resolved = self.get_resolved(
            key=key,
            execution_overrides=execution_overrides,
            workflow_overrides=workflow_overrides,
            workspace_overrides=workspace_overrides,
            org_overrides=org_overrides,
        )
        if resolved is not None:
            return resolved.value
        return default

    def get_resolved(
        self,
        key: str,
        execution_overrides: Optional[Dict[str, Any]] = None,
        workflow_overrides: Optional[Dict[str, Any]] = None,
        workspace_overrides: Optional[Dict[str, Any]] = None,
        org_overrides: Optional[Dict[str, Any]] = None,
    ) -> Optional[ResolvedConfigValue]:
        """
        Resolve configuration value with full metadata and origin source tracking.
        """
        schema = self.registry.get_schema(key)
        domain = schema.domain if schema else ConfigDomain.DATABASE

        # Ordered from Highest Priority to Lowest Priority
        precedence_sources = [
            (ConfigSource.EXECUTION_OVERRIDE, execution_overrides or {}),
            (ConfigSource.WORKFLOW, workflow_overrides or {}),
            (ConfigSource.WORKSPACE, workspace_overrides or {}),
            (ConfigSource.ORGANIZATION, org_overrides or {}),
            (ConfigSource.FEATURE_FLAG, self._layers[ConfigSource.FEATURE_FLAG]),
            (ConfigSource.RUNTIME_OVERRIDE, self._layers[ConfigSource.RUNTIME_OVERRIDE]),
            (ConfigSource.SECRETS_MANAGER, self._layers[ConfigSource.SECRETS_MANAGER]),
            (ConfigSource.CLOUD_CONFIG, self._layers[ConfigSource.CLOUD_CONFIG]),
            (ConfigSource.ENVIRONMENT, self._layers[ConfigSource.ENVIRONMENT]),
            (ConfigSource.YAML_FILE, self._layers[ConfigSource.YAML_FILE]),
        ]

        for source_enum, layer_dict in precedence_sources:
            if key in layer_dict:
                raw_val = layer_dict[key]
                validated_val = ConfigurationValidator.validate_entry(schema, raw_val) if schema else raw_val
                return ResolvedConfigValue(
                    key=key,
                    value=validated_val,
                    source=source_enum,
                    domain=domain,
                    schema=schema,
                )

        # Fallback to Defaults (Lowest Priority)
        if schema and schema.default_value is not None:
            return ResolvedConfigValue(
                key=key,
                value=schema.default_value,
                source=ConfigSource.DEFAULTS,
                domain=domain,
                schema=schema,
            )

        return None
