from dataclasses import dataclass, field
from typing import List, Dict, Any
from app.shared_kernel import BaseEntity, DomainEvent

@dataclass
class VerificationDefinitionCreated(DomainEvent):
    definition_id: str = ""
    name: str = ""

@dataclass
class VerificationDefinition(BaseEntity):
    name: str = ""
    invariants: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
