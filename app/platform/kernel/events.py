"""
Platform Kernel Event Definitions and Types.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
import uuid


class KernelEventType(str, Enum):
    """Core event types generated within the platform kernel."""
    RUNTIME_STATE_CHANGED = "platform.runtime.state_changed"
    BOOTSTRAP_COMPLETED = "platform.runtime.bootstrap_completed"
    SHUTDOWN_INITIATED = "platform.runtime.shutdown_initiated"
    SHUTDOWN_COMPLETED = "platform.runtime.shutdown_completed"
    MODULE_REGISTERED = "platform.module.registered"
    MODULE_LOADED = "platform.module.loaded"
    MODULE_FAILED = "platform.module.failed"
    PLUGIN_REGISTERED = "platform.plugin.registered"
    PLUGIN_UNLOADED = "platform.plugin.unloaded"
    CAPABILITY_ADVERTISED = "platform.capability.advertised"
    HEALTH_STATUS_CHANGED = "platform.health.status_changed"
    ERROR_OCCURRED = "platform.error.occurred"
    RECOVERY_INITIATED = "platform.recovery.initiated"


class IKernelEvent(ABC):
    """Protocol for kernel events."""

    @property
    @abstractmethod
    def event_id(self) -> str:
        pass

    @property
    @abstractmethod
    def event_type(self) -> str:
        pass

    @property
    @abstractmethod
    def timestamp(self) -> datetime:
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass


@dataclass(frozen=True)
class KernelEvent(IKernelEvent):
    """Concrete immutable kernel event envelope."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = KernelEventType.RUNTIME_STATE_CHANGED.value
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    source: str = "platform.kernel"
    tenant_id: Optional[str] = None
    correlation_id: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.event_id,
            "type": self.event_type,
            "source": self.source,
            "time": self.timestamp.isoformat(),
            "tenant": self.tenant_id,
            "correlation_id": self.correlation_id,
            "data": self.data,
        }
