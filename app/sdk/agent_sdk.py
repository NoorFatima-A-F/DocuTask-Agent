"""Enterprise Agent SDK - Core Agent Abstractions.

Defines base classes, lifecycle protocols, execution contexts, and capability
contracts for any autonomous agent running on the DocuTask Platform OS.
"""

from __future__ import annotations

import abc
import enum
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


class AgentLifecycleState(str, enum.Enum):
    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    IDLE = "idle"
    EXECUTING = "executing"
    WAITING_FOR_INPUT = "waiting_for_input"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    TERMINATED = "terminated"


@dataclass
class AgentManifest:
    agent_id: str
    name: str
    version: str
    author: str
    description: str
    required_capabilities: List[str] = field(default_factory=list)
    provided_capabilities: List[str] = field(default_factory=list)
    allowed_tools: List[str] = field(default_factory=list)
    permission_scopes: List[str] = field(default_factory=list)
    resource_limits: Dict[str, Any] = field(default_factory=dict)
    schema_version: str = "2026.1"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description,
            "required_capabilities": self.required_capabilities,
            "provided_capabilities": self.provided_capabilities,
            "allowed_tools": self.allowed_tools,
            "permission_scopes": self.permission_scopes,
            "resource_limits": self.resource_limits,
            "schema_version": self.schema_version,
        }


@dataclass
class AgentExecutionContext:
    session_id: str
    mission_id: str
    environment_vars: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    granted_scopes: Set[str] = field(default_factory=set)
    created_at: float = field(default_factory=time.time)

    def has_scope(self, scope: str) -> bool:
        return scope in self.granted_scopes or "*" in self.granted_scopes


class BaseAgent(abc.ABC):
    def __init__(self, manifest: AgentManifest, context: Optional[AgentExecutionContext] = None):
        self.manifest = manifest
        self.context = context or AgentExecutionContext(
            session_id=f"sess-{uuid.uuid4().hex[:8]}",
            mission_id=f"miss-{uuid.uuid4().hex[:8]}",
            granted_scopes=set(manifest.permission_scopes),
        )
        self.state = AgentLifecycleState.UNINITIALIZED
        self._telemetry_hooks: List[Any] = []

    def initialize(self) -> None:
        self.state = AgentLifecycleState.INITIALIZING
        self.on_init()
        self.state = AgentLifecycleState.IDLE

    def on_init(self) -> None:
        """Override for custom initialization logic."""
        pass

    @abc.abstractmethod
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's core autonomous mission step."""
        pass

    def terminate(self) -> None:
        self.on_terminate()
        self.state = AgentLifecycleState.TERMINATED

    def on_terminate(self) -> None:
        """Override for cleanup logic."""
        pass

    def get_health(self) -> Dict[str, Any]:
        return {
            "agent_id": self.manifest.agent_id,
            "state": self.state.value,
            "version": self.manifest.version,
            "session_id": self.context.session_id,
            "healthy": self.state not in (AgentLifecycleState.FAILED, AgentLifecycleState.TERMINATED),
        }
