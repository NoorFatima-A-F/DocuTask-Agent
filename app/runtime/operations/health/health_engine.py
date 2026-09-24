"""
AOIS-HROP Phase 13.7 - Health Engine
Master health coordinator integrating evaluator, calculator, dependency graph, trend analyzer, and forecast engine.
"""

from typing import Any, Dict, Optional
from app.runtime.operations.health.subsystem_health import SubsystemHealthEvaluator, SubsystemHealthReport
from app.runtime.operations.health.health_calculator import HealthScoreCalculator
from app.runtime.operations.health.dependency_health import DependencyHealthGraph
from app.runtime.operations.health.health_trend import HealthTrendAnalyzer
from app.runtime.operations.health.health_forecast import HealthForecastEngine
from app.runtime.operations.events.operation_events import SubsystemType


class HealthEngine:
    """
    Master coordinator for platform-wide health monitoring, trend forecasting, and dependency cascade evaluation.
    """

    def __init__(self):
        self.evaluator = SubsystemHealthEvaluator()
        self.calculator = HealthScoreCalculator()
        self.dependency_graph = DependencyHealthGraph()
        self.trend_analyzer = HealthTrendAnalyzer()
        self.forecast_engine = HealthForecastEngine(self.trend_analyzer)

    def evaluate_platform_health(
        self,
        subsystem_metrics: Optional[Dict[str, Dict[str, float]]] = None,
    ) -> Dict[str, Any]:
        reports: Dict[str, SubsystemHealthReport] = {}

        for st in SubsystemType:
            metrics = (subsystem_metrics or {}).get(st.value, {})
            report = self.evaluator.evaluate_subsystem(
                subsystem=st,
                error_rate=metrics.get("error_rate", 0.0),
                latency_p95_ms=metrics.get("latency_p95_ms", 220.0),
                saturation_pct=metrics.get("saturation_pct", 25.0),
                unresponsive_tasks=int(metrics.get("unresponsive_tasks", 0)),
            )
            reports[st.value] = report

        composite = self.calculator.compute_composite_health(reports)
        status = self.calculator.determine_system_status(composite)
        self.trend_analyzer.record_health(composite)
        forecast = self.forecast_engine.generate_forecast(composite)

        return {
            "composite_score": composite,
            "status": status,
            "ema_score": self.trend_analyzer.calculate_ema(),
            "trend_slope": self.trend_analyzer.calculate_trend_slope(),
            "drift_detected": self.trend_analyzer.detect_drift(),
            "subsystems": {
                name: {
                    "score": r.score,
                    "status": r.status,
                    "issues": r.active_issues,
                    "metrics": r.metrics,
                }
                for name, r in reports.items()
            },
            "forecast": {
                "in_1h": forecast.predicted_score_in_1h,
                "in_24h": forecast.predicted_score_in_24h,
                "sla_breach_risk_pct": forecast.risk_of_sla_breach_pct,
                "time_to_degradation_sec": forecast.time_to_degradation_sec,
                "proactive_action": forecast.recommended_proactive_action,
            },
        }


_GLOBAL_HEALTH_ENGINE: Optional[HealthEngine] = None


def get_health_engine() -> HealthEngine:
    global _GLOBAL_HEALTH_ENGINE
    if _GLOBAL_HEALTH_ENGINE is None:
        _GLOBAL_HEALTH_ENGINE = HealthEngine()
    return _GLOBAL_HEALTH_ENGINE
