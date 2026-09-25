from dataclasses import dataclass, field
from typing import List
from app.shared_kernel import BaseEntity, DomainEvent

@dataclass
class PluginRegistered(DomainEvent):
    plugin_id: str = ""
    name: str = ""

@dataclass
class PluginRegistryAggregate(BaseEntity):
    name: str = ""
    capabilities: List[str] = field(default_factory=list)
    status: str = "ACTIVE"
