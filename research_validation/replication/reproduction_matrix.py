"""
Independent Evidence & Real-World Validation Platform (IERVP)
Phase 56: Independent Reproduction Matrix Framework

Orchestrates multi-reviewer, multi-environment replication experiments:
- Developer A (Local Dev, Windows 11)
- Developer B (Secondary Dev, Ubuntu Linux 22.04 LTS)
- Independent Reviewer (Clean Box, macOS 14 Sonoma)
- Automated CI Runner (GitHub Actions / GitLab Runner)
- Cloud Production Container (Google Cloud Run / GKE)

Generates empirical reproduction matrices highlighting exact numerical divergences.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class EvaluatorRole(str, Enum):
    PRIMARY_DEV = "Developer A (Primary)"
    SECONDARY_DEV = "Developer B (Secondary)"
    INDEPENDENT_REVIEWER = "Independent Reviewer"
    CI_RUNNER = "Automated CI Runner"
    CLOUD_CONTAINER = "Cloud Run / Container"


@dataclass
class ReplicationExperimentRow:
    """A single row in the peer-reviewed reproduction matrix."""
    reviewer_role: EvaluatorRole
    environment_desc: str
    operating_system: str
    python_version: str
    target_metric_name: str
    baseline_value: float
    reproduced_value: float
    absolute_difference: float
    relative_difference: float
    same_result: bool  # True if divergence <= tolerance
    notes: str


@dataclass
class ReproductionMatrixReport:
    """Complete reproduction matrix report for artifact evaluation committees."""
    benchmark_name: str
    total_evaluators: int
    concordant_evaluators_count: int
    reproducibility_rate: float
    max_relative_divergence: float
    matrix_rows: List[ReplicationExperimentRow]
    matrix_table_markdown: str
    assumptions: List[str]
    limitations: List[str]
    reproducibility_instructions: str
    verdict: str  # "REPRODUCIBLE", "ACCEPTABLE_TOLERANCE", "DIVERGENT", "UNVERIFIED"


class IndependentReproductionMatrixLab:
    """
    Constructs and audits the cross-evaluator reproduction matrix.
    """

    @classmethod
    def generate_matrix_row(
        cls,
        role: EvaluatorRole,
        env_desc: str,
        os_name: str,
        py_ver: str,
        metric_name: str,
        baseline_val: float,
        reproduced_val: float,
        tolerance_rel: float = 0.02
    ) -> ReplicationExperimentRow:
        """Create a single matrix row with exact divergence calculation."""
        abs_diff = abs(baseline_val - reproduced_val)
        rel_diff = abs_diff / max(abs(baseline_val), 1e-12)
        is_same = rel_diff <= tolerance_rel

        notes = f"Replicated within {rel_diff*100:.2f}% tolerance." if is_same else f"Diverged by {rel_diff*100:.2f}% (> {tolerance_rel*100:.1f}% threshold)."

        return ReplicationExperimentRow(
            reviewer_role=role,
            environment_desc=env_desc,
            operating_system=os_name,
            python_version=py_ver,
            target_metric_name=metric_name,
            baseline_value=baseline_val,
            reproduced_value=reproduced_val,
            absolute_difference=abs_diff,
            relative_difference=rel_diff,
            same_result=is_same,
            notes=notes
        )

    @classmethod
    def format_matrix_markdown(cls, rows: List[ReplicationExperimentRow]) -> str:
        """Generate markdown table conforming to ACM/IEEE Artifact Evaluation standards."""
        lines = [
            "| Reviewer / Evaluator | Environment | OS | Baseline | Reproduced | Abs Diff | Rel Diff | Same Result | Notes |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
        ]
        for r in rows:
            same_str = "**YES**" if r.same_result else "**NO**"
            lines.append(
                f"| {r.reviewer_role.value} | {r.environment_desc} | {r.operating_system} | "
                f"{r.baseline_value:.4f} | {r.reproduced_value:.4f} | {r.absolute_difference:.2e} | "
                f"{r.relative_difference*100:.2f}% | {same_str} | {r.notes} |"
            )
        return "\n".join(lines)

    @classmethod
    def build_reproduction_study(
        cls,
        benchmark_name: str,
        metric_name: str,
        baseline_val: float,
        evaluator_results: List[Tuple[EvaluatorRole, str, str, str, float]],
        tolerance_rel: float = 0.02
    ) -> ReproductionMatrixReport:
        """
        Build full reproduction matrix across all evaluator submissions.
        evaluator_results: List of (role, env_desc, os_name, py_ver, rep_val)
        """
        if not evaluator_results:
            return ReproductionMatrixReport(
                benchmark_name=benchmark_name,
                total_evaluators=0,
                concordant_evaluators_count=0,
                reproducibility_rate=0.0,
                max_relative_divergence=0.0,
                matrix_rows=[],
                matrix_table_markdown="| Empty Matrix |",
                assumptions=["Evaluator submissions provided"],
                limitations=["No evaluator executions recorded"],
                reproducibility_instructions="Execute benchmark across at least 2 independent environments",
                verdict="UNVERIFIED"
            )

        rows = [
            cls.generate_matrix_row(role, env, os_n, py_v, metric_name, baseline_val, val, tolerance_rel=tolerance_rel)
            for role, env, os_n, py_v, val in evaluator_results
        ]

        total = len(rows)
        concordant = sum(1 for r in rows if r.same_result)
        rate = concordant / total
        max_div = max(r.relative_difference for r in rows)

        table_md = cls.format_matrix_markdown(rows)

        verdict = "REPRODUCIBLE" if rate == 1.0 else "ACCEPTABLE_TOLERANCE" if rate >= 0.80 else "DIVERGENT"

        return ReproductionMatrixReport(
            benchmark_name=benchmark_name,
            total_evaluators=total,
            concordant_evaluators_count=concordant,
            reproducibility_rate=rate,
            max_relative_divergence=max_div,
            matrix_rows=rows,
            matrix_table_markdown=table_md,
            assumptions=[
                "Independent environments configured with pinned dependency versions",
                "Deterministic random seed applied across all evaluator runs"
            ],
            limitations=[
                "Floating point operations across diverse CPU architectures (x86_64 vs ARM64) may cause sub-ULP variation"
            ],
            reproducibility_instructions="Clone repository, execute `poetry install`, and run `poetry run pytest tests/` with specified seed.",
            verdict=verdict
        )
