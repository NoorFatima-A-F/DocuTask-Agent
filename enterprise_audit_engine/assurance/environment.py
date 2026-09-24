"""Deterministic Environmental Telemetry & Execution Provenance."""

import platform
import subprocess
import sys
import hashlib
from pathlib import Path
from typing import Dict
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class CertificationExecutionEnvironment(BaseModel):
    """Immutable environmental snapshot captured during certification execution."""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    python_version: str
    python_executable: str
    os_name: str
    os_platform: str = ""
    os_release: str
    architecture: str
    cpu_architecture: str = ""
    hostname: str = ""
    hostname_hash: str
    git_commit: str
    git_branch: str
    git_dirty: bool
    dependency_versions: Dict[str, str] = Field(default_factory=dict)
    timezone: str = "UTC"
    execution_timestamp: str = ""
    environment_hash: str = ""

    @classmethod
    def capture_environment(cls, repo_root: Path) -> "CertificationExecutionEnvironment":
        """Captures host environment parameters for audit provenance."""
        # Git information
        commit = "HEAD"
        branch = "main"
        is_dirty = False
        try:
            r1 = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(repo_root), capture_output=True, text=True, timeout=5)
            if r1.returncode == 0 and r1.stdout.strip():
                commit = r1.stdout.strip()
            r2 = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=str(repo_root), capture_output=True, text=True, timeout=5)
            if r2.returncode == 0 and r2.stdout.strip():
                branch = r2.stdout.strip()
            r3 = subprocess.run(["git", "status", "--porcelain"], cwd=str(repo_root), capture_output=True, text=True, timeout=5)
            if r3.returncode == 0:
                is_dirty = len(r3.stdout.strip()) > 0
        except Exception:
            pass

        # Python dependencies
        deps = {}
        try:
            import pydantic
            deps["pydantic"] = pydantic.__version__
        except Exception:
            pass
        try:
            import cryptography
            deps["cryptography"] = cryptography.__version__
        except Exception:
            pass
        try:
            import pytest
            deps["pytest"] = pytest.__version__
        except Exception:
            pass

        node = platform.node()
        host_hash = hashlib.sha256(node.encode("utf-8")).hexdigest()[:16]
        now_iso = datetime.now(timezone.utc).isoformat()
        
        env_raw = f"{platform.python_version()}:{platform.system()}:{platform.release()}:{platform.machine()}:{commit}"
        env_hash = hashlib.sha256(env_raw.encode("utf-8")).hexdigest()

        return cls(
            timestamp=now_iso,
            python_version=platform.python_version(),
            python_executable=sys.executable,
            os_name=platform.system(),
            os_platform=platform.platform(),
            os_release=platform.release(),
            architecture=platform.machine(),
            cpu_architecture=platform.processor() or platform.machine(),
            hostname=node,
            hostname_hash=host_hash,
            git_commit=commit,
            git_branch=branch,
            git_dirty=is_dirty,
            dependency_versions=deps,
            timezone=datetime.now(timezone.utc).tzname() or "UTC",
            execution_timestamp=now_iso,
            environment_hash=env_hash,
        )


class EnvironmentCollector:
    """Collector helper for capturing execution environment."""

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root).resolve()

    def capture_environment(self) -> CertificationExecutionEnvironment:
        return CertificationExecutionEnvironment.capture_environment(self.repo_root)
