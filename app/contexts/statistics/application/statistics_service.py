from typing import List
import statistics as stats
import math
from ..domain.statistics_domain import StatisticalAggregate, StatisticalAnalysisCompleted
from app.shared_kernel import Result, Ok, Err, get_event_bus

class StatisticsService:
    def __init__(self, repo):
        self.repo = repo

    async def analyze_samples(self, analysis_id: str, metric_name: str, samples: List[float]) -> Result[StatisticalAggregate, str]:
        n = len(samples)
        if n == 0:
            return Err("Cannot analyze empty sample set")
        mean_val = stats.mean(samples)
        std_val = stats.stdev(samples) if n > 1 else 0.0
        z = 1.96
        margin = z * (std_val / math.sqrt(n)) if n > 1 else 0.0
        ci_lower = max(0.0, mean_val - margin)
        ci_upper = min(1.0, mean_val + margin) if mean_val <= 1.0 else mean_val + margin

        agg = StatisticalAggregate(
            id=analysis_id,
            metric_name=metric_name,
            sample_size=n,
            mean=mean_val,
            std_dev=std_val,
            ci_lower_95=ci_lower,
            ci_upper_95=ci_upper
        )
        self.repo.save(agg)
        await get_event_bus().publish(StatisticalAnalysisCompleted(analysis_id=analysis_id, metric_name=metric_name, mean=mean_val))
        return Ok(agg)
