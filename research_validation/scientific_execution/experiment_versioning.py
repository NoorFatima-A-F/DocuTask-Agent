"""
Experiment Versioning & Lineage Evolution (Phase 82B.3)
======================================================
Semantic version management for scientific experiments (Major.Minor.Patch).
Detects breaking configuration shifts, parameter drifts, and dataset alterations.
"""

from __future__ import annotations
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict

from research_validation.scientific_execution.experiment_manifest import ExperimentManifest


class VersionChangeType(str, Enum):
    MAJOR_BREAKING = "MAJOR_BREAKING"          # Dataset changed or target metrics altered
    MINOR_FEATURE = "MINOR_FEATURE"            # New parameters added with backward compatibility
    PATCH_STABILIZATION = "PATCH_STABILIZATION"# Parameter tuning / seed changes
    NO_CHANGE = "NO_CHANGE"


@dataclass(frozen=True)
class SemanticVersion:
    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, version_str: str) -> SemanticVersion:
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version_str.strip())
        if not match:
            return cls(1, 0, 0)
        return cls(int(match.group(1)), int(match.group(2)), int(match.group(3)))

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def next_version(self, change_type: VersionChangeType) -> SemanticVersion:
        if change_type == VersionChangeType.MAJOR_BREAKING:
            return SemanticVersion(self.major + 1, 0, 0)
        elif change_type == VersionChangeType.MINOR_FEATURE:
            return SemanticVersion(self.major, self.minor + 1, 0)
        elif change_type == VersionChangeType.PATCH_STABILIZATION:
            return SemanticVersion(self.major, self.minor, self.patch + 1)
        return self


@dataclass(frozen=True)
class VersionDiffReport:
    previous_version: str
    current_version: str
    change_type: VersionChangeType
    is_backward_compatible: bool
    dataset_changed: bool
    parameter_deltas: Dict[str, Any]
    summary_message: str


class ExperimentVersionManager:
    """
    Compares two experiment manifests and determines semantic version progression.
    """

    @classmethod
    def diff_manifests(
        cls,
        base_manifest: ExperimentManifest,
        new_manifest: ExperimentManifest,
    ) -> VersionDiffReport:
        """Compare manifests and classify version evolution."""
        param_deltas: Dict[str, Any] = {}

        # 1. Check Dataset
        dataset_changed = (
            base_manifest.dataset.sha256_checksum != new_manifest.dataset.sha256_checksum
            or base_manifest.dataset.dataset_name != new_manifest.dataset.dataset_name
        )

        # 2. Check Target Metrics
        base_metrics = set(base_manifest.parameters.target_metrics)
        new_metrics = set(new_manifest.parameters.target_metrics)
        metrics_changed = base_metrics != new_metrics

        # 3. Check Parameters
        base_p = base_manifest.parameters.custom_parameters
        new_p = new_manifest.parameters.custom_parameters
        for k, v in new_p.items():
            if k not in base_p or base_p[k] != v:
                param_deltas[k] = {"old": base_p.get(k), "new": v}

        if base_manifest.parameters.sample_count != new_manifest.parameters.sample_count:
            param_deltas["sample_count"] = {
                "old": base_manifest.parameters.sample_count,
                "new": new_manifest.parameters.sample_count,
            }

        # Classify change
        if dataset_changed or metrics_changed:
            change_type = VersionChangeType.MAJOR_BREAKING
            is_compat = False
            msg = "Major version bump: Dataset or target metric specification changed."
        elif param_deltas:
            change_type = VersionChangeType.MINOR_FEATURE
            is_compat = True
            msg = "Minor version bump: Execution parameters or hyperparameters updated."
        elif base_manifest.parameters.seed != new_manifest.parameters.seed:
            change_type = VersionChangeType.PATCH_STABILIZATION
            is_compat = True
            msg = "Patch version bump: Random seed alteration."
        else:
            change_type = VersionChangeType.NO_CHANGE
            is_compat = True
            msg = "Identical experiment specification."

        return VersionDiffReport(
            previous_version=base_manifest.semantic_version,
            current_version=new_manifest.semantic_version,
            change_type=change_type,
            is_backward_compatible=is_compat,
            dataset_changed=dataset_changed,
            parameter_deltas=param_deltas,
            summary_message=msg,
        )
