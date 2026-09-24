"""
Scientific Regression Intelligence (Phase 89C)
==============================================
Synthesizes holistic regression reports across all evaluated pipelines,
correlating degradation with root causes and emitting structured alerts.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from research_validation.regression.drift_detector import (
    DriftDimension, DriftSeverity, DimensionDriftResult, MultiDimensionalDriftDetector
)
from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class ScientificRegressionReport:
    """Consolidated regression report across all evaluated metrics and dimensions."""
    report_id: str
    experiment_id: str
    baseline_run_id: str
    evaluated_run_id: str
    total_regressions_detected: int
    has_critical_regression: bool
    dimension_results: List[DimensionDriftResult]
    recommended_action: str
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    report_digest_sha256: str = field(default="")


class ScientificRegressionDetector:
    """
    Automated regression intelligence engine.
    """

    def __init__(self):
        self.detector = MultiDimensionalDriftDetector()

    def evaluate_experiment_regression(
        self,
        experiment_id: str,
        baseline_run_id: str,
        evaluated_run_id: str,
        baseline_metrics: Dict[str, float],
        evaluated_metrics: Dict[str, float],
    ) -> ScientificRegressionReport:
        dim_results: List[DimensionDriftResult] = []
        crit_count = 0
        reg_count = 0
        higher_better: bool = True

        for m_name, base_val in baseline_metrics.items():
            eval_val = evaluated_metrics.get(m_name, base_val)
            higher_better = not ("latency" in m_name or "error" in m_name or m_name.endswith("_ms"))
            
            res = self.detector.evaluate_metric_drift(
                metric_name=m_name,
                baseline=base_val,
                current=eval_val,
                higher_is_better=higher_better,
            )
            dim_results.append(res)
            if res.is_regression:
                reg_count += 1
            if res.severity == DriftSeverity.CRITICAL:
                crit_count += 1

        rep_id = f"reg_rep_{experiment_id}_{len(dim_results)}"
        has_critical = (crit_count > 0)
        
        if has_critical:
            rec = "BLOCK_RELEASE: Critical performance/accuracy regression detected. Trigger bisect."
        elif reg_count > 0:
            rec = "FLAG_REVIEW: Moderate regression detected. Requires reviewer verification."
        else:
            rec = "PASS: No statistical or performance regressions detected."

        payload = {
            "report_id": rep_id,
            "experiment_id": experiment_id,
            "reg_count": reg_count,
            "has_critical": has_critical,
        }
        digest = hash_canonical_json(payload)

        return ScientificRegressionReport(
            report_id=rep_id,
            experiment_id=experiment_id,
            baseline_run_id=baseline_run_id,
            evaluated_run_id=evaluated_run_id,
            total_regressions_detected=reg_count,
            has_critical_regression=has_critical,
            dimension_results=dim_results,
            recommended_action=rec,
            report_digest_sha256=digest,
        )
