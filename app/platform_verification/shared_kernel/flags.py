"""
Feature Flag System.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

class FeatureFlagProvider(ABC):
    @abstractmethod
    def is_enabled(self, flag_key: str, tenant_id: str = "default", default: bool = False) -> bool:
        pass


class MemoryFeatureFlagProvider(FeatureFlagProvider):
    def __init__(self, initial_flags: Dict[str, bool] = None):
        self._flags: Dict[str, bool] = initial_flags or {
            "enable_probabilistic_bootstrap": True,
            "enable_welch_drift_detection": True,
            "enable_cas_merkle_trees": True,
            "enable_hmac_certification": True,
            "enable_audit_hash_chain": True,
            "enable_async_worker_execution": True
        }

    def is_enabled(self, flag_key: str, tenant_id: str = "default", default: bool = False) -> bool:
        return self._flags.get(flag_key, default)

    def set_flag(self, flag_key: str, enabled: bool) -> None:
        self._flags[flag_key] = enabled
