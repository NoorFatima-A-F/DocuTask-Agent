"""GitOps Reconciler and Drift Detection."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import json

from .synchronizer import GitOpsManifest, GitOpsSynchronizer


class DriftType(str, Enum):
    """Types of detected GitOps drift."""
    MISSING = "missing"      # Exists in desired state, absent in actual cluster
    MODIFIED = "modified"    # Spec differs between desired and actual
    EXTRA = "extra"          # Exists in actual cluster, absent in desired state


@dataclass
class DriftItem:
    """A detected divergence between desired and actual state."""
    resource_key: str
    drift_type: DriftType
    desired_spec: Optional[Dict[str, Any]] = None
    actual_spec: Optional[Dict[str, Any]] = None
    detected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class GitOpsReconciler:
    """Detects configuration drift and applies corrections to converge actual to desired state."""

    def __init__(self, synchronizer: GitOpsSynchronizer) -> None:
        self.synchronizer = synchronizer

    def detect_drift(self, environment: str, actual_resources: Dict[str, Dict[str, Any]]) -> List[DriftItem]:
        """Compare desired manifests with actual runtime resources."""
        desired_manifests = self.synchronizer.list_manifests_for_environment(environment)
        desired_map = {f"{m.kind}:{m.namespace}:{m.name}": m for m in desired_manifests}

        drifts: List[DriftItem] = []

        # 1. Check for missing or modified
        for key, desired in desired_map.items():
            if key not in actual_resources:
                drifts.append(DriftItem(
                    resource_key=key,
                    drift_type=DriftType.MISSING,
                    desired_spec=desired.desired_spec,
                ))
            else:
                actual = actual_resources[key]
                if self._specs_differ(desired.desired_spec, actual):
                    drifts.append(DriftItem(
                        resource_key=key,
                        drift_type=DriftType.MODIFIED,
                        desired_spec=desired.desired_spec,
                        actual_spec=actual,
                    ))

        # 2. Check for extra unmanaged resources
        for key, actual in actual_resources.items():
            if key not in desired_map:
                drifts.append(DriftItem(
                    resource_key=key,
                    drift_type=DriftType.EXTRA,
                    actual_spec=actual,
                ))

        return drifts

    def reconcile_drift(self, environment: str, actual_resources: Dict[str, Dict[str, Any]]) -> int:
        """Correct drift by applying desired specs directly into the actual state dictionary."""
        drifts = self.detect_drift(environment, actual_resources)
        corrections = 0

        for d in drifts:
            if d.drift_type in (DriftType.MISSING, DriftType.MODIFIED) and d.desired_spec:
                actual_resources[d.resource_key] = json.loads(json.dumps(d.desired_spec))
                corrections += 1
            elif d.drift_type == DriftType.EXTRA:
                del actual_resources[d.resource_key]
                corrections += 1

        return corrections

    def _specs_differ(self, desired: Dict[str, Any], actual: Dict[str, Any]) -> bool:
        """Check if desired and actual specs diverge."""
        d_str = json.dumps(desired, sort_keys=True)
        a_str = json.dumps(actual, sort_keys=True)
        return d_str != a_str
