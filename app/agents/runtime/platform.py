"""
Platform Runtime Host.
Implements IRuntimePlatform; provides high-level facade for platform boot, session creation, and service resolution.
"""

from typing import Any, Dict, Optional, Type, TypeVar
from uuid import UUID
from app.agents.runtime.configuration import PlatformRuntimeConfig
from app.agents.runtime.interfaces import IRuntimePlatform
from app.agents.runtime.kernel import RuntimeKernel
from app.agents.runtime.runtime_context import RuntimeContext
from app.agents.runtime.runtime_session import RuntimeSession
from app.agents.runtime.service_locator import ServiceLocator

T = TypeVar("T")


class Platform(IRuntimePlatform):
    """Unified platform host facade connecting user-facing gateways to the platform kernel."""

    def __init__(
        self,
        config: Optional[PlatformRuntimeConfig] = None,
        event_bus: Optional[Any] = None,
    ) -> None:
        self.kernel = RuntimeKernel(config=config, event_bus=event_bus)
        self.locator = ServiceLocator(self.kernel.service_registry)

    async def start(self) -> None:
        """Starts the platform runtime."""
        await self.kernel.boot()
        ServiceLocator.set_global_registry(self.kernel.service_registry)

    async def stop(self) -> None:
        """Stops the platform runtime."""
        await self.kernel.shutdown()

    def create_session(
        self,
        tenant_id: str = "default",
        user_id: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> RuntimeSession:
        """Spawns an authenticated root RuntimeSession under tenant policy."""
        self.kernel.tenant_manager.validate_tenant_access(tenant_id)
        ctx = RuntimeContext(
            tenant_id=tenant_id,
            user_id=user_id,
            environment=self.kernel.config.environment,
            attributes=attributes or {},
        )
        session = RuntimeSession(context=ctx)
        self.kernel.metrics.record_session_started()
        return session

    def resolve_service(self, interface_type: Type[T], name: Optional[str] = None) -> T:
        """Resolves a platform service via the ServiceRegistry."""
        return self.kernel.service_registry.resolve(interface_type, name=name)
