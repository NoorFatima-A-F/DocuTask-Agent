"""Reproducibility Engine Package (Phase 8 AEEERP)."""

from app.runtime.reproducibility.dependency_capture import (
    DependencyCapture,
    DependencyLock,
    DependencyManifest,
)
from app.runtime.reproducibility.environment_capture import (
    EnvironmentCapture,
    EnvironmentFingerprint,
)
from app.runtime.reproducibility.reproducer import (
    ReproductionResult,
    Reproducer,
    global_reproducer,
)
from app.runtime.reproducibility.runtime_snapshot import RuntimeSnapshot
from app.runtime.reproducibility.snapshot_manager import (
    SnapshotManager,
    global_snapshot_manager,
)

__all__ = [
    "EnvironmentFingerprint",
    "EnvironmentCapture",
    "DependencyLock",
    "DependencyManifest",
    "DependencyCapture",
    "RuntimeSnapshot",
    "SnapshotManager",
    "global_snapshot_manager",
    "ReproductionResult",
    "Reproducer",
    "global_reproducer",
]
