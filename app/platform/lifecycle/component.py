"""
Lifecycle Component Protocol and Base Class.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..kernel.lifecycle import LifecycleState
from ..kernel.health import ComponentHealth, HealthStatus


class ILifecycleComponent(ABC):
    """Standard lifecycle contract implemented by all platform subsystems."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Canonical name of this component."""
        pass

    @property
    @abstractmethod
    def dependencies(self) -> List[str]:
        """Names of components this component depends on for startup."""
        pass

    @property
    @abstractmethod
    def state(self) -> LifecycleState:
        """Current state of this component."""
        pass

    @abstractmethod
    async def initialize(self) -> None:
        """Pre-startup resource allocation, connection pools, schemas."""
        pass

    @abstractmethod
    async def start(self) -> None:
        """Start active execution, listeners, worker loops."""
        pass

    @abstractmethod
    async def health_check(self) -> ComponentHealth:
        """Evaluate operational health."""
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        """Graceful shutdown, state flushing, pool closing."""
        pass


class BaseLifecycleComponent(ILifecycleComponent):
    """Convenience base implementation of ILifecycleComponent."""

    def __init__(self, name: str, dependencies: Optional[List[str]] = None):
        self._name = name
        self._dependencies = dependencies or []
        self._state = LifecycleState.UNINITIALIZED

    @property
    def name(self) -> str:
        return self._name

    @property
    def dependencies(self) -> List[str]:
        return self._dependencies

    @property
    def state(self) -> LifecycleState:
        return self._state

    async def initialize(self) -> None:
        self._state = LifecycleState.INITIALIZED

    async def start(self) -> None:
        self._state = LifecycleState.ACTIVE

    async def health_check(self) -> ComponentHealth:
        return ComponentHealth(
            component_name=self.name,
            status=HealthStatus.HEALTHY if self._state == LifecycleState.ACTIVE else HealthStatus.DEGRADED,
            message=f"State: {self._state.value}",
        )

    async def shutdown(self) -> None:
        self._state = LifecycleState.STOPPED
