"""
Health Transition Rule Engine (Part 3H.3.3.3).
Evaluates metric signals against health_rules.yaml threshold definitions
to determine appropriate health state transitions.
"""
import os
import yaml
from typing import Dict, Any, Tuple
from app.platform_verification.health_transition_intelligence.domain.models import HealthState


class HealthRuleEngine:
    """
    Evaluates telemetry against operational rules to trigger state changes.
    """

    DEFAULT_RULES = {
        "rules": {
            "memory": {"warning_threshold_pct": 80.0, "critical_threshold_pct": 95.0, "action_on_critical": "DEGRADED"},
            "cpu": {"warning_threshold_pct": 85.0, "critical_threshold_pct": 98.0, "action_on_critical": "DEGRADED"},
            "latency": {"degraded_threshold_ms": 500.0, "critical_threshold_ms": 2000.0, "action_on_degraded": "DEGRADED", "action_on_critical": "NOT_READY"},
            "queue": {"warning_depth": 500, "critical_depth": 1000, "action_on_critical": "DEGRADED"},
            "database": {"unavailable_action": "NOT_READY"},
            "ai_provider": {"timeout_action": "DEGRADED"},
        }
    }

    def __init__(self, rules_path: str = "health_rules.yaml"):
        self.rules_path = rules_path
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict[str, Any]:
        if os.path.exists(self.rules_path):
            try:
                with open(self.rules_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if data and "rules" in data:
                        return data
            except Exception:
                pass
        return self.DEFAULT_RULES

    def evaluate_signals(self, snapshot: Dict[str, Any]) -> Tuple[HealthState, str]:
        r = self.rules.get("rules", {})

        # 1. Database check
        db_lat = snapshot.get("dependencies", {}).get("postgres_latency_ms", 10.0)
        if snapshot.get("dependencies", {}).get("postgres_available") is False or db_lat > 2000.0:
            return HealthState.NOT_READY, "PostgreSQL database unavailable or unacceptably slow"

        # 2. Redis check
        if snapshot.get("dependencies", {}).get("redis_available") is False:
            return HealthState.NOT_READY, "Redis queue broker unreachable"

        # 3. Memory check
        mem_pct = snapshot.get("service", {}).get("memory_usage_pct", 50.0)
        mem_crit = r.get("memory", {}).get("critical_threshold_pct", 95.0)
        if mem_pct >= mem_crit:
            return HealthState.DEGRADED, f"Host memory critical: {mem_pct}% >= {mem_crit}%"

        # 4. Latency / AI check
        ai_lat = snapshot.get("dependencies", {}).get("ai_latency_ms", 150.0)
        if ai_lat >= 2000.0:
            return HealthState.DEGRADED, f"Gemini AI provider latency elevated: {ai_lat}ms"

        # 5. Service Latency check
        svc_lat = snapshot.get("service", {}).get("event_loop_latency_ms", 5.0)
        lat_crit = r.get("latency", {}).get("critical_threshold_ms", 2000.0)
        lat_deg = r.get("latency", {}).get("degraded_threshold_ms", 500.0)
        if svc_lat >= lat_crit:
            return HealthState.NOT_READY, f"Event loop frozen: {svc_lat}ms >= {lat_crit}ms"
        elif svc_lat >= lat_deg:
            return HealthState.DEGRADED, f"Event loop elevated lag: {svc_lat}ms >= {lat_deg}ms"

        return HealthState.READY, "All operational telemetry within nominal thresholds"
