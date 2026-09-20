"""
Plugin Isolation Policy.
Defines security policy rules governing allowed network endpoints and filesystem paths.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.agents.runtime.exceptions import PluginValidationError


class NetworkOriginDeniedError(PluginValidationError):
    """Raised when plugin attempts network access to an unauthorized origin."""
    pass


class PathAccessDeniedError(PluginValidationError):
    """Raised when plugin attempts filesystem access to an unauthorized path."""
    pass


class PluginIsolationPolicy(BaseModel):
    """Enforces fine-grained path and network egress boundaries."""
    allowed_read_paths: List[str] = Field(default_factory=list)
    allowed_write_paths: List[str] = Field(default_factory=list)
    allowed_network_hosts: List[str] = Field(default_factory=list)
    allowed_network_origins: List[str] = Field(default_factory=list)
    allowed_filesystem_paths: List[str] = Field(default_factory=list)
    allow_unrestricted_network: bool = False

    def __init__(
        self,
        allowed_read_paths: Optional[List[str]] = None,
        allowed_write_paths: Optional[List[str]] = None,
        allowed_network_hosts: Optional[List[str]] = None,
        allowed_network_origins: Optional[List[str]] = None,
        allowed_filesystem_paths: Optional[List[str]] = None,
        allow_unrestricted_network: bool = False,
        **data,
    ):
        hosts = allowed_network_origins if allowed_network_origins is not None else (allowed_network_hosts or [])
        paths = allowed_filesystem_paths if allowed_filesystem_paths is not None else (allowed_read_paths or [])
        super().__init__(
            allowed_read_paths=paths,
            allowed_write_paths=allowed_write_paths or [],
            allowed_network_hosts=hosts,
            allowed_network_origins=hosts,
            allowed_filesystem_paths=paths,
            allow_unrestricted_network=allow_unrestricted_network,
            **data,
        )

    def verify_network_access(self, host: str) -> None:
        """Verifies if plugin is authorized to connect to target network host."""
        if self.allow_unrestricted_network:
            return
        if host not in self.allowed_network_hosts and host not in self.allowed_network_origins:
            raise PluginValidationError(
                f"Network egress violation: Host '{host}' is not in allowed_network_hosts."
            )

    def assert_network_origin(self, origin: str) -> None:
        if self.allow_unrestricted_network:
            return
        if origin not in self.allowed_network_origins and origin not in self.allowed_network_hosts:
            raise NetworkOriginDeniedError(
                f"Network origin violation: '{origin}' is not permitted by isolation policy."
            )

    def assert_path_access(self, path: str) -> None:
        norm_path = path.replace("\\", "/").rstrip("/")
        for allowed in self.allowed_filesystem_paths:
            norm_allowed = allowed.replace("\\", "/").rstrip("/")
            if norm_path == norm_allowed or norm_path.startswith(norm_allowed + "/"):
                return
        raise PathAccessDeniedError(
            f"Path access violation: '{path}' is not within allowed filesystem paths {self.allowed_filesystem_paths}."
        )
