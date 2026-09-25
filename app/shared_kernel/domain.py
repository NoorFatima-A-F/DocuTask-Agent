"""
Core Domain Primitives for DDD and Hexagonal Architecture.
Pure business-agnostic abstractions for Entities, Aggregates, Value Objects, and Specifications.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Generic, TypeVar, Optional, List

T = TypeVar("T")
ID = TypeVar("ID")

@dataclass(frozen=True)
class ValueObject(ABC):
    """Immutable Value Object base class."""
    pass

@dataclass
class BaseEntity(ABC):
    """Base Entity with identity equality and audit timestamps."""
    id: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: int = 1

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id and type(self) is type(other)

    def __hash__(self) -> int:
        return hash((self.__class__, self.id))

@dataclass
class Entity(BaseEntity, Generic[ID]):
    """Generic Entity with strongly-typed identity."""
    id: ID # type: ignore[assignment]

@dataclass
class AggregateRoot(Entity[ID]):
    """Aggregate Root managing domain invariants and local domain events."""
    _domain_events: List[Any] = field(default_factory=list, init=False, repr=False)

    def record_event(self, event: Any) -> None:
        self._domain_events.append(event)

    def pull_domain_events(self) -> List[Any]:
        events = list(self._domain_events)
        self._domain_events.clear()
        return events

class DomainServiceMarker:
    """Marker class/interface for pure domain services without state."""
    pass

class Specification(ABC, Generic[T]):
    """Specification pattern for composable business and query rules."""
    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        pass

    def and_(self, other: "Specification[T]") -> "Specification[T]":
        return _AndSpecification(self, other)

    def or_(self, other: "Specification[T]") -> "Specification[T]":
        return _OrSpecification(self, other)

    def not_(self) -> "Specification[T]":
        return _NotSpecification(self)

class _AndSpecification(Specification[T]):
    def __init__(self, left: Specification[T], right: Specification[T]):
        self.left = left
        self.right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self.left.is_satisfied_by(candidate) and self.right.is_satisfied_by(candidate)

class _OrSpecification(Specification[T]):
    def __init__(self, left: Specification[T], right: Specification[T]):
        self.left = left
        self.right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self.left.is_satisfied_by(candidate) or self.right.is_satisfied_by(candidate)

class _NotSpecification(Specification[T]):
    def __init__(self, spec: Specification[T]):
        self.spec = spec

    def is_satisfied_by(self, candidate: T) -> bool:
        return not self.spec.is_satisfied_by(candidate)

class RepositoryContract(ABC, Generic[T, ID]):
    """Generic Repository Port Contract."""
    @abstractmethod
    async def get_by_id(self, entity_id: ID) -> Optional[T]:
        pass

    @abstractmethod
    async def save(self, entity: T) -> None:
        pass

    @abstractmethod
    async def delete(self, entity_id: ID) -> None:
        pass

class UnitOfWorkContract(ABC):
    """Generic Unit of Work Port Contract for atomic transaction boundaries."""
    @abstractmethod
    async def __aenter__(self) -> "UnitOfWorkContract":
        pass

    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass
