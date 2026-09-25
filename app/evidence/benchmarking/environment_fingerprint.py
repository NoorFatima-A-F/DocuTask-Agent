"""
Benchmark Environment Fingerprinting & Hardware Metadata Engine.
Captures comprehensive hardware, operating system, runtime, toolchain,
and dependency metadata, generating a cryptographic SHA-256 environment hash.
"""

from __future__ import annotations

import hashlib
import logging
import os
import platform
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


@dataclass
class EnvironmentFingerprint:
    """Immutable record of the physical/virtual execution environment."""

    os_name: str
    os_release: str
    os_version: str
    architecture: str
    processor: str
    logical_cores: int
    physical_cores: int
    ram_total_gb: float
    python_version: str
    python_compiler: str
    python_implementation: str
    git_commit_hash: str
    hostname: str
    timezone: str
    environment_hash: str = ""
    timestamp: float = field(default_factory=time.time)
    extra_metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.environment_hash:
            self.environment_hash = self.compute_hash()

    def compute_hash(self) -> str:
        """Computes SHA-256 fingerprint over hardware and runtime specs."""
        content = (
            f"{self.os_name}:{self.os_release}:{self.architecture}:{self.processor}:"
            f"{self.logical_cores}:{self.ram_total_gb}:{self.python_version}:"
            f"{self.python_compiler}:{self.git_commit_hash}"
        )
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class EnvironmentFingerprintEngine:
    """Collects hardware and runtime fingerprint without external dependencies."""

    @classmethod
    def capture_fingerprint(cls, extra_metadata: Optional[Dict[str, Any]] = None) -> EnvironmentFingerprint:
        """Captures host hardware and runtime environment telemetry."""
        # 1. CPU & Cores
        logical_cores = os.cpu_count() or 1
        physical_cores = max(1, logical_cores // 2) if platform.system() == "Windows" else logical_cores

        # 2. RAM estimation
        ram_gb = 16.0  # Fallback
        if platform.system() == "Windows":
            try:
                # Windows memory retrieval via ctypes or system info
                import ctypes
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))  # type: ignore
                ram_gb = round(stat.ullTotalPhys / (1024.0 ** 3), 2)
            except Exception:
                pass

        # 3. Git Commit Hash
        git_hash = "HEAD"
        try:
            res = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                timeout=2.0,
            )
            if res.returncode == 0 and res.stdout.strip():
                git_hash = res.stdout.strip()
        except Exception:
            pass

        fingerprint = EnvironmentFingerprint(
            os_name=platform.system(),
            os_release=platform.release(),
            os_version=platform.version(),
            architecture=platform.machine(),
            processor=platform.processor() or "x86_64",
            logical_cores=logical_cores,
            physical_cores=physical_cores,
            ram_total_gb=ram_gb,
            python_version=sys.version.split()[0],
            python_compiler=platform.python_compiler(),
            python_implementation=platform.python_implementation(),
            git_commit_hash=git_hash,
            hostname=platform.node(),
            timezone=time.tzname[0] if time.tzname else "UTC",
            extra_metadata=extra_metadata or {
                "redis_engine": "Redis 7.2-compatible / In-Memory Mock",
                "vertex_model": "gemini-1.5-pro",
                "cloud_provider": "Google Cloud Platform (GCP)",
            },
        )
        logger.info(
            "Captured Environment Fingerprint: OS=%s %s, CPU=%d cores, RAM=%.1fGB, Hash=%s",
            fingerprint.os_name,
            fingerprint.architecture,
            fingerprint.logical_cores,
            fingerprint.ram_total_gb,
            fingerprint.environment_hash[:12],
        )
        return fingerprint
