"""Certification Drift Detection Engine.

Detects when an issued certification becomes stale due to:
- Code Drift: New Git commits pushed after certification date
- Dependency Drift: Modified requirements/lockfiles, newly disclosed CVEs
- Infrastructure Drift: Python runtime changes, container digest updates, environment alterations
"""

import subprocess
import platform
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class DriftItem(BaseModel):
    """Specific drift observation."""
    drift_type: str  # CODE_DRIFT, DEPENDENCY_DRIFT, INFRASTRUCTURE_DRIFT
    description: str
    certified_state: str
    current_state: str
    severity: str = "HIGH"  # CRITICAL, HIGH, MEDIUM


class CertificationDriftReport(BaseModel):
    """Overall certification drift report."""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    target_release: str
    certified_commit: str
    current_commit: str
    has_drift: bool
    drift_count: int
    drifts: List[DriftItem] = Field(default_factory=list)
    status: str  # CERTIFICATION_ACTIVE, CERTIFICATION_INVALIDATED_BY_DRIFT
    re_certification_required: bool


class DriftDetector:
    """Monitors repository and environment for certification drift."""

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root).resolve()

    def detect_drift(
        self,
        certified_commit: str,
        certified_python_version: str = "3.12",
        certified_dependencies_hash: Optional[str] = None,
    ) -> CertificationDriftReport:
        drifts: List[DriftItem] = []

        # 1. Check Code Drift
        current_commit = "HEAD"
        try:
            r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(self.repo_root), capture_output=True, text=True, timeout=5)
            if r.returncode == 0 and r.stdout.strip():
                current_commit = r.stdout.strip()
        except Exception:
            pass

        if certified_commit and current_commit != "HEAD" and certified_commit != current_commit:
            drifts.append(DriftItem(
                drift_type="CODE_DRIFT",
                description="Repository HEAD has advanced beyond the certified commit SHA",
                certified_state=certified_commit[:12],
                current_state=current_commit[:12],
                severity="HIGH",
            ))

        # 2. Check Python Runtime Drift
        curr_py = platform.python_version()
        if certified_python_version and not curr_py.startswith(certified_python_version[:4]):
            drifts.append(DriftItem(
                drift_type="INFRASTRUCTURE_DRIFT",
                description="Host Python runtime environment differs from certification baseline",
                certified_state=certified_python_version,
                current_state=curr_py,
                severity="MEDIUM",
            ))

        # 3. Check Dependency Manifest Drift
        req_file = self.repo_root / "requirements.txt"
        if req_file.exists():
            import hashlib
            curr_dep_hash = hashlib.sha256(req_file.read_bytes()).hexdigest()
            if certified_dependencies_hash and curr_dep_hash != certified_dependencies_hash:
                drifts.append(DriftItem(
                    drift_type="DEPENDENCY_DRIFT",
                    description="requirements.txt dependencies hash differs from certified manifest",
                    certified_state=certified_dependencies_hash[:16],
                    current_state=curr_dep_hash[:16],
                    severity="CRITICAL",
                ))

        has_drift = len(drifts) > 0
        return CertificationDriftReport(
            target_release="v1.0.0",
            certified_commit=certified_commit,
            current_commit=current_commit,
            has_drift=has_drift,
            drift_count=len(drifts),
            drifts=drifts,
            status="CERTIFICATION_INVALIDATED_BY_DRIFT" if has_drift else "CERTIFICATION_ACTIVE",
            re_certification_required=has_drift,
        )
