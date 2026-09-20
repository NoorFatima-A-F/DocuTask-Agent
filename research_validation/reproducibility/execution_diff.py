"""
Execution Diff Comparator (Phase 82B.6)
=======================================
Compares multi-step execution traces, latency distributions, and memory
profiles across independent experiment runs.
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from research_validation.scientific_execution.experiment_runner import ExperimentRunResult
from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class ExecutionStepDelta:
    step_name: str
    base_hash: Optional[str]
    target_hash: Optional[str]
    is_identical: bool


@dataclass(frozen=True)
class ExecutionTraceDiffReport:
    base_run_id: str
    target_run_id: str
    is_exact_reproduction: bool
    status_match: bool
    latency_delta_ms: float
    latency_relative_ratio: float
    step_deltas: Tuple[ExecutionStepDelta, ...]
    differing_steps_count: int
    diff_hash: str


class ExecutionDiffComparator:
    """
    Compares two ExperimentRunResults step by step.
    """

    @classmethod
    def compare_runs(
        cls,
        base_run: ExperimentRunResult,
        target_run: ExperimentRunResult,
    ) -> ExecutionTraceDiffReport:
        """Execute fine-grained diff between two run results."""
        status_match = (base_run.status == target_run.status)
        lat_diff = target_run.duration_ms - base_run.duration_ms
        lat_ratio = (target_run.duration_ms / base_run.duration_ms) if base_run.duration_ms > 0 else 1.0

        # Step comparison
        all_steps = set(base_run.intermediate_hashes.keys()).union(set(target_run.intermediate_hashes.keys()))
        step_deltas: List[ExecutionStepDelta] = []
        differing_count = 0

        for step in sorted(all_steps):
            h1 = base_run.intermediate_hashes.get(step)
            h2 = target_run.intermediate_hashes.get(step)
            identical = (h1 == h2 and h1 is not None)
            if not identical:
                differing_count += 1
            step_deltas.append(ExecutionStepDelta(
                step_name=step,
                base_hash=h1,
                target_hash=h2,
                is_identical=identical,
            ))

        exact = status_match and (differing_count == 0) and (base_run.final_output_digest == target_run.final_output_digest)

        h_payload = {
            "base": base_run.run_id,
            "target": target_run.run_id,
            "exact": exact,
            "differing_steps": differing_count,
        }
        diff_h = hash_canonical_json(h_payload)

        return ExecutionTraceDiffReport(
            base_run_id=base_run.run_id,
            target_run_id=target_run.run_id,
            is_exact_reproduction=exact,
            status_match=status_match,
            latency_delta_ms=lat_diff,
            latency_relative_ratio=lat_ratio,
            step_deltas=tuple(step_deltas),
            differing_steps_count=differing_count,
            diff_hash=diff_h,
        )
