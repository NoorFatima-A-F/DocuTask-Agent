from dataclasses import dataclass, field
from typing import Dict, Any
from app.shared_kernel import BaseEntity, DomainEvent

@dataclass
class EnvironmentReady(DomainEvent):
    env_id: str = ""
    tier: str = ""

@dataclass
class EnvironmentAggregate(BaseEntity):
    name: str = ""
    tier: str = "STAGING"
    is_ready: bool = True
    profile: Dict[str, Any] = field(default_factory=dict)
