"""
Experiment Replay Engine (Phase 82B.3)
======================================
Provides independent, deterministic re-execution of scientific experiments
from saved manifests and compares replayed metrics against original records.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from research_validation.scientific_execution.experiment_manifest import ExperimentManifest
from research_validation.scientific_execution.experiment_runner import (
    ScientificExperimentRunner, ExperimentRunResult
)


@dataclass(frozen=True)
class MetricReplayComparison:
    metric_name: str
    original_value: float
    replayed_value: float
    absolute_delta: float
    relative_delta: float
    is_exact_match: bool
    within_tolerance: bool


@dataclass(frozen=True)
class ExperimentReplayReport:
    experiment_id: str
    original_run_id: str
    replayed_run_id: str
    is_reproduced: bool
    hash_match: bool
    metric_comparisons: Dict[str, MetricReplayComparison]
    execution_duration_ratio: float
    timestamp_utc: str
    diagnostic: str


class ExperimentReplayEngine:
    """
    Replays an experiment and conducts precision tolerance comparisons.
    """

    def __init__(self, tolerance: float = 1e-5, latency_tolerance_ms: float = 100.0):
        self.tolerance = tolerance
        self.latency_tolerance_ms = latency_tolerance_ms
        self.runner = ScientificExperimentRunner()

    def replay_and_compare(
        self,
        manifest: ExperimentManifest,
        original_result: ExperimentRunResult,
        mock_samples: Optional[List[Dict[str, Any]]] = None,
    ) -> ExperimentReplayReport:
        """Re-execute experiment and evaluate metric parity."""
        replayed_res = self.runner.execute(manifest, mock_dataset_samples=mock_samples)
        now_str = datetime.now(timezone.utc).isoformat()

        comparisons: Dict[str, MetricReplayComparison] = {}
        all_within_tol = True

        for m_name, orig_val in original_result.metrics.items():
            rep_val = replayed_res.metrics.get(m_name, 0.0)
            abs_diff = abs(orig_val - rep_val)
            rel_diff = abs_diff / abs(orig_val) if abs(orig_val) > 0 else 0.0
            
            # Latency and duration measurements undergo non-deterministic wall-clock jitter
            if "latency" in m_name or m_name.endswith("_ms") or "duration" in m_name:
                within_tol = abs_diff <= self.latency_tolerance_ms or rel_diff <= 10.0
            else:
                within_tol = abs_diff <= self.tolerance or rel_diff <= self.tolerance

            if not within_tol:
                all_within_tol = False

            comparisons[m_name] = MetricReplayComparison(
                metric_name=m_name,
                original_value=orig_val,
                replayed_value=rep_val,
                absolute_delta=abs_diff,
                relative_delta=rel_diff,
                is_exact_match=(abs_diff == 0.0),
                within_tolerance=within_tol,
            )

        hash_match = (original_result.final_output_digest == replayed_res.final_output_digest)
        is_reproduced = all_within_tol and (original_result.status == replayed_res.status)
        dur_ratio = (
            replayed_res.duration_ms / original_result.duration_ms
            if original_result.duration_ms > 0 else 1.0
        )

        return ExperimentReplayReport(
            experiment_id=manifest.experiment_id,
            original_run_id=original_result.run_id,
            replayed_run_id=replayed_res.run_id,
            is_reproduced=is_reproduced,
            hash_match=hash_match,
            metric_comparisons=comparisons,
            execution_duration_ratio=dur_ratio,
            timestamp_utc=now_str,
            diagnostic="Experiment reproduced within tolerance." if is_reproduced else "Metric divergence detected.",
        )
