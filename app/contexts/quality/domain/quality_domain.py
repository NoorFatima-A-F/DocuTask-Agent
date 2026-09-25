from dataclasses import dataclass, field
from typing import List
from app.shared_kernel import BaseEntity, DomainEvent

@dataclass
class QualityGateEvaluated(DomainEvent):
    gate_id: str = ""
    passed: bool = True

@dataclass
class QualityGateAggregate(BaseEntity):
    run_id: str = ""
    is_passed: bool = True
    blockers: List[str] = field(default_factory=list)
