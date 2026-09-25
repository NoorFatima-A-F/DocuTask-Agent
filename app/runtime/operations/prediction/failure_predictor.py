"""
AOIS-HROP Phase 13.7 - Predictive Risk & Failure Engine
Forecasts capacity exhaustion, budget overruns, retry storms, confidence collapse, and queue explosions prior to manifestation.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List
import uuid


@dataclass
class FailureForecast:
    prediction_id: str
    failure_type: str  # CAPACITY_EXHAUSTION, BUDGET_EXHAUSTION, RETRY_STORM, CONFIDENCE_COLLAPSE, QUEUE_EXPLOSION
    probability: float  # 0.0 - 1.0
    estimated_time_to_failure_sec: float
    affected_subsystem: str
    impact_severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    preventative_recommendation: str
    predicted_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class OperationalRiskForecast:
    forecast_id: str
    composite_risk_index: float  # 0.0 (low) - 1.0 (extreme)
    sla_breach_probability: float
    financial_exposure_usd: float
    active_threats_count: int
    top_threat_subsystem: str
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class FailurePredictor:
    """
    Predictive intelligence forecasting impending subsystem failures from telemetry rate-of-change.
    """

    def predict_capacity_exhaustion(self, current_concurrency: int, max_concurrency: int, growth_rate: float) -> FailureForecast:
        headroom = max_concurrency - current_concurrency
        time_to_exhaust = round(headroom / (growth_rate if growth_rate > 0 else 0.1), 1)
        prob = round(min(1.0, current_concurrency / max_concurrency), 2)

        return FailureForecast(
            prediction_id=f"pred-cap-{uuid.uuid4().hex[:8]}",
            failure_type="CAPACITY_EXHAUSTION",
            probability=prob,
            estimated_time_to_failure_sec=max(10.0, time_to_exhaust),
            affected_subsystem="WORKERS",
            impact_severity="HIGH" if prob > 0.8 else "MEDIUM",
            preventative_recommendation="AUTO_SCALE_WORKER_POOL_OR_BURST_LOCAL_OCR",
        )

    def predict_budget_exhaustion(self, current_spend: float, budget_cap: float, burn_rate_usd_per_min: float) -> FailureForecast:
        remaining = max(0.0, budget_cap - current_spend)
        burn = burn_rate_usd_per_min if burn_rate_usd_per_min > 0 else 0.01
        time_to_exhaust = round((remaining / burn) * 60.0, 1)
        prob = round(min(1.0, current_spend / (budget_cap if budget_cap > 0 else 1.0)), 2)

        return FailureForecast(
            prediction_id=f"pred-bdg-{uuid.uuid4().hex[:8]}",
            failure_type="BUDGET_EXHAUSTION",
            probability=prob,
            estimated_time_to_failure_sec=max(15.0, time_to_exhaust),
            affected_subsystem="OPTIMIZATION",
            impact_severity="CRITICAL" if prob > 0.9 else "HIGH",
            preventative_recommendation="SWITCH_TO_QUANTIZED_LOCAL_MODEL_TO_HALT_SPEND",
        )

    def predict_retry_storm(self, recent_error_count: int, retry_rate: float) -> FailureForecast:
        prob = round(min(1.0, (recent_error_count / 10.0) * (retry_rate * 5.0)), 2)
        return FailureForecast(
            prediction_id=f"pred-ret-{uuid.uuid4().hex[:8]}",
            failure_type="RETRY_STORM",
            probability=prob,
            estimated_time_to_failure_sec=30.0 if prob > 0.5 else 180.0,
            affected_subsystem="API",
            impact_severity="HIGH" if prob > 0.7 else "LOW",
            preventative_recommendation="ENGAGE_ADAPTIVE_EXPONENTIAL_BACKOFF_AND_CIRCUIT_BREAKER",
        )

    def predict_confidence_collapse(self, current_confidence: float, variance: float) -> FailureForecast:
        prob = round(min(1.0, max(0.0, (0.95 - current_confidence) * 5.0) + variance), 2)
        return FailureForecast(
            prediction_id=f"pred-cnf-{uuid.uuid4().hex[:8]}",
            failure_type="CONFIDENCE_COLLAPSE",
            probability=prob,
            estimated_time_to_failure_sec=60.0,
            affected_subsystem="PLANNER",
            impact_severity="CRITICAL" if prob > 0.6 else "MEDIUM",
            preventative_recommendation="ESCALATE_TO_MULTI_AGENT_CONSENSUS_AND_SMT_SYMBOLIC_VERIFIER",
        )

    def generate_all_predictions(
        self,
        concurrency: int = 24,
        max_concurrency: int = 32,
        current_spend: float = 0.045,
        budget_cap: float = 0.150,
        recent_errors: int = 1,
        confidence: float = 0.965,
    ) -> List[FailureForecast]:
        return [
            self.predict_capacity_exhaustion(concurrency, max_concurrency, growth_rate=1.2),
            self.predict_budget_exhaustion(current_spend, budget_cap, burn_rate_usd_per_min=0.015),
            self.predict_retry_storm(recent_errors, retry_rate=0.02),
            self.predict_confidence_collapse(confidence, variance=0.03),
        ]


class RiskForecastEngine:
    """
    Synthesizes discrete failure predictions into aggregate enterprise risk exposure ratings.
    """

    def __init__(self, failure_predictor: FailurePredictor):
        self.predictor = failure_predictor

    def compute_risk_forecast(self, predictions: List[FailureForecast]) -> OperationalRiskForecast:
        if not predictions:
            predictions = self.predictor.generate_all_predictions()

        avg_prob = sum(p.probability for p in predictions) / len(predictions)
        sla_prob = round(min(1.0, avg_prob * 1.25), 3)
        risk_index = round(min(1.0, avg_prob * 0.85 + (0.15 if any(p.impact_severity == "CRITICAL" for p in predictions) else 0.0)), 3)

        top_threat = max(predictions, key=lambda p: p.probability)

        return OperationalRiskForecast(
            forecast_id=f"risk-{uuid.uuid4().hex[:8]}",
            composite_risk_index=risk_index,
            sla_breach_probability=sla_prob,
            financial_exposure_usd=round(risk_index * 12.50, 2),
            active_threats_count=len([p for p in predictions if p.probability > 0.4]),
            top_threat_subsystem=top_threat.affected_subsystem,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )
