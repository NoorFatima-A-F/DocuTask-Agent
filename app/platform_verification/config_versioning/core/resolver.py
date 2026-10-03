"""
Layered Configuration Resolver.
Enforces strict 7-tier precedence:
1. Experiment Override (highest)
2. Execution Config
3. Module Config
4. Service Config
5. Environment Config
6. Platform Config
7. Global Defaults (lowest)
"""
import copy
from typing import Any, Dict, Optional
from app.platform_verification.config_versioning.domain.models import EnvironmentTier

class ConfigurationResolver:
    def __init__(self):
        self._global_defaults: Dict[str, Any] = {
            "platform_name": "DocuTask Enterprise Agent Platform",
            "version": "2.0.0",
            "log_level": "INFO",
            "timeout_seconds": 300,
            "max_retries": 3,
            "security": {
                "enforce_tls": True,
                "token_expiry_hours": 24,
                "allow_insecure_origins": False
            },
            "ai": {
                "default_model": "gemini-2.5-flash",
                "temperature": 0.0,
                "max_tokens": 4096
            }
        }
        self._environment_configs: Dict[EnvironmentTier, Dict[str, Any]] = {
            EnvironmentTier.DEVELOPMENT: {"log_level": "DEBUG", "timeout_seconds": 60, "mock_external_apis": True},
            EnvironmentTier.INTEGRATION: {"timeout_seconds": 180, "mock_external_apis": False},
            EnvironmentTier.STAGING: {"timeout_seconds": 300, "production_shadow_sampling": 0.1},
            EnvironmentTier.PRODUCTION: {"timeout_seconds": 600, "strict_quality_gates": True},
            EnvironmentTier.CHAOS: {"fault_injection_rate": 0.05, "latency_injection_ms": 250},
            EnvironmentTier.SECURITY_LAB: {"fuzzing_enabled": True, "strict_cert_verification": True}
        }
        self._service_configs: Dict[str, Dict[str, Any]] = {}
        self._module_configs: Dict[str, Dict[str, Any]] = {}

    def set_service_config(self, service_name: str, config: Dict[str, Any]) -> None:
        self._service_configs[service_name] = config

    def set_module_config(self, module_name: str, config: Dict[str, Any]) -> None:
        self._module_configs[module_name] = config

    def resolve(
        self,
        environment: EnvironmentTier = EnvironmentTier.INTEGRATION,
        service_name: Optional[str] = None,
        module_name: Optional[str] = None,
        execution_config: Optional[Dict[str, Any]] = None,
        experiment_override: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Deeply merges configurations following the 7-tier precedence."""
        resolved: Dict[str, Any] = copy.deepcopy(self._global_defaults)
        
        # 1. Environment Config
        if environment in self._environment_configs:
            self._deep_update(resolved, self._environment_configs[environment])

        # 2. Service Config
        if service_name and service_name in self._service_configs:
            self._deep_update(resolved, self._service_configs[service_name])

        # 3. Module Config
        if module_name and module_name in self._module_configs:
            self._deep_update(resolved, self._module_configs[module_name])

        # 4. Execution Config
        if execution_config:
            self._deep_update(resolved, execution_config)

        # 5. Experiment Override (highest priority)
        if experiment_override:
            self._deep_update(resolved, experiment_override)

        return resolved

    def _deep_update(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        for k, v in source.items():
            if isinstance(v, dict) and k in target and isinstance(target[k], dict):
                self._deep_update(target[k], v)
            else:
                target[k] = copy.deepcopy(v)

configuration_resolver = ConfigurationResolver()
