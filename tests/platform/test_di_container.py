"""Tests for Dependency Injection Container."""

import pytest
from app.platform.di.container import DIContainer


def test_di_container_resolution():
    container = DIContainer()
    container.register_instance("config_val", 42)
    container.register_factory("computed_service", lambda c: f"Service with {c.resolve('config_val')}")

    assert container.resolve("config_val") == 42
    assert container.resolve("computed_service") == "Service with 42"

    # Scoped child container
    child = container.create_child_scope()
    child.register_instance("scoped_val", "child_value")
    assert child.resolve("config_val") == 42
    assert child.resolve("scoped_val") == "child_value"

    with pytest.raises(KeyError):
        container.resolve("scoped_val")
