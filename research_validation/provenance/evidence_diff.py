"""
Evidence Provenance & Scientific Lineage Framework
Module: evidence_diff.py

Compares two scientific evidence bundles and highlights:
- Metric regressions / improvements
- Changed assumptions and methodology
- Changed configuration and hyperparameter hashes
- Changed dataset versions and model versions
- Changed git commit SHAs and software package versions
- Evidence quality level progressions or regressions
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from research_validation.provenance.provenance_models import EvidenceNode, EvidenceQualityLevel


@dataclass
class MetricDelta:
    """Quantitative divergence between two versions of a metric."""
    metric_name: str
    baseline_value: float
    comparison_value: float
    absolute_delta: float
    relative_delta_pct: float
    is_improved: bool


@dataclass
class EnvironmentDelta:
    """Differences in runtime hardware or software dependencies."""
    git_commit_changed: bool
    baseline_commit: str
    comparison_commit: str
    package_version_changes: Dict[str, Tuple[str, str]]  # pkg -> (baseline_ver, comp_ver)
    config_hash_changed: bool
    dataset_version_changed: bool
    model_version_changed: bool


@dataclass
class EvidenceBundleDiffReport:
    """Comprehensive difference report between two evidence bundles."""
    baseline_bundle_id: str
    comparison_bundle_id: str
    metric_deltas: List[MetricDelta]
    environment_delta: EnvironmentDelta
    quality_level_changed: bool
    baseline_quality: EvidenceQualityLevel
    comparison_quality: EvidenceQualityLevel
    added_nodes_count: int
    removed_nodes_count: int
    modified_nodes_count: int
    summary_markdown: str


class EvidenceDiffer:
    """
    Computes structured diffs between scientific evidence graphs and nodes.
    """

    @classmethod
    def compare_nodes(
        cls,
        baseline_node: EvidenceNode,
        comparison_node: EvidenceNode
    ) -> EvidenceBundleDiffReport:
        """Compare two specific evidence nodes and their environments."""
        # 1. Metric deltas
        deltas: List[MetricDelta] = []
        b_payload = baseline_node.payload
        c_payload = comparison_node.payload

        common_keys = set(b_payload.keys()).intersection(set(c_payload.keys()))
        for k in common_keys:
            v_base = b_payload[k]
            v_comp = c_payload[k]
            if isinstance(v_base, (int, float)) and isinstance(v_comp, (int, float)):
                abs_d = v_comp - v_base
                rel_pct = (abs_d / max(abs(v_base), 1e-12)) * 100.0
                is_imp = abs_d >= 0 if "error" not in k.lower() and "latency" not in k.lower() else abs_d <= 0
                deltas.append(MetricDelta(
                    metric_name=k,
                    baseline_value=float(v_base),
                    comparison_value=float(v_comp),
                    absolute_delta=abs_d,
                    relative_delta_pct=rel_pct,
                    is_improved=is_imp
                ))

        # 2. Environment deltas
        b_env = baseline_node.environment
        c_env = comparison_node.environment

        pkg_changes: Dict[str, Tuple[str, str]] = {}
        all_pkgs = set(b_env.package_versions.keys()).union(set(c_env.package_versions.keys()))
        for p in all_pkgs:
            v1 = b_env.package_versions.get(p, "NOT_INSTALLED")
            v2 = c_env.package_versions.get(p, "NOT_INSTALLED")
            if v1 != v2:
                pkg_changes[p] = (v1, v2)

        env_delta = EnvironmentDelta(
            git_commit_changed=(b_env.git_commit_sha != c_env.git_commit_sha),
            baseline_commit=b_env.git_commit_sha,
            comparison_commit=c_env.git_commit_sha,
            package_version_changes=pkg_changes,
            config_hash_changed=(b_env.config_hash != c_env.config_hash),
            dataset_version_changed=(b_env.dataset_version != c_env.dataset_version),
            model_version_changed=(b_env.model_version != c_env.model_version)
        )

        qual_changed = (baseline_node.quality_level != comparison_node.quality_level)

        # Generate markdown summary table
        md_lines = [
            f"### Evidence Diff: `{baseline_node.node_id}` vs `{comparison_node.node_id}`",
            "",
            f"- **Baseline Quality**: `{baseline_node.quality_level.value}`",
            f"- **Comparison Quality**: `{comparison_node.quality_level.value}`",
            f"- **Git Commit**: `{b_env.git_commit_sha[:8]}` → `{c_env.git_commit_sha[:8]}`",
            "",
            "| Metric | Baseline | Comparison | Absolute Delta | Relative Change | Improved |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |"
        ]
        for d in deltas:
            imp_str = "YES" if d.is_improved else "REGRESSED"
            md_lines.append(
                f"| `{d.metric_name}` | {d.baseline_value:.4f} | {d.comparison_value:.4f} | "
                f"{d.absolute_delta:+.4f} | {d.relative_delta_pct:+.2f}% | **{imp_str}** |"
            )

        return EvidenceBundleDiffReport(
            baseline_bundle_id=baseline_node.node_id,
            comparison_bundle_id=comparison_node.node_id,
            metric_deltas=deltas,
            environment_delta=env_delta,
            quality_level_changed=qual_changed,
            baseline_quality=baseline_node.quality_level,
            comparison_quality=comparison_node.quality_level,
            added_nodes_count=0,
            removed_nodes_count=0,
            modified_nodes_count=1,
            summary_markdown="\n".join(md_lines)
        )
