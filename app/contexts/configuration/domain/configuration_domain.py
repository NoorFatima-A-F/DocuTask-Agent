from dataclasses import dataclass, field
from typing import Dict, Any
from app.shared_kernel import BaseEntity, DomainEvent

@dataclass
class ConfigurationSnapshotCreated(DomainEvent):
    config_id: str = ""
    snapshot_hash: str = ""

@dataclass
class ConfigurationAggregate(BaseEntity):
    tier: str = "STAGING"
    parameters: Dict[str, Any] = field(default_factory=dict)
    snapshot_hash: str = ""
