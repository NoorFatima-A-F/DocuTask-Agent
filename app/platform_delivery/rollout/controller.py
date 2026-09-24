"""Progressive Delivery Controller."""
from typing import Optional
from ..control_plane.controller import DeploymentRecord
from ..strategies.canary import CanaryStrategy
from .analysis import CanaryAnalysisEngine, RolloutDecision


class ProgressiveDeliveryController:
    """Executes progressive rollout steps and handles automated abort upon telemetry degradation."""

    def __init__(
        self,
        canary_strategy: Optional[CanaryStrategy] = None,
        analysis_engine: Optional[CanaryAnalysisEngine] = None,
    ):
        self.canary_strategy = canary_strategy or CanaryStrategy()
        self.analysis_engine = analysis_engine or CanaryAnalysisEngine()

    def run_step_analysis(
        self,
        deployment: DeploymentRecord,
        step_index: int,
        traffic_pct: int,
        error_rate: float,
        p95_ms: float,
    ) -> RolloutDecision:
        decision, reasons = self.analysis_engine.evaluate_telemetry(
            error_rate=error_rate,
            p95_latency_ms=p95_ms,
        )
        self.canary_strategy.evaluate_step(
            step_index=step_index,
            traffic_pct=traffic_pct,
            observed_error_rate=error_rate,
            observed_p95_ms=p95_ms,
        )
        return decision
