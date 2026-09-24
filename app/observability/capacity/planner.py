"""Capacity Planning and Saturation Horizon Forecasting."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ResourceSaturationForecast:
    resource_name: str
    current_value: float
    saturation_threshold: float
    daily_growth_rate: float
    days_to_saturation: Optional[float]
    is_critical: bool


class CapacityPlanner:
    """Predicts infrastructure and runtime resource saturation timelines based on historical growth."""

    def __init__(self, critical_days_threshold: float = 7.0):
        self.critical_days_threshold = critical_days_threshold

    def calculate_saturation(
        self,
        resource_name: str,
        current_value: float,
        saturation_threshold: float,
        daily_growth_rate: float,
    ) -> ResourceSaturationForecast:
        """Forecast days until resource limit is reached."""
        if daily_growth_rate <= 0:
            days = None
            is_critical = False
        else:
            remaining = max(0.0, saturation_threshold - current_value)
            days = remaining / daily_growth_rate
            is_critical = days <= self.critical_days_threshold

        return ResourceSaturationForecast(
            resource_name=resource_name,
            current_value=current_value,
            saturation_threshold=saturation_threshold,
            daily_growth_rate=daily_growth_rate,
            days_to_saturation=round(days, 1) if days is not None else None,
            is_critical=is_critical,
        )

    def evaluate_fleet_capacity(
        self,
        metrics_growth_map: Dict[str, Dict[str, float]],
    ) -> List[ResourceSaturationForecast]:
        """Evaluate multiple resources (e.g. CPU, Storage, Worker Queues, AI Tokens)."""
        forecasts: List[ResourceSaturationForecast] = []
        for name, params in metrics_growth_map.items():
            f = self.calculate_saturation(
                resource_name=name,
                current_value=params.get("current", 0.0),
                saturation_threshold=params.get("threshold", 100.0),
                daily_growth_rate=params.get("growth_rate", 0.0),
            )
            forecasts.append(f)
        return forecasts
