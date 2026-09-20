"""
Strongly-typed Domain Events for Plugin Extensibility.
"""
from dataclasses import dataclass
from typing import Any, Dict, Optional
from datetime import datetime, timezone
from app.platform_verification.extension_framework.domain.models import PluginLifecycleState, PluginHealthState


@dataclass(frozen=True)
class PluginDiscoveredEvent:
    plugin_id: str
    version: str
    discovery_mechanism: str
    timestamp: str = datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class PluginInitializedEvent:
    plugin_id: str
    version: str
    timestamp: str = datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class PluginExecutionStartedEvent:
    execution_id: str
    plugin_id: str
    correlation_id: str
    timestamp: str = datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class PluginExecutionCompletedEvent:
    execution_id: str
    plugin_id: str
    is_success: bool
    execution_time_ms: float
    timestamp: str = datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class PluginFailedEvent:
    plugin_id: str
    error: str
    stack_trace: Optional[str] = None
    timestamp: str = datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class PluginHealthChangedEvent:
    plugin_id: str
    old_state: PluginHealthState
    new_state: PluginHealthState
    timestamp: str = datetime.now(timezone.utc).isoformat()
