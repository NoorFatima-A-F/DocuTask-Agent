"""
Online Drift Detection - Drift Alerting & Mitigation Advisor
Classifies drift severity and prescribes automated mitigation actions.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class DriftAlert:
    metric_name: str
    psi_score: float
    kl_divergence: float
    wasserstein_dist: float
    sequential_alarm: bool
    severity: str  # NEGLIGIBLE | WARNING | CRITICAL_DRIFT
    recommended_mitigation: str
    auto_trigger_recalibration: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DriftAlertAdvisor:
    """Evaluates drift metrics and recommends actionable policy or recalibration interventions."""

    @staticmethod
    def evaluate_metric_drift(
        metric_name: str,
        psi: float,
        kl: float,
        wasserstein: float,
        sequential_alarm: bool = False,
    ) -> DriftAlert:
        # Standard Industry PSI thresholds:
        # PSI < 0.1: No significant change
        # 0.1 <= PSI < 0.25: Moderate shift / Warning
        # PSI >= 0.25: Significant shift / Critical Action Needed

        if psi >= 0.25 or sequential_alarm or kl > 0.40:
            severity = "CRITICAL_DRIFT"
            mitigation = "Trigger automated model recalibration, re-estimate surrogate surrogate weights, and alert on-call ML engineer."
            auto_trigger = True
        elif psi >= 0.10 or kl > 0.15:
            severity = "WARNING"
            mitigation = "Increase shadow evaluation sampling frequency and monitor residual error autocorrelation."
            auto_trigger = False
        else:
            severity = "NEGLIGIBLE"
            mitigation = "Baseline distribution stable. No operational intervention required."
            auto_trigger = False

        return DriftAlert(
            metric_name=metric_name,
            psi_score=round(psi, 4),
            kl_divergence=round(kl, 4),
            wasserstein_dist=round(wasserstein, 4),
            sequential_alarm=sequential_alarm,
            severity=severity,
            recommended_mitigation=mitigation,
            auto_trigger_recalibration=auto_trigger,
        )
