"""
Runtime Domain Events.
Pub/Sub compatible events emitted during platform kernel boot, module discovery, plugin loading, and shutdown.
"""

from dataclasses import dataclass
from app.agents.events import AgentEvent


@dataclass(frozen=True)
class RuntimeBootStartedEvent(AgentEvent):
    event_type: str = "RuntimeBootStarted"


@dataclass(frozen=True)
class RuntimeBootCompletedEvent(AgentEvent):
    event_type: str = "RuntimeBootCompleted"


@dataclass(frozen=True)
class RuntimeBootFailedEvent(AgentEvent):
    event_type: str = "RuntimeBootFailed"


@dataclass(frozen=True)
class SubsystemRegisteredEvent(AgentEvent):
    event_type: str = "SubsystemRegistered"


@dataclass(frozen=True)
class ModuleDiscoveredEvent(AgentEvent):
    event_type: str = "ModuleDiscovered"


@dataclass(frozen=True)
class PluginLoadedEvent(AgentEvent):
    event_type: str = "PluginLoaded"


@dataclass(frozen=True)
class HealthDegradedEvent(AgentEvent):
    event_type: str = "HealthDegraded"


@dataclass(frozen=True)
class SupervisorRestartTriggeredEvent(AgentEvent):
    event_type: str = "SupervisorRestartTriggered"


@dataclass(frozen=True)
class ShutdownInitiatedEvent(AgentEvent):
    event_type: str = "ShutdownInitiated"


@dataclass(frozen=True)
class RuntimeTerminatedEvent(AgentEvent):
    event_type: str = "RuntimeTerminated"
