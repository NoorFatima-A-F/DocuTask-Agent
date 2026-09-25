from dataclasses import dataclass, field
from typing import Dict, Any
from app.shared_kernel import BaseEntity, DomainEvent

@dataclass
class ExecutionStarted(DomainEvent):
    execution_id: str = ""
    spec_id: str = ""

@dataclass
class ExecutionCompleted(DomainEvent):
    execution_id: str = ""
    status: str = "COMPLETED"

@dataclass
class ExecutionAggregate(BaseEntity):
    spec_id: str = ""
    status: str = "INITIALIZED"
    attempts: int = 0
    results: Dict[str, Any] = field(default_factory=dict)
