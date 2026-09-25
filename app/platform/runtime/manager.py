"""
Enterprise Platform Runtime Manager.
The core operating system kernel manager of DocuTask Agent.
Coordinates bootstrapper, dependency injection container, lifecycle state transitions, module loading,
service registries, event mesh, and graceful shutdown.
"""

from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional
from .states import RuntimeState, RuntimeStateEvent, VALID_STATE_TRANSITIONS
from ..kernel.exceptions import BootstrapException, LifecycleException
from ...core.container.container import DependencyContainer
from ..configuration.provider import ConfigurationProvider
from ..lifecycle.manager import LifecycleManager
from ..modules.manager import ModuleManager
from ..plugins.manager import PluginManager
from ..capabilities.registry import CapabilityRegistry
from ..registry.service_registry import ServiceRegistry
from ...observability.health.manager import HealthManager
from ...events.bus import EventBus
from ...infrastructure.secrets.secret_manager import SecretManager
from ...core.feature_flags.service import FeatureFlagService
from ..resources.manager import ResourceManager
from ..services.background.manager import BackgroundServiceManager
from ..diagnostics.reporter import DiagnosticsReporter
from ...infrastructure.logging.logger import PlatformLogger


class RuntimeManager:
    """
    DocuTask Agent Platform Runtime Manager.
    Bootstraps, monitors, and orchestrates the entire platform operating foundation.
    """

    def __init__(
        self,
        container: Optional[DependencyContainer] = None,
        config_provider: Optional[ConfigurationProvider] = None,
        event_bus: Optional[EventBus] = None,
    ):
        self._state = RuntimeState.CREATED
        self._state_history: List[RuntimeStateEvent] = []
        self._listeners: List[Callable[[RuntimeStateEvent], None]] = []

        # Platform Kernel Subsystems
        self.container = container or DependencyContainer()
        self.config_provider = config_provider or ConfigurationProvider()
        self.event_bus = event_bus or EventBus()
        self.secret_manager = SecretManager()
        self.feature_flags = FeatureFlagService()
        self.resource_manager = ResourceManager()
        self.lifecycle_manager = LifecycleManager()
        self.module_manager = ModuleManager()
        self.plugin_manager = PluginManager()
        self.capability_registry = CapabilityRegistry()
        self.service_registry = ServiceRegistry()
        self.health_manager = HealthManager()
        self.background_services = BackgroundServiceManager()
        self.diagnostics = DiagnosticsReporter(
            module_registry=self.module_manager.registry,
            plugin_registry=self.plugin_manager.registry,
            service_registry=self.service_registry,
            capability_registry=self.capability_registry,
            health_manager=self.health_manager,
        )
        self.logger = PlatformLogger("docutask.runtime")

        # Register foundational services in DI Container
        self._register_container_defaults()

    @property
    def state(self) -> RuntimeState:
        return self._state

    def add_state_listener(self, listener: Callable[[RuntimeStateEvent], None]) -> None:
        """Add callback for runtime state transitions."""
        self._listeners.append(listener)

    def transition(self, to_state: RuntimeState, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Validate and execute a finite state machine transition."""
        valid_next = VALID_STATE_TRANSITIONS.get(self._state, [])
        if to_state not in valid_next and to_state != RuntimeState.FAILED:
            raise LifecycleException(
                f"Invalid runtime state transition from {self._state.value} to {to_state.value}. Allowed: {[s.value for s in valid_next]}"
            )

        from_st = self._state
        self._state = to_state
        event = RuntimeStateEvent(
            from_state=from_st,
            to_state=to_state,
            timestamp=datetime.now(timezone.utc),
            metadata=metadata or {},
        )
        self._state_history.append(event)
        self.logger.info(f"Runtime state transition: {from_st.value} -> {to_state.value}", **(metadata or {}))

        # Notify listeners
        for listener in self._listeners:
            try:
                listener(event)
            except Exception:
                pass

    def _register_container_defaults(self) -> None:
        """Register kernel subsystems in DI container."""
        self.container.register_instance(DependencyContainer, self.container)
        self.container.register_instance(ConfigurationProvider, self.config_provider)
        self.container.register_instance(EventBus, self.event_bus)
        self.container.register_instance(SecretManager, self.secret_manager)
        self.container.register_instance(FeatureFlagService, self.feature_flags)
        self.container.register_instance(ResourceManager, self.resource_manager)
        self.container.register_instance(LifecycleManager, self.lifecycle_manager)
        self.container.register_instance(ModuleManager, self.module_manager)
        self.container.register_instance(PluginManager, self.plugin_manager)
        self.container.register_instance(CapabilityRegistry, self.capability_registry)
        self.container.register_instance(ServiceRegistry, self.service_registry)
        self.container.register_instance(HealthManager, self.health_manager)
        self.container.register_instance(BackgroundServiceManager, self.background_services)
        self.container.register_instance(DiagnosticsReporter, self.diagnostics)

    async def bootstrap(self) -> None:
        """Execute full platform bootstrap sequence across all lifecycle stages."""
        try:
            # 1. Config Loading
            self.transition(RuntimeState.CONFIG_LOADING)
            # 2. Config Validated
            self.transition(RuntimeState.CONFIG_VALIDATED)
            # 3. Secrets Ready
            self.transition(RuntimeState.SECRETS_READY)
            # 4. Database Ready
            self.transition(RuntimeState.DATABASE_READY)
            # 5. Cache Ready
            self.transition(RuntimeState.CACHE_READY)
            # 6. Queue Ready
            self.transition(RuntimeState.QUEUE_READY)
            # 7. Event Bus Ready
            self.transition(RuntimeState.EVENT_BUS_READY)
            # 8. Module Loading
            self.transition(RuntimeState.MODULE_LOADING)
            await self.module_manager.initialize_all()
            # 9. Plugin Loading
            self.transition(RuntimeState.PLUGIN_LOADING)
            # 10. Service Ready
            self.transition(RuntimeState.SERVICE_READY)
            await self.lifecycle_manager.initialize_all()
            await self.lifecycle_manager.start_all()
            # 11. Health Checking
            self.transition(RuntimeState.HEALTH_CHECKING)
            await self.health_manager.check_health()
            # 12. Ready
            self.health_manager.set_ready(True)
            self.health_manager.set_startup_complete(True)
            self.transition(RuntimeState.READY)
            # 13. Running
            await self.background_services.start()
            self.transition(RuntimeState.RUNNING)
            self.logger.info("Platform Kernel bootstrap completed successfully. Runtime is RUNNING.")

        except Exception as e:
            self.logger.error(f"Platform bootstrap failed: {str(e)}")
            self.transition(RuntimeState.FAILED, metadata={"error": str(e)})
            raise BootstrapException(f"Platform bootstrap failed at state {self._state.value}: {str(e)}") from e

    async def shutdown(self) -> None:
        """Execute graceful 9-stage shutdown."""
        if self._state == RuntimeState.TERMINATED:
            return

        self.logger.info("Initiating platform graceful shutdown...")
        self.transition(RuntimeState.SHUTTING_DOWN)

        # Stage 1: Stop accepting requests
        self.health_manager.set_ready(False)

        # Stage 2: Stop background workers
        await self.background_services.stop()

        # Stage 3: Stop modules
        await self.module_manager.stop_all()

        # Stage 4: Shutdown lifecycle components
        await self.lifecycle_manager.shutdown_all()

        # Stage 5: Finalize state
        self.transition(RuntimeState.TERMINATED)
        self.logger.info("Platform runtime terminated safely.")

    def get_state_history(self) -> List[RuntimeStateEvent]:
        """Return audit history of state transitions."""
        return list(self._state_history)
