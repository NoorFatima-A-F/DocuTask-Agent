"""
AOIS-HROP Phase 13.7 - Operational Analytics Engine
Master enterprise SRE analytics consolidating health KPIs, recovery analytics, capacity trends, availability metrics, and cost impacts.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from app.runtime.operations.health.health_engine import get_health_engine
from app.runtime.operations.incidents.incident_engine import get_incident_engine
from app.runtime.operations.healing.healing_engine import get_healing_engine
from app.runtime.operations.recovery.recovery_engine import get_recovery_engine
from app.runtime.operations.resilience.resilience_engine import get_resilience_engine
from app.runtime.operations.prediction.failure_predictor import FailurePredictor, RiskForecastEngine


class OperationalAnalytics:
    """
    Consolidates real-time telemetry into high-level operational intelligence for SREs and executives.
    """

    def __init__(self):
        self.health_engine = get_health_engine()
        self.incident_engine = get_incident_engine()
        self.healing_engine = get_healing_engine()
        self.recovery_engine = get_recovery_engine()
        self.resilience_engine = get_resilience_engine()
        self.predictor = FailurePredictor()
        self.risk_engine = RiskForecastEngine(self.predictor)

    def get_full_analytics(self) -> Dict[str, Any]:
        health = self.health_engine.evaluate_platform_health()
        resilience = self.resilience_engine.generate_resilience_profile()
        predictions = self.predictor.generate_all_predictions()
        risk = self.risk_engine.compute_risk_forecast(predictions)
        incidents = self.incident_engine.get_all_incidents_summary()
        healing_history = self.healing_engine.get_healing_history()

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "executive_summary": {
                "health_score": health["composite_score"],
                "health_status": health["status"],
                "resilience_score": resilience.resilience_score,
                "availability_pct": resilience.availability_percentage,
                "active_incidents": len([i for i in incidents if not i.get("resolved", False)]),
                "total_healed_operations": len(healing_history),
                "composite_risk_index": risk.composite_risk_index,
                "financial_exposure_usd": risk.financial_exposure_usd,
            },
            "sre_metrics": {
                "mttr_seconds": resilience.mttr_seconds,
                "mttd_seconds": resilience.mttd_seconds,
                "mtbf_hours": resilience.mtbf_hours,
                "healing_success_rate_pct": resilience.healing_success_rate_pct,
                "recovery_success_rate_pct": resilience.recovery_success_rate_pct,
                "sla_compliance_pct": resilience.sla_compliance_pct,
            },
            "health_breakdown": health["subsystems"],
            "predictions": [
                {
                    "type": p.failure_type,
                    "probability": p.probability,
                    "time_to_failure_sec": p.estimated_time_to_failure_sec,
                    "subsystem": p.affected_subsystem,
                    "severity": p.impact_severity,
                    "recommendation": p.preventative_recommendation,
                }
                for p in predictions
            ],
            "risk_profile": {
                "risk_index": risk.composite_risk_index,
                "sla_breach_prob": risk.sla_breach_probability,
                "top_threat": risk.top_threat_subsystem,
            },
        }


_GLOBAL_ANALYTICS: Optional[OperationalAnalytics] = None


def get_operational_analytics() -> OperationalAnalytics:
    global _GLOBAL_ANALYTICS
    if _GLOBAL_ANALYTICS is None:
        _GLOBAL_ANALYTICS = OperationalAnalytics()
    return _GLOBAL_ANALYTICS
