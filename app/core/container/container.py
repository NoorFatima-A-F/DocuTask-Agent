"""
Enterprise Dependency Injection Container.
Provides registration, resolution, scoped child containers, lifetime management,
circular dependency detection, and testing overrides.
"""

from contextlib import contextmanager
import inspect
import sys
from typing import Any, Callable, Dict, Iterator, List, Optional, Set, Type, TypeVar, Union
from .exceptions import (
    CircularDependencyException,
    ContainerException,
    ResolutionException,
    ServiceNotFoundException,
)
from .lifetimes import Lifetime

T = TypeVar("T")


class ServiceDescriptor:
    """Internal registration descriptor for a dependency."""

    def __init__(
        self,
        service_type: Type[Any],
        implementation_type: Optional[Type[Any]] = None,
        factory: Optional[Callable[["DependencyContainer"], Any]] = None,
        instance: Optional[Any] = None,
        lifetime: Lifetime = Lifetime.TRANSIENT,
    ):
        self.service_type = service_type
        self.implementation_type = implementation_type or service_type
        self.factory = factory
        self.instance = instance
        self.lifetime = lifetime


class DependencyScope:
    """Scoped container for request/session lifetime resolution."""

    def __init__(self, parent_container: "DependencyContainer"):
        self._parent = parent_container
        self._scoped_instances: Dict[Type[Any], Any] = {}
        self._resolving_stack: List[Type[Any]] = []

    def resolve(self, service_type: Type[T]) -> T:
        """Resolve a service within this specific scope."""
        return self._parent._resolve_internal(service_type, scope=self)

    def register_instance(self, service_type: Type[T], instance: T) -> None:
        """Register an instance directly into this scope."""
        self._scoped_instances[service_type] = instance

    def close(self) -> None:
        """Clean up all scoped instances."""
        self._scoped_instances.clear()

    def __enter__(self) -> "DependencyScope":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


