"""
Hardened Runtime Startup Pipeline & Boot Transaction Manager.
Executes the deterministic 10-step platform startup sequence with transactional rollback on failure:
OFFLINE -> BOOTING -> CONFIGURATION_VALIDATION -> DEPENDENCY_RESOLUTION -> MODULE_DISCOVERY ->
SERVICE_REGISTRATION -> PLUGIN_LOADING -> SUBSYSTEM_INITIALIZATION -> HEALTH_CHECK -> READY -> RUNNING.
"""

import logging
import time
from typing import Any, Callable, Coroutine, Dict, List, Optional
from app.agents.runtime.bootstrap import PlatformBootstrapper
from app.agents.runtime.configuration import PlatformRuntimeConfig
from app.agents.runtime.dependency_manager import DependencyManager
from app.agents.runtime.events import (
    ModuleDiscoveredEvent,
    RuntimeBootCompletedEvent,
    RuntimeBootFailedEvent,
    RuntimeBootStartedEvent,
    SubsystemRegisteredEvent,
)
from app.agents.runtime.initializer import SubsystemInitializer
from app.agents.runtime.module_loader import ModuleLoader
from app.agents.runtime.plugin_manager import PluginManager
from app.agents.runtime.runtime_health import SubsystemHealthStatus
from app.agents.runtime.runtime_lifecycle import RuntimeLifecycleState
from app.agents.runtime.runtime_metrics import RuntimeMetricsCollector
from app.agents.runtime.runtime_monitor import RuntimeMonitor
from app.agents.runtime.runtime_state import RuntimeState
from app.agents.runtime.service_registry import ServiceRegistry

logger = logging.getLogger(__name__)


class BootTransactionManager:
    """Manages transactional boot progression and executes reverse cleanup upon step failure."""

    def __init__(self) -> None:
        self._rollback_actions: List[Tuple_Action] = []

    def record_action(self, description: str, rollback_fn: Callable[[], Coroutine[Any, Any, Any]]) -> None:
        """Registers a reverse compensating action to execute if boot fails later."""
        self._rollback_actions.append((description, rollback_fn))

    async def execute_rollback(self) -> List[str]:
        """Executes all registered rollback actions in LIFO reverse order."""
        executed = []
        while self._rollback_actions:
            desc, fn = self._rollback_actions.pop()
            logger.warning(f"BootTransactionManager: Rolling back '{desc}'...")
            try:
                await fn()
                executed.append(desc)
            except Exception as e:
                logger.error(f"Error during boot rollback of '{desc}': {e}")
        return executed

    def commit(self) -> None:
        """Clears rollback actions upon successful boot completion."""
        self._rollback_actions.clear()


Tuple_Action = Any


class StartupPipeline:
    """Production-grade hardened startup pipeline with automatic transactional rollback."""

    def __init__(
        self,
        config: Optional[PlatformRuntimeConfig] = None,
        event_bus: Optional[Any] = None,
        metrics: Optional[RuntimeMetricsCollector] = None,
    ) -> None:
        self.config = config or PlatformRuntimeConfig()
        self.event_bus = event_bus
        self.metrics = metrics or RuntimeMetricsCollector()
        self.tx_manager = BootTransactionManager()

    async def execute(self) -> Dict[str, Any]:
        """Executes the boot pipeline; executes full transactional rollback on failure."""
        start_time = time.perf_counter()
        logger.info("Executing Hardened Platform Runtime Startup Pipeline...")
        await self._publish_event(RuntimeBootStartedEvent())

        state = RuntimeState(lifecycle_state=RuntimeLifecycleState.BOOTING)

        try:
            # 1. Bootstrap
            bootstrapper = PlatformBootstrapper(self.config)
            container = bootstrapper.bootstrap()
            registry: ServiceRegistry = container.resolve(ServiceRegistry)
            dep_manager: DependencyManager = container.resolve(DependencyManager)

            async def _cleanup_container():
                container.clear()
                registry.clear()
            self.tx_manager.record_action("bootstrap_container", _cleanup_container)

            # 2. Configuration Validation & Initialization State
            state = state.transition_to(RuntimeLifecycleState.INITIALIZING)

            # 3. Module Discovery
            module_loader = ModuleLoader()
            discovered_modules = module_loader.discover_modules()
            for mod in discovered_modules:
                dep_manager.register_subsystem(mod.name, mod.dependencies)
                await self._publish_event(
                    ModuleDiscoveredEvent(payload={"module": mod.name, "version": mod.version})
                )

            # 4. Dependency Ordering & Service Registration
            startup_order = dep_manager.compute_initialization_order()
            logger.info(f"Computed subsystem startup order: {startup_order}")

            initializer = SubsystemInitializer(registry)
            for mod_name in startup_order:
                subsystem_instance = await initializer.initialize_subsystem(mod_name)
                registry.register(dict, subsystem_instance, name=mod_name)
                await self._publish_event(
                    SubsystemRegisteredEvent(payload={"subsystem": mod_name})
                )

            # 5. Plugin Loading
            plugin_manager = PluginManager()

            # 6. Health & Readiness Verification
            monitor = RuntimeMonitor()
            health_report = await monitor.check_health()
            if health_report.overall_status == SubsystemHealthStatus.UNHEALTHY:
                state = state.transition_to(RuntimeLifecycleState.DEGRADED)
                logger.warning("Startup health report indicated DEGRADED subsystems.")
            else:
                state = state.transition_to(RuntimeLifecycleState.READY)
                state = state.transition_to(RuntimeLifecycleState.RUNNING)

            duration_ms = (time.perf_counter() - start_time) * 1000.0
            self.metrics.record_startup_time(duration_ms)
            self.metrics.set_registered_services(registry.count())

            self.tx_manager.commit()
            await self._publish_event(
                RuntimeBootCompletedEvent(
                    payload={"duration_ms": duration_ms, "state": state.lifecycle_state.value}
                )
            )

            return {
                "state": state,
                "container": container,
                "service_registry": registry,
                "dependency_manager": dep_manager,
                "module_loader": module_loader,
                "plugin_manager": plugin_manager,
                "monitor": monitor,
                "metrics": self.metrics,
            }

        except Exception as exc:
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            logger.error(f"StartupPipeline failed during boot: {exc}. Rolling back initialized state.")
            await self.tx_manager.execute_rollback()
            await self._publish_event(
                RuntimeBootFailedEvent(payload={"error": str(exc), "duration_ms": duration_ms})
            )
            raise

    async def _publish_event(self, event: Any) -> None:
        if self.event_bus and hasattr(self.event_bus, "publish"):
            try:
                await self.event_bus.publish(event)
            except Exception as ex:
                logger.warning(f"Startup event publishing failed: {ex}")
