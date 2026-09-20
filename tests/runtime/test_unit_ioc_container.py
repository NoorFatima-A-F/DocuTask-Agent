"""
Unit test suite for DependencyContainer and ScopedContainer.
Validates singleton, transient, scoped lifetimes, constructor parameter injection,
circular dependency detection, and exception scenarios.
"""

import pytest
from typing import Any
from app.agents.runtime.dependency_container import DependencyContainer, Lifetime, ScopedContainer
from app.agents.runtime.exceptions import (
    CyclicDependencyError,
    ServiceNotFoundError,
)


class ILogger:
    def log(self, msg: str) -> str:
        raise NotImplementedError


class ConsoleLogger(ILogger):
    def log(self, msg: str) -> str:
        return f"[LOG] {msg}"


class IDatabase:
    def query(self) -> str:
        raise NotImplementedError


class PostgresDatabase(IDatabase):
    def __init__(self, logger: ILogger) -> None:
        self.logger = logger

    def query(self) -> str:
        return f"postgres:{self.logger.log('query')}"


class UserRepository:
    def __init__(self, db: IDatabase) -> None:
        self.db = db


class CircularA:
    def __init__(self, b: "CircularB") -> None:
        self.b = b


class CircularB:
    def __init__(self, a: CircularA) -> None:
        self.a = a


class DefaultParamService:
    def __init__(self, name: str = "default_service") -> None:
        self.name = name


class MissingParamService:
    def __init__(self, unreg: IDatabase) -> None:
        self.unreg = unreg


def test_singleton_registration_and_resolution():
    container = DependencyContainer()
    logger_instance = ConsoleLogger()
    container.register_singleton(ILogger, logger_instance)

    resolved_1 = container.resolve(ILogger)
    resolved_2 = container.resolve(ILogger)

    assert resolved_1 is logger_instance
    assert resolved_2 is logger_instance
    assert resolved_1 is resolved_2


def test_singleton_class_registration_instantiates_once():
    container = DependencyContainer()
    container.register_singleton(ILogger, ConsoleLogger)

    resolved_1 = container.resolve(ILogger)
    resolved_2 = container.resolve(ILogger)

    assert isinstance(resolved_1, ConsoleLogger)
    assert resolved_1 is resolved_2


def test_transient_registration_creates_fresh_instances():
    container = DependencyContainer()
    container.register_transient(ILogger, ConsoleLogger)

    resolved_1 = container.resolve(ILogger)
    resolved_2 = container.resolve(ILogger)

    assert isinstance(resolved_1, ConsoleLogger)
    assert isinstance(resolved_2, ConsoleLogger)
    assert resolved_1 is not resolved_2


def test_constructor_injection_nested_resolution():
    container = DependencyContainer()
    container.register_singleton(ILogger, ConsoleLogger)
    container.register_transient(IDatabase, PostgresDatabase)
    container.register_transient(UserRepository, UserRepository)

    repo = container.resolve(UserRepository)
    assert isinstance(repo, UserRepository)
    assert isinstance(repo.db, PostgresDatabase)
    assert isinstance(repo.db.logger, ConsoleLogger)
    assert repo.db.query() == "postgres:[LOG] query"


def test_scoped_lifetime_per_scope_isolation():
    container = DependencyContainer()
    container.register_singleton(ILogger, ConsoleLogger)
    container.register_scoped(IDatabase, PostgresDatabase)

    scope1 = container.create_scope(scope_id="scope-1")
    scope2 = container.create_scope(scope_id="scope-2")

    db_scope1_a = scope1.resolve(IDatabase)
    db_scope1_b = scope1.resolve(IDatabase)

    db_scope2_a = scope2.resolve(IDatabase)

    # Within scope 1, instances are identical
    assert db_scope1_a is db_scope1_b
    # Across scopes, instances are distinct
    assert db_scope1_a is not db_scope2_a
    # But singleton dependencies inside them are identical
    assert db_scope1_a.logger is db_scope2_a.logger


def test_circular_dependency_detection_raises_cyclic_error():
    container = DependencyContainer()
    container.register_transient(CircularA, CircularA)
    container.register_transient(CircularB, CircularB)

    with pytest.raises(CyclicDependencyError) as exc_info:
        container.resolve(CircularA)
    assert "Circular constructor dependency detected" in str(exc_info.value)


