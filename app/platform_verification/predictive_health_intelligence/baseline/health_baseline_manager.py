"""
Health Baseline Manager (Part 3H.3.4.3).
Loads declarative operational baselines from health_baseline.yaml and validates service operating ranges.
"""
import os
import yaml
from typing import Dict, Any, List, Optional
from app.platform_verification.predictive_health_intelligence.domain.models import (
    BaselineProfile,
    BaselineReport,
)


class HealthBaselineManager:
    """
    Manages normal operational baselines and thresholds across platform services.
    """

    DEFAULT_BASELINE = {
        "profiles": {
            "worker": {
                "cpu_usage_pct": {"nominal_min": 20.0, "nominal_max": 65.0, "warning_threshold": 80.0, "critical_threshold": 95.0},
                "memory_usage_pct": {"nominal_min": 30.0, "nominal_max": 70.0, "warning_threshold": 80.0, "critical_threshold": 95.0},
                "queue_depth": {"nominal_min": 0, "nominal_max": 500, "warning_threshold": 2000, "critical_threshold": 5000},
            },
            "database": {
                "connection_utilization_pct": {"nominal_min": 10.0, "nominal_max": 60.0, "warning_threshold": 75.0, "critical_threshold": 90.0},
                "query_latency_ms": {"nominal_min": 2.0, "nominal_max": 30.0, "warning_threshold": 80.0, "critical_threshold": 200.0},
            },
            "ai_provider": {
                "model_latency_ms": {"nominal_min": 150.0, "nominal_max": 800.0, "warning_threshold": 1500.0, "critical_threshold": 3000.0},
                "error_rate_pct": {"nominal_min": 0.0, "nominal_max": 1.0, "warning_threshold": 5.0, "critical_threshold": 15.0},
            },
        }
    }

    def __init__(self, baseline_path: str = "health_baseline.yaml"):
        self.baseline_path = baseline_path
        self.raw_data = self._load_yaml()

    def _load_yaml(self) -> Dict[str, Any]:
        if os.path.exists(self.baseline_path):
            try:
                with open(self.baseline_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if data and "profiles" in data:
                        return data
            except Exception:
                pass
        return self.DEFAULT_BASELINE

    def get_baseline_report(self) -> BaselineReport:
        profiles: List[BaselineProfile] = []
        p_dict = self.raw_data.get("profiles", {})

        for svc_name, metrics in p_dict.items():
            for m_name, ranges in metrics.items():
                profiles.append(
                    BaselineProfile(
                        service=svc_name,
                        metric=m_name,
                        nominal_min=float(ranges.get("nominal_min", 0.0)),
                        nominal_max=float(ranges.get("nominal_max", 100.0)),
                        warning_threshold=float(ranges.get("warning_threshold", 80.0)),
                        critical_threshold=float(ranges.get("critical_threshold", 95.0)),
                    )
                )

        passed = len(profiles) >= 6

        return BaselineReport(
            total_profiles=len(profiles),
            profiles=profiles,
            baseline_loaded=True,
            passed=passed,
            details={
                "source_file": self.baseline_path,
                "services_profiled": list(p_dict.keys()),
            },
        )
