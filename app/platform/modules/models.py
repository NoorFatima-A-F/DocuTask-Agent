"""
Platform Module Domain Models and 9-State Lifecycle Machine.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from ..kernel.metadata import ModuleMetadata
from ..kernel.versioning import SemanticVersion


class ModuleState(str, Enum):
    """9-state formal lifecycle of a platform module."""
    DISCOVERED = "DISCOVERED"
    VALIDATED = "VALIDATED"
    REGISTERED = "REGISTERED"
    CONFIGURED = "CONFIGURED"
    INITIALIZED = "INITIALIZED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    UNLOADED = "UNLOADED"


@dataclass
class ModuleRecord:
    """Runtime tracking record for a managed module."""
    name: str
    version: SemanticVersion
    metadata: ModuleMetadata
    state: ModuleState = ModuleState.DISCOVERED
    instance: Optional[Any] = None
    loaded_at: Optional[datetime] = None
    error_message: Optional[str] = None
    configuration: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": str(self.version),
            "state": self.state.value,
            "dependencies": self.metadata.dependencies,
            "capabilities": self.metadata.capabilities,
            "loaded_at": self.loaded_at.isoformat() if self.loaded_at else None,
            "error_message": self.error_message,
        }
