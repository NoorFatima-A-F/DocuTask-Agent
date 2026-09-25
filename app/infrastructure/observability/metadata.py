"""
Deployment and Runtime Metadata Profiler.
Exposes Git commit, build time, SemVer version, environment tier, and hardware capabilities.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
import os
import platform

@dataclass(frozen=True)
class DeploymentMetadata:
    version: str = "1.0.0"
    environment: str = "development"
    git_commit: str = "HEAD"
    build_time: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    python_version: str = field(default_factory=platform.python_version)
    os_name: str = field(default_factory=platform.system)

class DeploymentMetadataProfiler:
    """Profiles runtime deployment parameters."""
    @staticmethod
    def get_metadata(env: str = "development") -> DeploymentMetadata:
        return DeploymentMetadata(
            version="1.0.0",
            environment=env,
            git_commit=os.getenv("GIT_COMMIT", "local-dev")
        )
