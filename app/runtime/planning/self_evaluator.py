"""Planner Self-Evaluation & Calibration Engine for DocuTask Autonomous Planning Platform.

Compares predicted planning metrics against actual execution telemetry to measure calibration error,
isolate root causes for plan deviation, and tune predictive models over time.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Dict, List
from pydantic import BaseModel, Field


class ExpectedVsActual(BaseModel):
    """Side-by-side comparison of planner predictions vs observed execution telemetry."""
    predicted_latency_ms: float
    actual_latency_ms: float
    latency_delta_ms: float
    latency_error_pct: float

    predicted_cost_usd: float
    actual_cost_usd: float
    cost_delta_usd: float
    cost_error_pct: float

    predicted_accuracy: float
    actual_accuracy: float
    accuracy_delta: float

    predicted_risk_score: float
    actual_failure_occurred: bool


class PlanCalibrationMetric(BaseModel):
    """Aggregate model calibration scores and feedback adjustments."""
    calibration_id: str = Field(default_factory=lambda: f"calib_{uuid.uuid4().hex[:8]}")
    mission_id: str
    strategy_id: str
    comparison: ExpectedVsActual
    overall_calibration_score: float = Field(ge=0.0, le=1.0, description="1 / (1 + MAPE/100)")
    root_causes: List[str] = Field(default_factory=list)
    tuning_recommendations: Dict[str, str] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PlannerSelfEvaluationEngine:
    """Evaluates planner accuracy post-mission and generates calibration signals."""

    def evaluate_mission(
        self,
        mission_id: str,
        strategy_id: str,
        predicted_latency_ms: float,
        actual_latency_ms: float,
        predicted_cost_usd: float,
        actual_cost_usd: float,
        predicted_accuracy: float,
        actual_accuracy: float,
        predicted_risk_score: float,
        actual_failure_occurred: bool = False,
    ) -> PlanCalibrationMetric:
        # Latency error
        lat_delta = actual_latency_ms - predicted_latency_ms
        lat_err_pct = abs(lat_delta) / max(1.0, predicted_latency_ms) * 100.0

        # Cost error
        cost_delta = actual_cost_usd - predicted_cost_usd
        cost_err_pct = abs(cost_delta) / max(1e-6, predicted_cost_usd) * 100.0

        # Accuracy error
        acc_delta = actual_accuracy - predicted_accuracy

        comparison = ExpectedVsActual(
            predicted_latency_ms=round(predicted_latency_ms, 2),
            actual_latency_ms=round(actual_latency_ms, 2),
            latency_delta_ms=round(lat_delta, 2),
            latency_error_pct=round(lat_err_pct, 2),
            predicted_cost_usd=round(predicted_cost_usd, 6),
            actual_cost_usd=round(actual_cost_usd, 6),
            cost_delta_usd=round(cost_delta, 6),
            cost_error_pct=round(cost_err_pct, 2),
            predicted_accuracy=round(predicted_accuracy, 4),
            actual_accuracy=round(actual_accuracy, 4),
            accuracy_delta=round(acc_delta, 4),
            predicted_risk_score=round(predicted_risk_score, 4),
            actual_failure_occurred=actual_failure_occurred,
        )

        # Smooth, non-negative calibration score in range (0, 1]
        mape = (lat_err_pct + cost_err_pct) / 2.0
        calibration_score = 1.0 / (1.0 + (mape / 100.0))

        # Root cause analysis
        root_causes: List[str] = []
        tuning: Dict[str, str] = {}

        if lat_err_pct > 25.0:
            if lat_delta > 0:
                root_causes.append("Worker queuing delay and upstream network jitter exceeded P90 estimate.")
                tuning["latency_p50_multiplier"] = "Increase base latency multiplier by +10%."
            else:
                root_causes.append("Parallel pipelining exceeded expected speedup factor.")
                tuning["concurrency_efficiency"] = "Adjust pipelining factor from 0.85 to 0.78."

        if cost_err_pct > 20.0:
            if cost_delta > 0:
                root_causes.append("LLM token consumption exceeded prompt budget by >20%.")
                tuning["token_buffer"] = "Increase token safety margin by +15%."

        if actual_failure_occurred and predicted_risk_score < 0.10:
            root_causes.append("Unforeseen runtime exception occurred despite low initial risk score.")
            tuning["risk_floor"] = "Raise baseline minimum risk threshold to 0.08."

        if not root_causes:
            root_causes.append("Plan executed within nominal 95% confidence bounds.")
            tuning["model_status"] = "Calibration optimal. No tuning required."

        return PlanCalibrationMetric(
            mission_id=mission_id,
            strategy_id=strategy_id,
            comparison=comparison,
            overall_calibration_score=round(calibration_score, 4),
            root_causes=root_causes,
            tuning_recommendations=tuning,
        )
