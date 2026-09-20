"""
Research Validation & Independent Scientific Verification Framework (RVISF)
Phase 37: Independent Replication Framework

Enables independent third-party researchers and automated test runners to verify reproducibility
across different compute environments, platforms (Windows, Linux, macOS, Cloud Run), and evaluators.
Compliant with ACM Artifact Review Badging (Artifacts Evaluated - Reusable, Results Replicated).
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ReplicationRun:
    """A single execution run by an evaluator."""
    run_id: str
    evaluator_name: str
    environment_info: Dict[str, Any]
    metric_values: Dict[str, float]
    execution_duration_ms: float
    timestamp_ns: int


@dataclass
class MetricReplicationComparison:
    """Statistical comparison of a metric across replication runs."""
    metric_name: str
    baseline_value: float
    replicated_mean: float
    replicated_std: float
    replicated_cv: float  # Coefficient of Variation (std / mean)
    max_relative_divergence: float
    within_tolerance: bool
    status: str  # "REPRODUCED", "DIVERGED", "INCONCLUSIVE"


@dataclass
class ReplicationPackage:
    """Complete multi-evaluator replication audit package."""
    study_name: str
    baseline_run: ReplicationRun
    independent_runs: List[ReplicationRun]
    metric_comparisons: List[MetricReplicationComparison]
    overall_reproducibility_score: float
    acm_badge_eligibility: str  # "ARTIFACTS_REUSABLE", "RESULTS_REPLICATED", "NONE"
    cryptographic_digest: str
    status: str  # "REPRODUCED", "PARTIAL", "FAILED"


class IndependentReplicationEngine:
    """
    Evaluates cross-environment and cross-evaluator reproducibility.
    """

    @staticmethod
    def capture_environment_fingerprint() -> Dict[str, Any]:
        """Capture standard environment attributes."""
        return {
            "os": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": sys.version.split()[0],
            "python_implementation": platform.python_implementation(),
        }

    @classmethod
    def compare_metrics(
        cls,
        baseline_metrics: Dict[str, float],
        replicated_runs: List[ReplicationRun],
        tolerance_ratio: float = 0.05
    ) -> List[MetricReplicationComparison]:
        """
        Compare baseline metric values against independent replicated runs.
        """
        if not replicated_runs:
            return []

        results: List[MetricReplicationComparison] = []
        for metric_name, baseline_val in baseline_metrics.items():
            rep_vals = [r.metric_values.get(metric_name) for r in replicated_runs if metric_name in r.metric_values]
            if not rep_vals:
                results.append(MetricReplicationComparison(
                    metric_name=metric_name,
                    baseline_value=baseline_val,
                    replicated_mean=0.0,
                    replicated_std=0.0,
                    replicated_cv=0.0,
                    max_relative_divergence=1.0,
                    within_tolerance=False,
                    status="INCONCLUSIVE"
                ))
                continue

            n = len(rep_vals)
            mean_val = sum(rep_vals) / n
            var = sum((x - mean_val) ** 2 for x in rep_vals) / (n - 1) if n > 1 else 0.0
            std_val = math.sqrt(var)
            cv = (std_val / mean_val) if abs(mean_val) > 1e-12 else 0.0

            # Max divergence from baseline
            max_divergence = max(abs(x - baseline_val) / max(abs(baseline_val), 1e-9) for x in rep_vals)
            within_tol = max_divergence <= tolerance_ratio

            status = "REPRODUCED" if within_tol else "DIVERGED"
            results.append(MetricReplicationComparison(
                metric_name=metric_name,
                baseline_value=baseline_val,
                replicated_mean=mean_val,
                replicated_std=std_val,
                replicated_cv=cv,
                max_relative_divergence=max_divergence,
                within_tolerance=within_tol,
                status=status
            ))

        return results

    @classmethod
    def evaluate_replication_package(
        cls,
        study_name: str,
        baseline_run: ReplicationRun,
        independent_runs: List[ReplicationRun],
        tolerance_ratio: float = 0.05
    ) -> ReplicationPackage:
        """
        Produce a certified replication package.
        """
        comparisons = cls.compare_metrics(
            baseline_metrics=baseline_run.metric_values,
            replicated_runs=independent_runs,
            tolerance_ratio=tolerance_ratio
        )

        total_metrics = len(comparisons)
        reproduced_metrics = sum(1 for c in comparisons if c.within_tolerance)

        score = (reproduced_metrics / total_metrics) if total_metrics > 0 else 0.0

        if score >= 0.90 and len(independent_runs) >= 2:
            badge = "RESULTS_REPLICATED"
            status = "REPRODUCED"
        elif score >= 0.70:
            badge = "ARTIFACTS_REUSABLE"
            status = "PARTIAL"
        else:
            badge = "NONE"
            status = "FAILED"

        # Cryptographic content hashing
        payload = {
            "study": study_name,
            "baseline": asdict(baseline_run),
            "runs": [asdict(r) for r in independent_runs],
            "score": score
        }
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

        return ReplicationPackage(
            study_name=study_name,
            baseline_run=baseline_run,
            independent_runs=independent_runs,
            metric_comparisons=comparisons,
            overall_reproducibility_score=score,
            acm_badge_eligibility=badge,
            cryptographic_digest=digest,
            status=status
        )
