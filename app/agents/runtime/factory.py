"""
Runtime Factory.
Dependency injection factory assembling fully configured PlatformRuntime, RuntimeKernel, and Platform instances.
"""

from typing import Any, Optional
from app.agents.runtime.configuration import PlatformRuntimeConfig
from app.agents.runtime.kernel import RuntimeKernel
from app.agents.runtime.platform import Platform
from app.agents.runtime.runtime import PlatformRuntime
from app.agents.runtime.runtime_cache import RuntimeCache
from app.agents.runtime.runtime_repository import (
    IRuntimeRepository,
    InMemoryRuntimeRepository,
)


class RuntimeFactory:
    """Factory for instantiating production-ready runtime components."""

    @staticmethod
    def create_kernel(
        config: Optional[PlatformRuntimeConfig] = None,
        event_bus: Optional[Any] = None,
    ) -> RuntimeKernel:
        """Constructs an unbooted RuntimeKernel."""
        return RuntimeKernel(config=config, event_bus=event_bus)

    @staticmethod
    def create_platform(
        config: Optional[PlatformRuntimeConfig] = None,
        event_bus: Optional[Any] = None,
    ) -> Platform:
        """Constructs a Platform host facade."""
        return Platform(config=config, event_bus=event_bus)

    @staticmethod
    def create_runtime(
        config: Optional[PlatformRuntimeConfig] = None,
        repository: Optional[IRuntimeRepository] = None,
        cache: Optional[RuntimeCache] = None,
        event_bus: Optional[Any] = None,
    ) -> PlatformRuntime:
        """Constructs a complete PlatformRuntime container."""
        return PlatformRuntime(
            config=config,
            repository=repository or InMemoryRuntimeRepository(),
            cache=cache or RuntimeCache(),
            event_bus=event_bus,
        )
