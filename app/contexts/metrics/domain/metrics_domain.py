from dataclasses import dataclass
from app.shared_kernel import BaseEntity, DomainEvent

@dataclass
class MetricComputed(DomainEvent):
    metric_id: str = ""
    run_id: str = ""
    name: str = ""
    value: float = 0.0

@dataclass
class MetricAggregate(BaseEntity):
    run_id: str = ""
    name: str = ""
    value: float = 0.0
    category: str = "AI_QUALITY"
