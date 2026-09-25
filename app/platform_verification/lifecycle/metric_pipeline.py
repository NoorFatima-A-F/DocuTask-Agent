from dataclasses import dataclass
from typing import Dict, List
import math

@dataclass(frozen=True)
class ComputedMetric:
    metric_name: str
    value: float
    unit: str
    sample_size: int
    confidence_interval_95: tuple[float, float]
    dimension: str

class MetricProcessingPipeline:
    @staticmethod
    def process_metrics(raw_samples: Dict[str, List[float]]) -> Dict[str, ComputedMetric]:
        results = {}
        for name, values in raw_samples.items():
            if not values:
                continue
            n = len(values)
            mean = sum(values) / n
            variance = sum((x - mean) ** 2 for x in values) / max(1, n - 1)
            std_dev = math.sqrt(variance)
            margin = 1.96 * (std_dev / math.sqrt(n)) if n > 1 else 0.0

            dim = "PERFORMANCE" if "latency" in name or "time" in name else "CORRECTNESS"
            unit = "ms" if "latency" in name else "score"

            results[name] = ComputedMetric(
                metric_name=name,
                value=mean,
                unit=unit,
                sample_size=n,
                confidence_interval_95=(max(0.0, mean - margin), mean + margin),
                dimension=dim
            )
        return results
