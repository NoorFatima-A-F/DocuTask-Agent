from typing import List
from ..domain.metrics_domain import MetricAggregate, MetricComputed
from app.shared_kernel import Result, Ok, get_event_bus

class MetricsService:
    def __init__(self, repo):
        self.repo = repo

    async def record_metric(self, metric_id: str, run_id: str, name: str, value: float, category: str = "AI_QUALITY") -> Result[MetricAggregate, str]:
        agg = MetricAggregate(id=metric_id, run_id=run_id, name=name, value=value, category=category)
        self.repo.save(agg)
        await get_event_bus().publish(MetricComputed(metric_id=metric_id, run_id=run_id, name=name, value=value))
        return Ok(agg)
