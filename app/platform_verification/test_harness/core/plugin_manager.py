"""
Verification Plugin Framework and Registry.
"""
from __future__ import annotations
from typing import Dict, List, Optional
from app.platform_verification.test_harness.domain.interfaces import IVerificationPlugin


class PluginManager:
    """Manages custom verification extensions, evaluators, and runners."""

    def __init__(self) -> None:
        self._plugins: Dict[str, IVerificationPlugin] = {}

    def register_plugin(self, name: str, plugin: IVerificationPlugin) -> None:
        self._plugins[name] = plugin

    def get_plugin(self, name: str) -> Optional[IVerificationPlugin]:
        return self._plugins.get(name)

    def list_plugins(self) -> List[str]:
        return list(self._plugins.keys())