def test_service_not_found_raises_service_not_found_error():
    container = DependencyContainer()
    with pytest.raises(ServiceNotFoundError) as exc_info:
        container.resolve(IDatabase)
    assert "Service for interface 'IDatabase' is not registered" in str(exc_info.value)


def test_unregistered_constructor_parameter_raises_service_not_found_error():
    container = DependencyContainer()
    container.register_transient(MissingParamService, MissingParamService)

    with pytest.raises(ServiceNotFoundError) as exc_info:
        container.resolve(MissingParamService)
    assert "Unable to resolve required constructor parameter 'unreg: IDatabase'" in str(exc_info.value)


def test_default_parameter_injection():
    container = DependencyContainer()
    container.register_transient(DefaultParamService, DefaultParamService)

    service = container.resolve(DefaultParamService)
    assert service.name == "default_service"


def test_factory_function_registration():
    container = DependencyContainer()
    container.register_singleton(ILogger, ConsoleLogger)

    def db_factory(logger: ILogger) -> IDatabase:
        return PostgresDatabase(logger=logger)

    container.register_transient(IDatabase, db_factory)
    db = container.resolve(IDatabase)
    assert isinstance(db, PostgresDatabase)
    assert db.logger.log("factory") == "[LOG] factory"


def test_container_has_and_clear():
    container = DependencyContainer()
    assert not container.has(ILogger)
    container.register_singleton(ILogger, ConsoleLogger)
    assert container.has(ILogger)

    scope = container.create_scope()
    assert scope.has(ILogger)

    container.clear()
    assert not container.has(ILogger)


def test_scoped_container_close_clears_instances():
    container = DependencyContainer()
    container.register_singleton(ILogger, ConsoleLogger)
    container.register_scoped(IDatabase, PostgresDatabase)

    scope = container.create_scope()
    db1 = scope.resolve(IDatabase)
    scope.close()
    db2 = scope.resolve(IDatabase)

    assert db1 is not db2


class IStorageProvider:
    def store(self, key: str, value: str) -> None:
        raise NotImplementedError


class BadStorageImplementation:
    # Does not implement store()
    def save_data(self, data: str) -> None:
        pass


class ValidStorageImplementation(IStorageProvider):
    def store(self, key: str, value: str) -> None:
        pass


class TenantContext:
    def __init__(self, tenant_id: str = "tenant-1") -> None:
        self.tenant_id = tenant_id


class GlobalDatabaseService:
    # Singleton depending on Scoped TenantContext
    def __init__(self, context: TenantContext) -> None:
        self.context = context


def test_interface_contract_validation():
    from app.agents.runtime.exceptions import InvalidBindingError
    container = DependencyContainer()

    # Valid binding succeeds
    container.register_singleton(IStorageProvider, ValidStorageImplementation)

    # Invalid binding rejected with InvalidBindingError
    with pytest.raises(InvalidBindingError) as exc_info:
        container.register_singleton(IStorageProvider, BadStorageImplementation)
    assert "Missing required attributes/methods" in str(exc_info.value)


def test_invalid_lifetime_dependency():
    from app.agents.runtime.exceptions import InvalidLifetimeDependencyError
    container = DependencyContainer()
    container.register_scoped(TenantContext, TenantContext)
    container.register_singleton(GlobalDatabaseService, GlobalDatabaseService)

    # Resolving Singleton that depends on Scoped must raise InvalidLifetimeDependencyError
    with pytest.raises(InvalidLifetimeDependencyError) as exc_info:
        container.resolve(GlobalDatabaseService)
    assert "Lifetime safety violation" in str(exc_info.value)
    assert "GlobalDatabaseService" in str(exc_info.value)
    assert "TenantContext" in str(exc_info.value)


def test_dependency_graph_lifetime_analysis():
    from app.agents.runtime.exceptions import InvalidLifetimeDependencyError
    container = DependencyContainer()
    container.register_scoped(TenantContext, TenantContext)
    container.register_singleton(GlobalDatabaseService, GlobalDatabaseService)

    # Static analysis of graph detects violation prior to resolution
    with pytest.raises(InvalidLifetimeDependencyError) as exc_info:
        container.validate_dependency_graph()
    assert "Lifetime safety violation" in str(exc_info.value)

