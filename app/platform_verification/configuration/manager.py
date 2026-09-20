"""
Scoped Configuration Manager with Immutability and Hashing.
"""
import copy
import hashlib
import json
from typing import Any, Dict, Optional
from app.platform_verification.configuration.scopes import ConfigScope
from app.platform_verification.configuration.schemas import VerificationPlatformConfig
from app.platform_verification.shared_kernel.exceptions import ConfigurationException

class EnterpriseConfigurationManager:
    def __init__(self):
        self._scoped_configs: Dict[ConfigScope, Dict[str, Any]] = {
            scope: {} for scope in ConfigScope
        }
        self._frozen_configs: Dict[str, Dict[str, Any]] = {}
        self._load_defaults()

    def _load_defaults(self):
        default_cfg = VerificationPlatformConfig().model_dump()
        self._scoped_configs[ConfigScope.GLOBAL] = default_cfg

    def set_scoped_config(self, scope: ConfigScope, key: str, value: Any) -> None:
        self._scoped_configs[scope][key] = value

    def get_scoped_config(self, scope: ConfigScope, key: str, default: Any = None) -> Any:
        return self._scoped_configs[scope].get(key, default)

    def resolve_effective_config(
        self,
        module_name: Optional[str] = None,
        execution_id: Optional[str] = None,
        overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Resolves configuration hierarchy: GLOBAL -> ENV -> MODULE -> EXECUTION -> EXPERIMENT -> OVERRIDE."""
        effective: Dict[str, Any] = {}
        
        # 1. Global
        effective.update(self._scoped_configs[ConfigScope.GLOBAL])
        # 2. Environment
        effective.update(self._scoped_configs[ConfigScope.ENVIRONMENT])
        # 3. Module
        if module_name and module_name in self._scoped_configs[ConfigScope.MODULE]:
            effective.update(self._scoped_configs[ConfigScope.MODULE][module_name])
        # 4. Execution
        if execution_id and execution_id in self._scoped_configs[ConfigScope.EXECUTION]:
            effective.update(self._scoped_configs[ConfigScope.EXECUTION][execution_id])
        # 5. Overrides
        if overrides:
            effective.update(overrides)

        return effective

    def freeze_execution_config(self, execution_id: str, config_dict: Dict[str, Any]) -> str:
        """Locks configuration during execution and returns its SHA-256 fingerprint."""
        frozen_copy = copy.deepcopy(config_dict)
        config_hash = hashlib.sha256(json.dumps(frozen_copy, sort_keys=True, default=str).encode("utf-8")).hexdigest()
        self._frozen_configs[execution_id] = {
            "config": frozen_copy,
            "hash": config_hash
        }
        return config_hash

    def get_frozen_config(self, execution_id: str) -> Optional[Dict[str, Any]]:
        return self._frozen_configs.get(execution_id, {}).get("config")

verification_config_manager = EnterpriseConfigurationManager()
