"""GitOps Controller and State Reconciliation Engine (Req 25, 27)."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid

from .drift import DriftDetector, DriftPolicyAction, DriftReport
from .providers.argocd import ArgoCDProvider
from .providers.base import GitOpsProvider


@dataclass
class GitOpsApplicationRecord:
    app_name: str
    environment: str
    desired_version: str
    observed_version: str
    sync_status: str = "Synced"
    health_status: str = "Healthy"
    last_reconciled_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    drift_detected: bool = False


class GitOpsController:
    """Reconciles declarative Git desired states with live cluster infrastructure."""

    def __init__(self, provider: Optional[GitOpsProvider] = None):
        self.provider = provider or ArgoCDProvider()
        self._applications: Dict[str, GitOpsApplicationRecord] = {}

    def register_application(
        self,
        app_name: str,
        environment: str,
        initial_version: str,
    ) -> GitOpsApplicationRecord:
        rec = GitOpsApplicationRecord(
            app_name=app_name,
            environment=environment,
            desired_version=initial_version,
            observed_version=initial_version,
        )
        self._applications[app_name] = rec
        return rec

    def get_application(self, app_name: str) -> Optional[GitOpsApplicationRecord]:
        return self._applications.get(app_name)

    def set_desired_version(self, app_name: str, new_version: str) -> GitOpsApplicationRecord:
        rec = self._applications.get(app_name)
        if not rec:
            raise KeyError(f"Application '{app_name}' not registered in GitOps controller")
        rec.desired_version = new_version
        rec.drift_detected = rec.desired_version != rec.observed_version
        return rec

    def reconcile(self, app_name: str) -> GitOpsApplicationRecord:
        rec = self._applications.get(app_name)
        if not rec:
            raise KeyError(f"Application '{app_name}' not registered in GitOps controller")

        sync_res = self.provider.sync_application(app_name, rec.desired_version)
        rec.observed_version = rec.desired_version
        rec.sync_status = sync_res.sync_status
        rec.health_status = sync_res.health_status
        rec.last_reconciled_at = datetime.now(timezone.utc)
        rec.drift_detected = False
        return rec

    def check_drift(self, app_name: str) -> DriftReport:
        rec = self._applications.get(app_name)
        if not rec:
            raise KeyError(f"Application '{app_name}' not registered")

        desired = {"version": rec.desired_version}
        actual = {"version": rec.observed_version}
        return DriftDetector.detect_drift(
            environment=rec.environment,
            component=app_name,
            desired_state=desired,
            actual_state=actual,
        )
