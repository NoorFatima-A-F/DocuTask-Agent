"""
Platform Runtime Container.
Encapsulates Kernel, Cache, Repository, Metrics, and Platform Host components.
"""

from typing import Any, Optional
from app.agents.runtime.configuration import PlatformRuntimeConfig
from app.agents.runtime.kernel import RuntimeKernel
from app.agents.runtime.platform import Platform
from app.agents.runtime.runtime_cache import RuntimeCache
from app.agents.runtime.runtime_repository import (
    IRuntimeRepository,
    InMemoryRuntimeRepository,
)


class PlatformRuntime:
    """Production runtime environment hosting the platform kernel and stateful services."""

    def __init__(
        self,
        config: Optional[PlatformRuntimeConfig] = None,
        repository: Optional[IRuntimeRepository] = None,
        cache: Optional[RuntimeCache] = None,
        event_bus: Optional[Any] = None,
    ) -> None:
        self.config = config or PlatformRuntimeConfig()
        self.repository = repository or InMemoryRuntimeRepository()
        self.cache = cache or RuntimeCache()
        self.platform = Platform(config=self.config, event_bus=event_bus)

    @property
    def kernel(self) -> RuntimeKernel:
        return self.platform.kernel

    @property
    def is_active(self) -> bool:
        return self.kernel.is_running()

    async def initialize(self) -> None:
        """Boots platform kernel and binds state."""
        await self.platform.start()
        await self.repository.save_state(self.kernel.state)

    async def shutdown(self) -> None:
        """Shuts down platform kernel and saves terminal state."""
        await self.platform.stop()
        await self.repository.save_state(self.kernel.state)
