"""
Tests for Enterprise Dependency Injection Container.
"""

import pytest
from app.core.container.container import DependencyContainer, Lifetime
from app.core.container.exceptions import (
    CircularDependencyException,
    ResolutionException,
    ServiceNotFoundException,
)


class IEngine:
    pass


class V8Engine(IEngine):
    def __init__(self, horsepower: int = 450):
        self.horsepower = horsepower


class Car:
    def __init__(self, engine: IEngine):
        self.engine = engine


class NodeA:
    def __init__(self, b: "NodeB"):
        self.b = b


class NodeB:
    def __init__(self, a: "NodeA"):
        self.a = a


def test_container_singleton_registration():
    container = DependencyContainer()
    container.register(IEngine, V8Engine, lifetime=Lifetime.SINGLETON)

    engine1 = container.resolve(IEngine)
    engine2 = container.resolve(IEngine)

    assert isinstance(engine1, V8Engine)
    assert engine1 is engine2


def test_container_transient_registration():
    container = DependencyContainer()
    container.register(IEngine, V8Engine, lifetime=Lifetime.TRANSIENT)

    engine1 = container.resolve(IEngine)
    engine2 = container.resolve(IEngine)

    assert isinstance(engine1, V8Engine)
    assert engine1 is not engine2


def test_container_nested_parameter_resolution():
    container = DependencyContainer()
    container.register(IEngine, V8Engine, lifetime=Lifetime.SINGLETON)
    container.register(Car, Car, lifetime=Lifetime.TRANSIENT)

    car = container.resolve(Car)
    assert isinstance(car, Car)
    assert isinstance(car.engine, V8Engine)
    assert car.engine.horsepower == 450


def test_container_scoped_lifetime():
    container = DependencyContainer()
    container.register(IEngine, V8Engine, lifetime=Lifetime.SCOPED)

    scope1 = container.create_scope()
    scope2 = container.create_scope()

    e1_a = scope1.resolve(IEngine)
    e1_b = scope1.resolve(IEngine)
    e2_a = scope2.resolve(IEngine)

    assert e1_a is e1_b
    assert e1_a is not e2_a


def test_container_circular_dependency_detection():
    container = DependencyContainer()
    container.register(NodeA, NodeA)
    container.register(NodeB, NodeB)

    with pytest.raises(CircularDependencyException) as exc_info:
        container.resolve(NodeA)

    assert "Circular dependency cycle detected" in str(exc_info.value)


def test_container_test_override():
    container = DependencyContainer()
    container.register(IEngine, V8Engine)

    class MockEngine(IEngine):
        pass

    container.override(IEngine, MockEngine)
    resolved = container.resolve(IEngine)
    assert isinstance(resolved, MockEngine)

    container.clear_overrides()
    resolved_after = container.resolve(IEngine)
    assert isinstance(resolved_after, V8Engine)
