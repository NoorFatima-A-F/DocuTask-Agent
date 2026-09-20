from dataclasses import dataclass, field
from typing import Dict, Any
from app.shared_kernel import BaseEntity, DomainEvent

@dataclass
class AuditRecordAppended(DomainEvent):
    record_id: str = ""
    event_type: str = ""

@dataclass
class AuditRecordAggregate(BaseEntity):
    sequence: int = 1
    event_type: str = ""
    actor: str = "SYSTEM"
    prev_hash: str = "0" * 64
    record_hash: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
