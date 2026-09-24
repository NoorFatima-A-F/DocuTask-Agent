from dataclasses import dataclass
from app.shared_kernel import BaseEntity, DomainEvent

@dataclass
class StatisticalAnalysisCompleted(DomainEvent):
    analysis_id: str = ""
    metric_name: str = ""
    mean: float = 0.0

@dataclass
class StatisticalAggregate(BaseEntity):
    metric_name: str = ""
    sample_size: int = 0
    mean: float = 0.0
    std_dev: float = 0.0
    ci_lower_95: float = 0.0
    ci_upper_95: float = 0.0
