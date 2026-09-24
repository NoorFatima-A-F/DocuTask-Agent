"""
Platform Runtime Configuration.
Structured Pydantic v2 configuration governing runtime timeouts, concurrency, environments, and feature flags.
"""

from typing import Any, Dict
from pydantic import BaseModel, Field
from app.agents.runtime.feature_flags import RuntimeFeatureFlags


class PlatformRuntimeConfig(BaseModel):
    """Configuration governing the Enterprise Agent Platform Runtime Kernel."""
    environment: str = Field(default="DEV")
    max_concurrent_sessions: int = Field(default=1000, gt=0)
    startup_timeout_seconds: float = Field(default=60.0, gt=0.0)
    shutdown_drain_seconds: float = Field(default=30.0, gt=0.0)
    enable_supervisor: bool = True
    workspace_root: str = Field(default="/tmp/antigravity/workspaces")
    feature_flags: RuntimeFeatureFlags = Field(default_factory=RuntimeFeatureFlags)
    extra_properties: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}
