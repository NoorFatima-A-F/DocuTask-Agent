"""Version Manager Interface."""

from __future__ import annotations

from app.platform.lifecycle.lifecycle_manager import (
    LifecycleManager,
    PluginVersionRecord,
    global_lifecycle_manager,
)

__all__ = [
    "PluginVersionRecord",
    "LifecycleManager",
    "global_lifecycle_manager",
]
