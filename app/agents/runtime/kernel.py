"""
Enterprise Runtime Kernel.
Implements IKernel; serves as the centralized platform control plane governing boot, shutdown,
dependency graph resolution, Erlang OTP supervision, and multi-tenancy.
"""

import logging
from typing import Any, Optional
from app.agents.runtime.configuration import PlatformRuntimeConfig
from app.agents.runtime.dependency_container import DependencyContainer
from app.agents.runtime.dependency_manager import DependencyManager
from app.agents.runtime.interfaces import IKernel
from app.agents.runtime.plugin_manager import PluginManager
from app.agents.runtime.runtime_health import PlatformHealthReport
from app.agents.runtime.runtime_lifecycle import RuntimeLifecycleState
from app.agents.runtime.runtime_metrics import RuntimeMetricsCollector
from app.agents.runtime.runtime_monitor import RuntimeMonitor
from app.agents.runtime.runtime_state import RuntimeState
from app.agents.runtime.runtime_supervisor import RuntimeSupervisor
from app.agents.runtime.service_registry import ServiceRegistry
from app.agents.runtime.shutdown import ShutdownPipeline
from app.agents.runtime.startup import StartupPipeline
from app.agents.runtime.tenant_manager import TenantManager

logger = logging.getLogger(__name__)


class RuntimeKernel(IKernel):
    """Platform Runtime Kernel acting as the Kubernetes/Ray/Temporal control plane for agents."""

    def __init__(
        self,
        config: Optional[PlatformRuntimeConfig] = None,
        event_bus: Optional[Any] = None,
    ) -> None:
        self.config = config or PlatformRuntimeConfig()
        self.event_bus = event_bus
        self.state = RuntimeState(lifecycle_state=RuntimeLifecycleState.OFFLINE)
        self.metrics = RuntimeMetricsCollector()
        self.service_registry = ServiceRegistry()
        self.container = DependencyContainer()
        self.dependency_manager = DependencyManager()
        self.plugin_manager = PluginManager()
        self.supervisor = RuntimeSupervisor()
        self.monitor = RuntimeMonitor()
        self.tenant_manager = TenantManager()

    async def boot(self) -> None:
        """Executes the deterministic 11-step platform boot and wiring sequence."""
        logger.info("Booting Enterprise Agent Platform Runtime Kernel...")
        startup = StartupPipeline(
            config=self.config,
            event_bus=self.event_bus,
            metrics=self.metrics,
        )
        components = await startup.execute()
        self.state = components["state"]
        self.service_registry = components["service_registry"]
        self.dependency_manager = components["dependency_manager"]
        self.plugin_manager = components["plugin_manager"]
        self.monitor = components["monitor"]
        self.container = components["container"]

        logger.info(
            f"Kernel successfully booted into state '{self.state.lifecycle_state.value}' with "
            f"{self.service_registry.count()} registered services."
        )

    async def shutdown(self) -> None:
        """Gracefully terminates the platform runtime kernel."""
        logger.info("Initiating platform kernel shutdown...")
        shutdown_pipe = ShutdownPipeline(
            event_bus=self.event_bus,
            metrics=self.metrics,
        )
        self.state = await shutdown_pipe.execute(self.state)

    def is_running(self) -> bool:
        """Returns True if the kernel is operational."""
        return self.state.lifecycle_state in (
            RuntimeLifecycleState.RUNNING,
            RuntimeLifecycleState.READY,
            RuntimeLifecycleState.DEGRADED,
        )

    async def check_health(self) -> PlatformHealthReport:
        """Returns aggregate platform health report."""
        return await self.monitor.check_health()
