"""World Model & Forward System Simulator for DocuTask ADIP.

Simulates forward system states across 5 min, 10 min, and 30 min prediction horizons, forecasting
GPU utilization, queue depths, token consumption velocity, budget burn, memory pressure, and API quota degradation.
"""

from __future__ import annotations

import math
from typing import List
from pydantic import BaseModel, Field


class WorldStateForecast(BaseModel):
    """Predictive snapshot of cluster and execution state at a future time horizon."""
    horizon_minutes: int
    predicted_gpu_load_pct: float
    predicted_token_burn_velocity: float = Field(description="Tokens consumed per second")
    predicted_budget_burn_usd: float
    predicted_queue_depth: int
    predicted_memory_pressure_mb: float
    predicted_cloud_quota_available_pct: float
    expected_retries: float
    risk_alert_threshold: bool
    summary: str = ""


class WorldModel:
    """Simulates dynamic cluster physics and future resource trajectories."""

    def __init__(
        self,
        base_gpu_load_pct: float = 28.0,
        base_queue_depth: int = 2,
        base_token_rate: float = 450.0,
        active_workers: int = 8,
    ) -> None:
        self.base_gpu_load_pct = base_gpu_load_pct
        self.base_queue_depth = base_queue_depth
        self.base_token_rate = base_token_rate
        self.active_workers = active_workers

    def forecast_trajectory(
        self,
        current_mission_load_factor: float = 1.0,
        cluster_concurrency: int = 4,
    ) -> List[WorldStateForecast]:
        """Generates predictions across 5m, 10m, and 30m horizons."""
        horizons = [5, 10, 30]
        forecasts: List[WorldStateForecast] = []

        for h in horizons:
            # Non-linear growth and decay models
            time_decay = math.exp(-0.02 * h)
            load_factor = current_mission_load_factor * (1.0 + 0.05 * (cluster_concurrency / max(1, self.active_workers)))

            # GPU load: dampens toward baseline
            gpu_load = min(98.0, max(5.0, (self.base_gpu_load_pct * load_factor) + (10.0 * (1.0 - time_decay))))

            # Queue depth: queuing theory M/M/c approximation
            arrival_rate = 1.2 * load_factor
            service_rate = 1.5
            utilization = min(0.95, arrival_rate / service_rate)
            queue_est = int(max(0, math.ceil((utilization ** 2) / (1.0 - utilization))))

            # Token burn & cost
            token_velocity = self.base_token_rate * load_factor
            total_tokens_horizon = token_velocity * (h * 60)
            budget_burn = round((total_tokens_horizon / 1000.0) * 0.00075, 4)

            # Memory pressure (MB)
            mem_pressure = min(32768.0, 4096.0 + (queue_est * 512.0) + (cluster_concurrency * 1024.0))

            # Cloud quota degradation
            quota_pct = max(10.0, 100.0 - (0.5 * h * load_factor))

            # Expected retries
            retries = round(0.02 * queue_est * h, 2)

            is_alert = (gpu_load > 85.0) or (quota_pct < 25.0) or (queue_est > 12)

            summary = (
                f"T+{h}m Forecast: GPU Load ~{gpu_load:.1f}%, Queue ~{queue_est} items, "
                f"Token Burn ~${budget_burn:.4f}. {'[CAPACITY WARNING]' if is_alert else '[NOMINAL]'}"
            )

            forecasts.append(
                WorldStateForecast(
                    horizon_minutes=h,
                    predicted_gpu_load_pct=round(gpu_load, 1),
                    predicted_token_burn_velocity=round(token_velocity, 1),
                    predicted_budget_burn_usd=budget_burn,
                    predicted_queue_depth=queue_est,
                    predicted_memory_pressure_mb=round(mem_pressure, 1),
                    predicted_cloud_quota_available_pct=round(quota_pct, 1),
                    expected_retries=retries,
                    risk_alert_threshold=is_alert,
                    summary=summary,
                )
            )

        return forecasts
