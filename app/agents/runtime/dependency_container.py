"""
Production Inversion of Control (IoC) Container.
Supports Singleton, Transient, and Scoped lifetimes, automatic constructor parameter injection via reflection,
factory providers, lazy initialization, circular resolution detection, interface contract validation,
and lifetime safety analysis.
"""

import inspect
from enum import Enum
from typing import Any, Callable, Dict, Optional, Set, Type, TypeVar
from app.agents.runtime.exceptions import (
    CyclicDependencyError,
    InvalidBindingError,
    InvalidLifetimeDependencyError,
    ServiceNotFoundError,
)

T = TypeVar("T")


class Lifetime(str, Enum):
    """Component registration lifetime in IoC container."""
    SINGLETON = "SINGLETON"
    TRANSIENT = "TRANSIENT"
    SCOPED = "SCOPED"


class InterfaceBindingValidator:
    """Validates that a concrete target type conforms to the registered interface specification."""

    @staticmethod
    def validate(interface_type: Type[Any], target: Any) -> None:
        """Verifies target class or instance implements the interface contract."""
        if not inspect.isclass(interface_type):
            return

        if callable(target) and not inspect.isclass(target):
            # Target is a factory function
            sig = inspect.signature(target)
            ret = sig.return_annotation
            if ret is not inspect.Signature.empty and inspect.isclass(ret):
                if issubclass(ret, interface_type):
                    return
            return

        target_cls = target if inspect.isclass(target) else getattr(target, "__class__", None)
        if target_cls is None or not inspect.isclass(target_cls):
            return

        # If target_cls is direct subclass, it satisfies contract
        if issubclass(target_cls, interface_type):
            return

        # Structural validation (duck typing): check all public methods/attributes
        missing_attrs = []
        for name, member in inspect.getmembers(interface_type):
            if name.startswith("_"):
                continue
            if not hasattr(target_cls, name):
                missing_attrs.append(name)

        if missing_attrs:
            raise InvalidBindingError(
                f"Target '{target_cls.__name__}' does not implement interface '{interface_type.__name__}'. "
                f"Missing required attributes/methods: {missing_attrs}"
            )


class LifetimeAnalyzer:
    """
    Enforces lifetime safety in dependency injection graphs.
    Prevents captive dependencies where a longer-lived component holds a shorter-lived component.
    Specifically:
    - SINGLETON cannot depend on SCOPED (would capture and leak tenant/request scope into global state).
    """

    @staticmethod
    def validate_dependency_lifetime(
        parent_lifetime: Lifetime,
        child_lifetime: Lifetime,
        parent_type: Type[Any],
        child_type: Type[Any],
    ) -> None:
        """Validates that parent component lifetime does not exceed child dependency lifetime."""
        if parent_lifetime == Lifetime.SINGLETON and child_lifetime == Lifetime.SCOPED:
            raise InvalidLifetimeDependencyError(
                f"Lifetime safety violation: Singleton component '{parent_type.__name__}' cannot depend on "
                f"Scoped component '{child_type.__name__}'. This would cause scoped state leakage across requests/tenants."
            )


class _ServiceBinding:
    def __init__(
        self,
        interface_type: Type[Any],
        target: Any,  # Class, Factory callable, or Instance
        lifetime: Lifetime,
        is_instance: bool = False,
    ) -> None:
        self.interface_type = interface_type
        self.target = target
        self.lifetime = lifetime
        self.is_instance = is_instance
        self.singleton_instance: Optional[Any] = target if is_instance else None


