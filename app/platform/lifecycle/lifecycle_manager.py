"""Extension Lifecycle Manager.

Manages dynamic install, enable, disable, upgrade, rollback, uninstall,
and version pinning for all platform plugins.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.platform.plugins.plugin_loader import (
    PluginContext,
    PluginLoader,
    PluginManifest,
    global_plugin_loader,
)


@dataclass
class PluginVersionRecord:
    version: str
    manifest_data: Dict[str, Any]
    installed_at: float = field(default_factory=time.time)


class LifecycleManager:
    def __init__(self, loader: Optional[PluginLoader] = None):
        self.loader = loader or global_plugin_loader
        self._version_history: Dict[str, List[PluginVersionRecord]] = {}
        self._action_log: List[Dict[str, Any]] = []

    def enable_plugin(self, plugin_id: str) -> bool:
        ctx = self.loader.get_plugin(plugin_id)
        if not ctx:
            return False
        ctx.is_enabled = True
        self._log_action("ENABLE", plugin_id)
        return True

    def disable_plugin(self, plugin_id: str) -> bool:
        ctx = self.loader.get_plugin(plugin_id)
        if not ctx:
            return False
        ctx.is_enabled = False
        self._log_action("DISABLE", plugin_id)
        return True

    def upgrade_plugin(self, plugin_id: str, new_manifest_data: Dict[str, Any]) -> PluginContext:
        ctx = self.loader.get_plugin(plugin_id)
        if ctx:
            # Save current version in history
            if plugin_id not in self._version_history:
                self._version_history[plugin_id] = []
            self._version_history[plugin_id].append(
                PluginVersionRecord(version=ctx.manifest.version, manifest_data=ctx.manifest.to_dict())
            )

        new_manifest = PluginManifest.from_dict(new_manifest_data)
        new_ctx = self.loader.load_plugin(new_manifest)
        self._log_action("UPGRADE", plugin_id, f"Upgraded to {new_manifest.version}")
        return new_ctx

    def rollback_plugin(self, plugin_id: str) -> Optional[PluginContext]:
        history = self._version_history.get(plugin_id, [])
        if not history:
            return None

        last_version = history.pop()
        prev_manifest = PluginManifest.from_dict(last_version.manifest_data)
        ctx = self.loader.load_plugin(prev_manifest)
        self._log_action("ROLLBACK", plugin_id, f"Rolled back to {prev_manifest.version}")
        return ctx

    def uninstall_plugin(self, plugin_id: str) -> bool:
        success = self.loader.unload_plugin(plugin_id)
        if success:
            self._log_action("UNINSTALL", plugin_id)
        return success

    def _log_action(self, action: str, plugin_id: str, details: str = "") -> None:
        self._action_log.append({
            "action": action,
            "plugin_id": plugin_id,
            "details": details,
            "timestamp": time.time(),
        })

    def get_action_log(self) -> List[Dict[str, Any]]:
        return list(self._action_log)


global_lifecycle_manager = LifecycleManager()
