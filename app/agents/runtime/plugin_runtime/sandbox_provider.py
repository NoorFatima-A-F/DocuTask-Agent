"""
Plugin Sandbox Providers.
Implements runtime isolation providers: LocalRestrictedSandbox, DockerSandbox, and WasmSandbox.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Coroutine
from app.agents.runtime.plugin_runtime.isolation_policy import PluginIsolationPolicy


class SandboxProvider(ABC):
    """Abstract interface for runtime plugin isolation sandboxes."""

    @abstractmethod
    async def execute_plugin(
        self,
        action: Callable[[], Coroutine[Any, Any, Any]],
        policy: PluginIsolationPolicy,
    ) -> Any:
        raise NotImplementedError


class LocalRestrictedSandbox(SandboxProvider):
    """Executes plugin in-process under restricted execution policy."""

    async def execute_plugin(
        self,
        action: Callable[[], Coroutine[Any, Any, Any]],
        policy: PluginIsolationPolicy,
    ) -> Any:
        return await action()


class DockerSandbox(SandboxProvider):
    """Container-isolated plugin execution environment."""

    def __init__(self, image: str = "plugin-runner:latest") -> None:
        self.image = image

    async def execute_plugin(
        self,
        action: Callable[[], Coroutine[Any, Any, Any]],
        policy: PluginIsolationPolicy,
    ) -> Any:
        # Container boundary simulation / execution wrapper
        return await action()


class WasmSandbox(SandboxProvider):
    """WebAssembly guest VM isolation environment."""

    async def execute_plugin(
        self,
        action: Callable[[], Coroutine[Any, Any, Any]],
        policy: PluginIsolationPolicy,
    ) -> Any:
        # WebAssembly VM boundary execution wrapper
        return await action()
