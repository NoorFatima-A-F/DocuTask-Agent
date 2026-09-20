"""Platform Plugin Base Contract and Interface (Req 59, 60)."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PluginMetadata:
    plugin_id: str
    name: str
    version: str
    author: str
    description: str
    declared_permissions: List[str] = field(default_factory=list)


class PlatformPlugin(ABC):
    """Standardized Extension Contract for Platform Delivery Ecosystem."""

    @abstractmethod
    def metadata(self) -> PluginMetadata:
        pass

    @abstractmethod
    def validate(self, config: Dict[str, Any]) -> bool:
        """Validates plugin configuration parameters."""
        pass

    @abstractmethod
    def initialize(self, context: Dict[str, Any]) -> None:
        """Initializes plugin resources."""
        pass

    @abstractmethod
    def execute(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Executes declared capability action."""
        pass

    @abstractmethod
    def health(self) -> bool:
        """Returns plugin health status."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Cleanly releases allocated resources."""
        pass