class DependencyContainer:
    """
    Central Dependency Injection Container for DocuTask Agent.
    """

    def __init__(self, parent: Optional["DependencyContainer"] = None):
        self._descriptors: Dict[Type[Any], ServiceDescriptor] = {}
        self._singletons: Dict[Type[Any], Any] = {}
        self._overrides: Dict[Type[Any], ServiceDescriptor] = {}
        self._parent = parent
        self._resolving_stack: List[Type[Any]] = []

    def register(
        self,
        service_type: Type[T],
        implementation: Optional[Type[Any]] = None,
        lifetime: Lifetime = Lifetime.TRANSIENT,
        factory: Optional[Callable[["DependencyContainer"], T]] = None,
        instance: Optional[T] = None,
    ) -> "DependencyContainer":
        """Register a dependency with specified lifetime."""
        if instance is not None:
            descriptor = ServiceDescriptor(
                service_type=service_type,
                instance=instance,
                lifetime=Lifetime.SINGLETON,
            )
            self._singletons[service_type] = instance
        else:
            descriptor = ServiceDescriptor(
                service_type=service_type,
                implementation_type=implementation,
                factory=factory,
                lifetime=lifetime,
            )
        self._descriptors[service_type] = descriptor
        return self

    def register_singleton(
        self,
        service_type: Type[T],
        implementation: Optional[Type[Any]] = None,
        factory: Optional[Callable[["DependencyContainer"], T]] = None,
        instance: Optional[T] = None,
    ) -> "DependencyContainer":
        """Convenience method for registering a singleton."""
        return self.register(
            service_type=service_type,
            implementation=implementation,
            lifetime=Lifetime.SINGLETON,
            factory=factory,
            instance=instance,
        )

    def register_instance(
        self,
        service_type: Type[T],
        instance: T,
    ) -> "DependencyContainer":
        """Convenience method for registering a direct singleton instance."""
        return self.register(
            service_type=service_type,
            instance=instance,
            lifetime=Lifetime.SINGLETON,
        )

    def register_scoped(
        self,
        service_type: Type[T],
        implementation: Optional[Type[Any]] = None,
        factory: Optional[Callable[["DependencyContainer"], T]] = None,
    ) -> "DependencyContainer":
        """Convenience method for registering a scoped dependency."""
        return self.register(
            service_type=service_type,
            implementation=implementation,
            lifetime=Lifetime.SCOPED,
            factory=factory,
        )

    def register_transient(
        self,
        service_type: Type[T],
        implementation: Optional[Type[Any]] = None,
        factory: Optional[Callable[["DependencyContainer"], T]] = None,
    ) -> "DependencyContainer":
        """Convenience method for registering a transient dependency."""
        return self.register(
            service_type=service_type,
            implementation=implementation,
            lifetime=Lifetime.TRANSIENT,
            factory=factory,
        )

    def override(
        self,
        service_type: Type[T],
        implementation: Optional[Type[Any]] = None,
        factory: Optional[Callable[["DependencyContainer"], T]] = None,
        instance: Optional[T] = None,
    ) -> "DependencyContainer":
        """Register a temporary test override."""
        if instance is not None:
            descriptor = ServiceDescriptor(
                service_type=service_type,
                instance=instance,
                lifetime=Lifetime.SINGLETON,
            )
        else:
            descriptor = ServiceDescriptor(
                service_type=service_type,
                implementation_type=implementation,
                factory=factory,
                lifetime=Lifetime.TRANSIENT,
            )
        self._overrides[service_type] = descriptor
        return self

    def clear_overrides(self) -> None:
        """Clear all test overrides."""
        self._overrides.clear()

    def is_registered(self, service_type: Type[Any]) -> bool:
        """Check if a service type is registered."""
        if service_type in self._overrides or service_type in self._descriptors:
            return True
        if self._parent and self._parent.is_registered(service_type):
            return True
        return False

    def create_scope(self) -> DependencyScope:
        """Create a new scoped container instance."""
        return DependencyScope(self)

    def resolve(self, service_type: Type[T]) -> T:
        """Resolve a service dependency."""
        return self._resolve_internal(service_type, scope=None)

    def _resolve_internal(
        self,
        service_type: Type[T],
        scope: Optional[DependencyScope] = None,
    ) -> T:
        # Check active resolution stack for circular dependencies
        type_name = service_type.__name__ if hasattr(service_type, "__name__") else str(service_type)
        if service_type in self._resolving_stack:
            cycle = [t.__name__ if hasattr(t, "__name__") else str(t) for t in self._resolving_stack] + [type_name]
            raise CircularDependencyException(cycle)

        # 1. Check overrides first
        descriptor = self._overrides.get(service_type)

        # 2. Check local registrations
        if descriptor is None:
            descriptor = self._descriptors.get(service_type)

        # 3. Check parent container if present
        if descriptor is None and self._parent:
            return self._parent._resolve_internal(service_type, scope=scope)

        # 4. If still not found, check if it's a concrete class that can be auto-instantiated
        if descriptor is None:
            if inspect.isclass(service_type) and not inspect.isabstract(service_type):
                descriptor = ServiceDescriptor(
                    service_type=service_type,
                    implementation_type=service_type,
                    lifetime=Lifetime.TRANSIENT,
                )
            else:
                raise ServiceNotFoundException(service_type)

        # Handle Singleton lifetime
        if descriptor.lifetime == Lifetime.SINGLETON:
            if descriptor.instance is not None:
                return descriptor.instance
            if service_type in self._singletons:
                return self._singletons[service_type]

        # Handle Scoped lifetime
        if descriptor.lifetime == Lifetime.SCOPED and scope is not None:
            if service_type in scope._scoped_instances:
                return scope._scoped_instances[service_type]

        # Push to resolution stack
        self._resolving_stack.append(service_type)
        try:
            instance = self._create_instance(descriptor, scope=scope)
        finally:
            self._resolving_stack.pop()

        # Cache according to lifetime
        if descriptor.lifetime == Lifetime.SINGLETON:
            self._singletons[service_type] = instance
        elif descriptor.lifetime == Lifetime.SCOPED and scope is not None:
            scope._scoped_instances[service_type] = instance

        return instance

    def _create_instance(
        self,
        descriptor: ServiceDescriptor,
        scope: Optional[DependencyScope] = None,
    ) -> Any:
        # Factory creation
        if descriptor.factory:
            return descriptor.factory(self)

        # Direct instance
        if descriptor.instance is not None:
            return descriptor.instance

        target_cls = descriptor.implementation_type or descriptor.service_type
        if not inspect.isclass(target_cls):
            raise ResolutionException(descriptor.service_type, f"Target {target_cls} is not a valid class")

        init_sig = inspect.signature(target_cls.__init__)
        params = init_sig.parameters
        kwargs = {}

        for param_name, param in params.items():
            if param_name in ("self", "args", "kwargs"):
                continue

            param_type = param.annotation
            if isinstance(param_type, str):
                # Try to resolve string annotation in target class module
                target_mod = sys.modules.get(target_cls.__module__)
                if target_mod and hasattr(target_mod, param_type):
                    param_type = getattr(target_mod, param_type)
                else:
                    # Search registered descriptor keys by name
                    for reg_type in self._descriptors:
                        if hasattr(reg_type, "__name__") and reg_type.__name__ == param_type:
                            param_type = reg_type
                            break

            if param_type is inspect.Parameter.empty or param_type is Any:
                # If no type annotation, check if there's a default value
                if param.default is not inspect.Parameter.empty:
                    kwargs[param_name] = param.default
                else:
                    raise ResolutionException(
                        descriptor.service_type,
                        f"Cannot resolve unannotated parameter '{param_name}' without default",
                    )
            elif not self.is_registered(param_type) and param.default is not inspect.Parameter.empty:
                kwargs[param_name] = param.default
            else:
                try:
                    kwargs[param_name] = self._resolve_internal(param_type, scope=scope)
                except ServiceNotFoundException:
                    if param.default is not inspect.Parameter.empty:
                        kwargs[param_name] = param.default
                    else:
                        raise ResolutionException(
                            descriptor.service_type,
                            f"Missing dependency '{param_name}' of type {param_type}",
                        )

        try:
            return target_cls(**kwargs)
        except Exception as e:
            raise ResolutionException(descriptor.service_type, f"Instantiation failed: {str(e)}", e)
