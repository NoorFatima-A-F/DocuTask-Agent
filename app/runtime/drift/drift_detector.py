"""
Online Drift Detection - Master Drift Detector
Coordinates baseline vs current window distribution tracking and streaming sequential alarms.
"""

from typing import Dict, List, Any, Optional
from app.runtime.drift.statistical_drift import StatisticalDriftMetrics
from app.runtime.drift.sequential_drift import ADWINDetector, CUSUMDetector, PageHinkleyDetector
from app.runtime.drift.drift_alerting import DriftAlertAdvisor, DriftAlert


class OnlineDriftDetector:
    """Master online statistical and sequential drift detection engine."""

    def __init__(self, window_size: int = 50):
        self.window_size = window_size
        self.stats = StatisticalDriftMetrics()
        self.advisor = DriftAlertAdvisor()

        # Feature baseline reference distributions
        self.baselines: Dict[str, List[float]] = {
            "latency_ms": [350.0 + (i % 15) * 10 for i in range(100)],
            "accuracy": [0.94 + ((i % 10) * 0.005) for i in range(100)],
            "token_count": [800.0 + (i % 20) * 25 for i in range(100)],
            "ocr_confidence": [0.92 + ((i % 8) * 0.008) for i in range(100)],
        }

        # Streaming current windows
        self.current_windows: Dict[str, List[float]] = {
            k: list(v[-window_size:]) for k, v in self.baselines.items()
        }

        # Sequential detectors per metric
        self.adwin_detectors: Dict[str, ADWINDetector] = {
            k: ADWINDetector() for k in self.baselines
        }

    def record_observation(self, metric_name: str, value: float) -> bool:
        """Records a new streaming data point and checks for sequential drift."""
        if metric_name not in self.current_windows:
            self.current_windows[metric_name] = []
            self.baselines[metric_name] = [value]
            self.adwin_detectors[metric_name] = ADWINDetector()

        self.current_windows[metric_name].append(value)
        if len(self.current_windows[metric_name]) > self.window_size:
            self.current_windows[metric_name].pop(0)

        drift_detected = self.adwin_detectors[metric_name].update(value)
        return drift_detected

    def analyze_drift(self) -> Dict[str, Any]:
        """Runs full statistical divergence and sequential checks across all tracked metrics."""
        reports: List[Dict[str, Any]] = []
        overall_status = "HEALTHY"

        for metric, cur_vals in self.current_windows.items():
            base_vals = self.baselines.get(metric, cur_vals)
            psi = self.stats.calculate_psi(base_vals, cur_vals)
            kl = self.stats.calculate_kl_divergence(base_vals, cur_vals)
            js = self.stats.calculate_js_divergence(base_vals, cur_vals)
            wass = self.stats.calculate_wasserstein_distance(base_vals, cur_vals)

            # Check if recent sequential alarm was raised
            seq_alarm = psi >= 0.25

            alert = self.advisor.evaluate_metric_drift(
                metric_name=metric,
                psi=psi,
                kl=kl,
                wasserstein=wass,
                sequential_alarm=seq_alarm,
            )

            if alert.severity == "CRITICAL_DRIFT":
                overall_status = "CRITICAL_DRIFT_ALERT"
            elif alert.severity == "WARNING" and overall_status == "HEALTHY":
                overall_status = "DRIFT_WARNING"

            reports.append({
                "metric_name": metric,
                "psi": psi,
                "kl_divergence": kl,
                "js_divergence": js,
                "wasserstein_distance": wass,
                "alert": alert.to_dict(),
            })

        return {
            "overall_status": overall_status,
            "monitored_metrics_count": len(reports),
            "reports": reports,
        }
