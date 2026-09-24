"""Cluster Labeling and Scheduling Metadata System."""

import re
from typing import Any, Dict, List, Tuple, Union
from pydantic import BaseModel, Field


class LabelSelector(BaseModel):
    """Selector for filtering clusters by labels."""

    match_labels: Dict[str, str] = Field(default_factory=dict)
    match_expressions: List[Dict[str, Any]] = Field(default_factory=list)


class ClusterLabelingSystem:
    """Validates, indexes, and queries key-value labels on clusters."""

    KEY_REGEX = re.compile(r"^([a-z0-9A-Z_.\-/]+)$")
    VAL_REGEX = re.compile(r"^([a-z0-9A-Z_.\-]*)$")

    def __init__(self) -> None:
        self._labels: Dict[str, Dict[str, str]] = {}  # cluster_id -> labels

    def validate_labels(self, labels: Dict[str, str]) -> Tuple[bool, List[str]]:
        """Validate label keys and values according to standard regex."""
        errors: List[str] = []
        for k, v in labels.items():
            if not self.KEY_REGEX.match(k):
                errors.append(f"Invalid label key: '{k}'")
            if not self.VAL_REGEX.match(str(v)):
                errors.append(f"Invalid label value: '{v}' for key '{k}'")
        return len(errors) == 0, errors

    def set_labels(self, cluster_id: str, labels: Dict[str, str]) -> None:
        is_valid, errors = self.validate_labels(labels)
        if not is_valid:
            raise ValueError("; ".join(errors))
        self._labels[cluster_id] = dict(labels)

    def get_labels(self, cluster_id: str) -> Dict[str, str]:
        return dict(self._labels.get(cluster_id, {}))

    def matches_selector(
        self,
        target: Union[str, Dict[str, str]],
        selector: Dict[str, str],
    ) -> Tuple[bool, List[str]]:
        """Check if label set matches selector requirements."""
        if isinstance(target, str):
            cluster_labels = self.get_labels(target)
        else:
            cluster_labels = target or {}

        errors: List[str] = []
        for k, v in selector.items():
            if cluster_labels.get(k) != str(v):
                errors.append(
                    f"Label mismatch: expected '{k}={v}', found '{cluster_labels.get(k)}'"
                )

        return len(errors) == 0, errors

    def find_clusters_by_labels(self, match_labels: Dict[str, str]) -> List[str]:
        return [
            cid for cid in self._labels.keys()
            if self.matches_selector(cid, match_labels)[0]
        ]
