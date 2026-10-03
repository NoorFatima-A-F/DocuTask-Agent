"""
Configuration Diff & Comparison Engine.
Identifies value changes, structure alterations, AI model drifts, and dependency mutations.
"""
from typing import Any, Dict, List, Union
from app.platform_verification.config_versioning.domain.models import ConfigurationDiff, ConfigurationSnapshot
from app.platform_verification.config_versioning.core.registry import configuration_registry

class ConfigurationDiffEngine:
    @staticmethod
    def compare_snapshots(source: ConfigurationSnapshot, target: ConfigurationSnapshot) -> ConfigurationDiff:
        s_cfg = source.resolved_configuration
        t_cfg = target.resolved_configuration

        modified: Dict[str, Dict[str, Any]] = {}
        added: Dict[str, Any] = {}
        removed: Dict[str, Any] = {}

        # Detect Added and Modified
        for k, v in t_cfg.items():
            if k not in s_cfg:
                added[k] = v
            elif s_cfg[k] != v:
                modified[k] = {"from": s_cfg[k], "to": v}

        # Detect Removed
        for k, v in s_cfg.items():
            if k not in t_cfg:
                removed[k] = v

        # AI Model Drift Check
        ai_drift = False
        s_ai = s_cfg.get("ai", {})
        t_ai = t_cfg.get("ai", {})
        if s_ai != t_ai:
            ai_drift = True

        has_changes = bool(modified or added or removed or (source.configuration_hash != target.configuration_hash))

        summary_parts = []
        if added:
            summary_parts.append(f"Added {len(added)} keys: {list(added.keys())}")
        if modified:
            summary_parts.append(f"Modified {len(modified)} keys: {list(modified.keys())}")
        if removed:
            summary_parts.append(f"Removed {len(removed)} keys: {list(removed.keys())}")
        if ai_drift:
            summary_parts.append("AI Model configuration drift detected.")

        human_summary = "; ".join(summary_parts) if summary_parts else "Identical configuration state."

        return ConfigurationDiff(
            source_snapshot_id=source.snapshot_id,
            target_snapshot_id=target.snapshot_id,
            has_changes=has_changes,
            modified_keys=modified,
            added_keys=added,
            removed_keys=removed,
            ai_model_drift=ai_drift,
            human_readable_summary=human_summary
        )

    def compare(self, source: Union[str, ConfigurationSnapshot], target: Union[str, ConfigurationSnapshot]) -> ConfigurationDiff:
        s = source if isinstance(source, ConfigurationSnapshot) else configuration_registry.get_snapshot(source)
        t = target if isinstance(target, ConfigurationSnapshot) else configuration_registry.get_snapshot(target)
        if not s:
            raise ValueError(f"Source snapshot '{source}' not found.")
        if not t:
            raise ValueError(f"Target snapshot '{target}' not found.")
        return self.compare_snapshots(s, t)

configuration_diff_engine = ConfigurationDiffEngine()
