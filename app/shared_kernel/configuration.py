"""
Abstract Configuration Contracts and Interfaces.
Provides framework-neutral configuration loader, source, and snapshot abstractions.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

class ConfigurationSource(str, Enum):
    ENVIRONMENT = "ENVIRONMENT"
    FILE = "FILE"
    DATABASE = "DATABASE"
    REMOTE = "REMOTE"
    CODE = "CODE"
    OVERRIDE = "OVERRIDE"

@dataclass(frozen=True)
class ConfigurationSnapshotContract(ABC):
    snapshot_id: str
    source: ConfigurationSource
    sha256_hash: str
    values: Dict[str, Any] = field(default_factory=dict)
    frozen: bool = True

class ConfigurationValidatorContract(ABC):
    @abstractmethod
    def validate_config(self, raw_config: Dict[str, Any]) -> bool:
        pass

class ConfigurationLoaderContract(ABC):
    @abstractmethod
    def load(self) -> Dict[str, Any]:
        pass

class ConfigurationProviderContract(ABC):
    @abstractmethod
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        pass

    @abstractmethod
    def get_snapshot(self) -> ConfigurationSnapshotContract:
        pass
