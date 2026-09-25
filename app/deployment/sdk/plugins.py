"""Deployment Lifecycle Plugin Architecture."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)


class DeploymentPlugin(ABC):
    """Base interface for deployment lifecycle extension plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier of the plugin."""
        pass

    def pre_deploy(self, context: Dict[str, Any]) -> bool:
        """Hook executed before deployment begins."""
        return True

    def post_deploy(self, context: Dict[str, Any]) -> None:
        """Hook executed after deployment successfully concludes."""
        pass

    def pre_rollback(self, context: Dict[str, Any]) -> bool:
        """Hook executed before rollback begins."""
        return True

    def post_rollback(self, context: Dict[str, Any]) -> None:
        """Hook executed after rollback completes."""
        pass


class PluginManager:
    """Dispatches lifecycle events across registered deployment plugins."""

    def __init__(self):
        self._plugins: Dict[str, DeploymentPlugin] = {}

    def register(self, plugin: DeploymentPlugin) -> None:
        """Registers a lifecycle plugin."""
        self._plugins[plugin.name] = plugin

    def unregister(self, plugin_name: str) -> None:
        """Removes a registered plugin."""
        self._plugins.pop(plugin_name, None)

    def list_plugins(self) -> List[str]:
        """Returns list of registered plugin names."""
        return list(self._plugins.keys())

    def run_pre_deploy(self, context: Dict[str, Any]) -> bool:
        """Executes pre-deploy hooks. If any returns False, deployment is halted."""
        for name, plugin in self._plugins.items():
            try:
                allowed = plugin.pre_deploy(context)
                if not allowed:
                    logger.warning("Plugin '%s' rejected pre_deploy hook", name)
                    return False
            except Exception as e:
                logger.error("Plugin '%s' pre_deploy error: %s", name, e)
                return False
        return True

    def run_post_deploy(self, context: Dict[str, Any]) -> None:
        """Executes post-deploy hooks across all plugins."""
        for name, plugin in self._plugins.items():
            try:
                plugin.post_deploy(context)
            except Exception as e:
                logger.error("Plugin '%s' post_deploy error: %s", name, e)

    def run_pre_rollback(self, context: Dict[str, Any]) -> bool:
        """Executes pre-rollback hooks."""
        for name, plugin in self._plugins.items():
            try:
                if not plugin.pre_rollback(context):
                    return False
            except Exception as e:
                logger.error("Plugin '%s' pre_rollback error: %s", name, e)
                return False
        return True

    def run_post_rollback(self, context: Dict[str, Any]) -> None:
        """Executes post-rollback hooks."""
        for name, plugin in self._plugins.items():
            try:
                plugin.post_rollback(context)
            except Exception as e:
                logger.error("Plugin '%s' post_rollback error: %s", name, e)
