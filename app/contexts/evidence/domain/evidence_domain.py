from dataclasses import dataclass, field
from typing import List
from app.shared_kernel import BaseEntity, DomainEvent

@dataclass
class EvidenceCaptured(DomainEvent):
    evidence_id: str = ""
    cas_hash: str = ""

@dataclass
class EvidenceAggregate(BaseEntity):
    run_id: str = ""
    retention_tier: str = "WARM"
    cas_hash: str = ""
    size_bytes: int = 0
    tags: List[str] = field(default_factory=list)
