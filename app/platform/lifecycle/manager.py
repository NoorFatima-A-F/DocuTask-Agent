"""
Enterprise Lifecycle Manager.
Coordinates platform component dependency resolution, ordered startup, and reverse shutdown.
"""

from collections import deque
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional
from ..kernel.exceptions import LifecycleException
from ..kernel.health import ComponentHealth, HealthStatus
from ..kernel.lifecycle import LifecycleState, LifecycleTransition
from .component import ILifecycleComponent


class LifecycleManager:
    """Manages lifecycle states, startup sequencing, and shutdown tearing down."""

    def __init__(self):
        self._components: Dict[str, ILifecycleComponent] = {}
        self._transitions: List[LifecycleTransition] = []
        self._state = LifecycleState.UNINITIALIZED
        self._listeners: List[Callable[[LifecycleTransition], None]] = []

    @property
    def state(self) -> LifecycleState:
        return self._state

    def register_component(self, component: ILifecycleComponent) -> None:
        """Register a component under lifecycle management."""
        self._components[component.name] = component

    def get_component(self, name: str) -> Optional[ILifecycleComponent]:
        """Get registered component by name."""
        return self._components.get(name)

    def list_components(self) -> List[ILifecycleComponent]:
        """List all registered components."""
        return list(self._components.values())

    def add_transition_listener(self, listener: Callable[[LifecycleTransition], None]) -> None:
        """Add event listener for lifecycle state transitions."""
        self._listeners.append(listener)

    def _record_transition(self, component_id: str, from_state: str, to_state: str, success: bool = True, error: Optional[str] = None) -> None:
        t = LifecycleTransition(
            component_id=component_id,
            from_state=from_state,
            to_state=to_state,
            timestamp=datetime.now(timezone.utc),
            success=success,
            error_message=error,
        )
        self._transitions.append(t)
        for listener in self._listeners:
            try:
                listener(t)
            except Exception:
                pass

    def get_ordered_components(self) -> List[ILifecycleComponent]:
        """Topological sort of components based on their declared dependencies."""
        in_degree: Dict[str, int] = {name: 0 for name in self._components}
        adj: Dict[str, List[str]] = {name: [] for name in self._components}

        for name, comp in self._components.items():
            for dep in comp.dependencies:
                if dep in self._components:
                    adj[dep].append(name)
                    in_degree[name] += 1

        queue = deque([name for name, deg in in_degree.items() if deg == 0])
        ordered_names: List[str] = []

        while queue:
            curr = queue.popleft()
            ordered_names.append(curr)
            for neighbor in adj[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(ordered_names) != len(self._components):
            # Circular dependency detected in components
            missing = set(self._components.keys()) - set(ordered_names)
            raise LifecycleException(f"Circular dependency detected among lifecycle components: {missing}")

        return [self._components[name] for name in ordered_names]

    async def initialize_all(self) -> None:
        """Initialize all registered components in dependency order."""
        self._state = LifecycleState.INITIALIZING
        ordered = self.get_ordered_components()
        for comp in ordered:
            try:
                await comp.initialize()
                self._record_transition(comp.name, LifecycleState.UNINITIALIZED.value, comp.state.value)
            except Exception as e:
                self._record_transition(comp.name, LifecycleState.UNINITIALIZED.value, LifecycleState.FAILED.value, success=False, error=str(e))
                self._state = LifecycleState.FAILED
                raise LifecycleException(f"Failed to initialize component '{comp.name}': {str(e)}") from e
        self._state = LifecycleState.INITIALIZED

    async def start_all(self) -> None:
        """Start all initialized components in dependency order."""
        if self._state != LifecycleState.INITIALIZED:
            await self.initialize_all()

        self._state = LifecycleState.STARTING
        ordered = self.get_ordered_components()
        for comp in ordered:
            try:
                await comp.start()
                self._record_transition(comp.name, LifecycleState.INITIALIZED.value, comp.state.value)
            except Exception as e:
                self._record_transition(comp.name, LifecycleState.INITIALIZED.value, LifecycleState.FAILED.value, success=False, error=str(e))
                self._state = LifecycleState.FAILED
                raise LifecycleException(f"Failed to start component '{comp.name}': {str(e)}") from e
        self._state = LifecycleState.ACTIVE

    async def check_all_health(self) -> Dict[str, ComponentHealth]:
        """Run health check across all registered components."""
        reports: Dict[str, ComponentHealth] = {}
        for name, comp in self._components.items():
            try:
                reports[name] = await comp.health_check()
            except Exception as e:
                reports[name] = ComponentHealth(
                    component_name=name,
                    status=HealthStatus.UNHEALTHY,
                    message=f"Health check threw exception: {str(e)}",
                )
        return reports

    async def shutdown_all(self) -> None:
        """Shutdown all components in reverse dependency order."""
        self._state = LifecycleState.STOPPING
        ordered = self.get_ordered_components()
        # Reverse order for shutdown
        for comp in reversed(ordered):
            try:
                from_st = comp.state.value
                await comp.shutdown()
                self._record_transition(comp.name, from_st, comp.state.value)
            except Exception as e:
                self._record_transition(comp.name, "UNKNOWN", LifecycleState.FAILED.value, success=False, error=str(e))
        self._state = LifecycleState.STOPPED
