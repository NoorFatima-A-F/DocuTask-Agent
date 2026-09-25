"""
Strongly-Typed Domain Identifiers.
"""
from dataclasses import dataclass
import uuid
from typing import TypeVar, Generic

T = TypeVar("T", bound=str)

@dataclass(frozen=True)
class StronglyTypedId(Generic[T]):
    value: str

    def __str__(self) -> str:
        return self.value

    @classmethod
    def generate(cls, prefix: str = "") -> "StronglyTypedId":
        uid = uuid.uuid4().hex[:12]
        return cls(value=f"{prefix}_{uid}" if prefix else uid)


class CorrelationId(StronglyTypedId):
    @classmethod
    def generate(cls) -> "CorrelationId":
        return cls(value=f"corr_{uuid.uuid4().hex[:12]}")


class ExecutionId(StronglyTypedId):
    @classmethod
    def generate(cls) -> "ExecutionId":
        return cls(value=f"exec_{uuid.uuid4().hex[:12]}")


class TenantId(StronglyTypedId):
    @classmethod
    def default(cls) -> "TenantId":
        return cls(value="default-tenant")


class RunId(StronglyTypedId):
    @classmethod
    def generate(cls) -> "RunId":
        return cls(value=f"vrun_{uuid.uuid4().hex[:12]}")


class DefinitionId(StronglyTypedId):
    @classmethod
    def generate(cls) -> "DefinitionId":
        return cls(value=f"def_{uuid.uuid4().hex[:12]}")


class EntityId(StronglyTypedId):
    @classmethod
    def generate(cls, entity_type: str = "ent") -> "EntityId":
        return cls(value=f"{entity_type}_{uuid.uuid4().hex[:12]}")
