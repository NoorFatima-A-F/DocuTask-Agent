"""IoC Dependency Injection Container.

Provides scoped dependency injection for plugins, ensuring no plugin directly accesses
global runtime singletons and all services are lifecycle-managed and mockable.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Type


class DIContainer:
    def __init__(self):
        self._singletons: Dict[str, Any] = {}
        self._factories: Dict[str, Callable[['DIContainer'], Any]] = {}
        self._types: Dict[Type[Any], Any] = {}

    def register_instance(self, key: str, instance: Any) -> None:
        self._singletons[key] = instance

    def register_factory(self, key: str, factory: Callable[['DIContainer'], Any]) -> None:
        self._factories[key] = factory

    def register_type(self, interface_cls: Type[Any], implementation: Any) -> None:
        self._types[interface_cls] = implementation

    def resolve(self, key: str) -> Any:
        if key in self._singletons:
            return self._singletons[key]
        if key in self._factories:
            instance = self._factories[key](self)
            self._singletons[key] = instance
            return instance
        raise KeyError(f"Service '{key}' not registered in DI container")

    def resolve_type(self, interface_cls: Type[Any]) -> Any:
        if interface_cls in self._types:
            return self._types[interface_cls]
        raise KeyError(f"Interface '{interface_cls.__name__}' not registered in DI container")

    def create_child_scope(self) -> 'DIContainer':
        child = DIContainer()
        child._singletons.update(self._singletons)
        child._factories.update(self._factories)
        child._types.update(self._types)
        return child


class ServiceProvider:
    @staticmethod
    def build_default_container() -> DIContainer:
        container = DIContainer()
        from app.runtime.evidence.evidence_collector import global_evidence_collector
        from app.runtime.decision_ledger.decision_ledger import global_decision_ledger
        from app.runtime.tool_ledger.tool_execution_ledger import global_tool_ledger
        from app.platform.capability.capability_registry import global_capability_registry

        container.register_instance("evidence_collector", global_evidence_collector)
        container.register_instance("decision_ledger", global_decision_ledger)
        container.register_instance("tool_ledger", global_tool_ledger)
        container.register_instance("capability_registry", global_capability_registry)
        return container


global_di_container = ServiceProvider.build_default_container()
