"""
Base DDD Entity and ValueObject abstractions for the Enterprise Verification Platform.
"""
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

@dataclass
class BaseEntity(ABC):
    id: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: int = 1

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id and type(self) is type(other)

    def __hash__(self) -> int:
        return hash((self.__class__, self.id))

@dataclass(frozen=True)
class ValueObject(ABC):
    pass