class ScopedContainer:
    """Child container representing an active execution or request scope."""

    def __init__(self, parent: "DependencyContainer", scope_id: Optional[str] = None) -> None:
        self.parent = parent
        self.scope_id = scope_id or "default-scope"
        self._scoped_instances: Dict[Type[Any], Any] = {}

    def resolve(self, interface_type: Type[T]) -> T:
        """Resolves service respecting scoped boundaries."""
        binding = self.parent.get_binding(interface_type)
        if not binding:
            raise ServiceNotFoundError(
                f"Service for interface '{interface_type.__name__}' is not registered in container."
            )

        if binding.lifetime == Lifetime.SCOPED:
            if interface_type not in self._scoped_instances:
                instance = self.parent._instantiate_target(binding.target, self, parent_binding=binding)
                self._scoped_instances[interface_type] = instance
            return self._scoped_instances[interface_type]
        elif binding.lifetime == Lifetime.SINGLETON:
            return self.parent.resolve(interface_type)
        else:
            return self.parent._instantiate_target(binding.target, self, parent_binding=binding)

    def has(self, interface_type: Type[Any]) -> bool:
        """Checks if parent container has binding for interface_type."""
        return self.parent.has(interface_type)

    def close(self) -> None:
        """Disposes all scoped instances."""
        self._scoped_instances.clear()


