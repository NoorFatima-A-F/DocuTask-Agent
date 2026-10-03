"""
Continuous Configuration Drift Detector.
Compares live active state against approved golden snapshot.
"""
import hashlib
import json
from typing import Any, Dict, Union
from app.platform_verification.config_versioning.domain.models import DriftReport, EnvironmentTier, ConfigurationSnapshot
from app.platform_verification.config_versioning.core.registry import configuration_registry

class DriftDetector:
    @staticmethod
    def detect_drift(baseline: Union[str, ConfigurationSnapshot], current_config: Dict[str, Any]) -> DriftReport:
        if isinstance(baseline, ConfigurationSnapshot):
            baseline_snap = baseline
            baseline_id = baseline.snapshot_id
        else:
            baseline_snap = configuration_registry.get_snapshot(baseline)
            baseline_id = baseline
            if not baseline_snap:
                raise ValueError(f"Baseline snapshot '{baseline_id}' not found.")

        current_bytes = json.dumps(current_config, sort_keys=True, default=str).encode("utf-8")
        current_hash = hashlib.sha256(current_bytes).hexdigest()

        is_drifted = (current_hash != baseline_snap.configuration_hash)
        unauthorized = []

        if is_drifted:
            b_cfg = baseline_snap.resolved_configuration
            for k, v in current_config.items():
                if k not in b_cfg:
                    unauthorized.append(f"Unexpected injected key: '{k}'")
                elif b_cfg[k] != v:
                    unauthorized.append(f"Mutated key: '{k}' (baseline: {b_cfg[k]} -> current: {v})")
            for k in b_cfg:
                if k not in current_config:
                    unauthorized.append(f"Missing baseline key: '{k}'")

        return DriftReport(
            target_environment=baseline_snap.environment,
            baseline_snapshot_id=baseline_id,
            baseline_hash=baseline_snap.configuration_hash,
            current_hash=current_hash,
            is_drifted=is_drifted,
            unauthorized_mutations=unauthorized
        )

drift_detector = DriftDetector()