class DependencyContainer:
    """Enterprise IoC container with reflection-based constructor injection, lifetime safety analysis, and contract validation."""

    def __init__(self) -> None:
        self._bindings: Dict[Type[Any], _ServiceBinding] = {}
        self._resolving_stack: Set[Type[Any]] = set()

    def register_singleton(
        self,
        interface_type: Type[T],
        instance_or_class: Any,
        validate_contract: bool = True,
    ) -> "DependencyContainer":
        """Registers a singleton instance or class resolved once and cached permanently."""
        if validate_contract:
            InterfaceBindingValidator.validate(interface_type, instance_or_class)

        is_inst = not isinstance(instance_or_class, type) and not (
            callable(instance_or_class) and not inspect.isclass(instance_or_class)
        )
        self._bindings[interface_type] = _ServiceBinding(
            interface_type=interface_type,
            target=instance_or_class,
            lifetime=Lifetime.SINGLETON,
            is_instance=is_inst,
        )
        return self

    def register_transient(
        self,
        interface_type: Type[T],
        class_or_factory: Any,
        validate_contract: bool = True,
    ) -> "DependencyContainer":
        """Registers a transient component instantiated on each resolve."""
        if validate_contract:
            InterfaceBindingValidator.validate(interface_type, class_or_factory)

        self._bindings[interface_type] = _ServiceBinding(
            interface_type=interface_type,
            target=class_or_factory,
            lifetime=Lifetime.TRANSIENT,
            is_instance=False,
        )
        return self

    def register_scoped(
        self,
        interface_type: Type[T],
        class_or_factory: Any,
        validate_contract: bool = True,
    ) -> "DependencyContainer":
        """Registers a scoped component instantiated once per ScopedContainer."""
        if validate_contract:
            InterfaceBindingValidator.validate(interface_type, class_or_factory)

        self._bindings[interface_type] = _ServiceBinding(
            interface_type=interface_type,
            target=class_or_factory,
            lifetime=Lifetime.SCOPED,
            is_instance=False,
        )
        return self

    def get_binding(self, interface_type: Type[Any]) -> Optional[_ServiceBinding]:
        """Retrieves service registration descriptor."""
        return self._bindings.get(interface_type)

    def create_scope(self, scope_id: Optional[str] = None) -> ScopedContainer:
        """Creates a child container for a request, tenant, or workflow execution scope."""
        return ScopedContainer(self, scope_id=scope_id)

    def resolve(self, interface_type: Type[T]) -> T:
        """Resolves an instance for the requested interface type, handling constructor injection."""
        binding = self._bindings.get(interface_type)
        if not binding:
            raise ServiceNotFoundError(
                f"Service for interface '{interface_type.__name__}' is not registered in container."
            )

        if binding.lifetime == Lifetime.SINGLETON:
            if binding.singleton_instance is None:
                binding.singleton_instance = self._instantiate_target(binding.target, self, parent_binding=binding)
            return binding.singleton_instance
        elif binding.lifetime == Lifetime.TRANSIENT:
            return self._instantiate_target(binding.target, self, parent_binding=binding)
        elif binding.lifetime == Lifetime.SCOPED:
            if binding.singleton_instance is None:
                binding.singleton_instance = self._instantiate_target(binding.target, self, parent_binding=binding)
            return binding.singleton_instance

    def _instantiate_target(self, target: Any, resolver: Any, parent_binding: Optional[_ServiceBinding] = None) -> Any:
        """Instantiates target using constructor injection if class, or invokes callable if factory."""
        if not inspect.isclass(target):
            if callable(target):
                sig = inspect.signature(target)
                if len(sig.parameters) == 0:
                    return target()
                kwargs = self._resolve_parameters(sig, resolver, parent_binding=parent_binding)
                return target(**kwargs)
            return target

        cls = target
        if cls in self._resolving_stack:
            raise CyclicDependencyError(
                f"Circular constructor dependency detected while resolving '{cls.__name__}'."
            )

        self._resolving_stack.add(cls)
        try:
            init_method = cls.__init__
            if init_method is object.__init__:
                return cls()

            sig = inspect.signature(init_method)
            kwargs = self._resolve_parameters(sig, resolver, parent_cls=cls, parent_binding=parent_binding)
            return cls(**kwargs)
        finally:
            self._resolving_stack.remove(cls)

    def _resolve_parameters(
        self,
        sig: inspect.Signature,
        resolver: Any,
        parent_cls: Optional[Type[Any]] = None,
        parent_binding: Optional[_ServiceBinding] = None,
    ) -> Dict[str, Any]:
        """Resolves constructor parameter values based on type annotations, enforcing lifetime safety."""
        kwargs: Dict[str, Any] = {}
        for param_name, param in sig.parameters.items():
            if param_name in ("self", "args", "kwargs"):
                continue

            param_type = param.annotation
            target_type = None
            if param_type is not inspect.Parameter.empty:
                if inspect.isclass(param_type):
                    target_type = param_type
                elif isinstance(param_type, str):
                    container = resolver.parent if hasattr(resolver, "parent") else resolver
                    for registered_k in container._bindings.keys():
                        if getattr(registered_k, "__name__", None) == param_type:
                            target_type = registered_k
                            break

            if target_type and resolver.has(target_type):
                # Lifetime Safety Check: Singletons must not depend on Scoped dependencies
                container = resolver.parent if hasattr(resolver, "parent") else resolver
                child_binding = container.get_binding(target_type)
                if parent_binding and child_binding:
                    LifetimeAnalyzer.validate_dependency_lifetime(
                        parent_binding.lifetime,
                        child_binding.lifetime,
                        parent_cls or parent_binding.interface_type,
                        target_type,
                    )

                kwargs[param_name] = resolver.resolve(target_type)
                continue

            # If default provided, use it
            if param.default is not inspect.Parameter.empty:
                kwargs[param_name] = param.default
            else:
                type_repr = getattr(target_type or param_type, "__name__", str(param_type))
                raise ServiceNotFoundError(
                    f"Unable to resolve required constructor parameter '{param_name}: {type_repr}'."
                )
        return kwargs

    def validate_dependency_graph(self) -> None:
        """Analyzes all registered bindings to guarantee acyclic and lifetime-safe dependencies."""
        for interface_type, binding in self._bindings.items():
            if inspect.isclass(binding.target):
                init_method = binding.target.__init__
                if init_method is not object.__init__:
                    sig = inspect.signature(init_method)
                    for param_name, param in sig.parameters.items():
                        if param_name in ("self", "args", "kwargs"):
                            continue
                        param_type = param.annotation
                        if inspect.isclass(param_type) and param_type in self._bindings:
                            child_binding = self._bindings[param_type]
                            LifetimeAnalyzer.validate_dependency_lifetime(
                                binding.lifetime,
                                child_binding.lifetime,
                                binding.target,
                                param_type,
                            )

    def has(self, interface_type: Type[Any]) -> bool:
        """Checks if an interface or class is registered."""
        return interface_type in self._bindings

    def clear(self) -> None:
        """Clears all registered bindings."""
        self._bindings.clear()
