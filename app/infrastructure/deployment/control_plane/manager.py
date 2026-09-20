"""Deployment Control Plane Manager orchestrating deployment authority, concurrency, and gates."""

from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Set
import logging
import threading
import uuid

from .state import DeploymentRecord, DeploymentStatus, DeploymentStrategyType, DeploymentHistoryTracker
from .orchestrator import DeploymentOrchestrator

logger = logging.getLogger("app.infrastructure.deployment.control_plane")


class DeploymentControlPlaneManager:
    """Central authority governing deployments across environments with concurrency and safety gates."""

    def __init__(
        self,
        history_tracker: Optional[DeploymentHistoryTracker] = None,
        orchestrator: Optional[DeploymentOrchestrator] = None,
    ) -> None:
        self.history_tracker = history_tracker or DeploymentHistoryTracker()
        self.orchestrator = orchestrator or DeploymentOrchestrator()
        self._active_deployments: Set[str] = set()  # service:environment lock
        self._lock = threading.RLock()
        self._governance_verifier: Optional[Callable[[str, str, str], bool]] = None
        self._reliability_gate: Optional[Callable[[str], bool]] = None

    def set_governance_verifier(self, verifier: Callable[[str, str, str], bool]) -> None:
        """Register governance policy verifier (service, version, environment)."""
        self._governance_verifier = verifier

    def set_reliability_gate(self, gate: Callable[[str], bool]) -> None:
        """Register reliability gate (environment)."""
        self._reliability_gate = gate

    def trigger_deployment(
        self,
        service_name: str,
        target_environment: str,
        target_version: str,
        release_id: Optional[str] = None,
        strategy: DeploymentStrategyType = DeploymentStrategyType.ROLLING,
        metadata: Optional[Dict[str, Any]] = None,
        health_checker: Optional[Callable[[], bool]] = None,
    ) -> DeploymentRecord:
        """Create and trigger a governed deployment."""
        lock_key = f"{service_name}:{target_environment}"

        with self._lock:
            if lock_key in self._active_deployments:
                raise ValueError(f"Active deployment already in progress for '{lock_key}'")

            # 1. Pre-flight Governance check
            if self._governance_verifier and not self._governance_verifier(service_name, target_version, target_environment):
                raise PermissionError(f"Deployment governance gate rejected deployment of '{service_name}' to '{target_environment}'")

            # 2. Pre-flight Reliability check (e.g. no active critical incidents)
            if self._reliability_gate and not self._reliability_gate(target_environment):
                raise RuntimeError(f"Reliability gate blocked deployment in '{target_environment}' due to active incidents or depleted error budget")

            # Determine previous version
            latest = self.history_tracker.get_latest_deployment(service_name, target_environment)
            prev_version = latest.target_version if latest else None

            record = DeploymentRecord(
                deployment_id=f"dep-{uuid.uuid4().hex[:8]}",
                release_id=release_id or f"rel-{uuid.uuid4().hex[:8]}",
                service_name=service_name,
                target_environment=target_environment,
                target_version=target_version,
                previous_version=prev_version,
                strategy=strategy,
                status=DeploymentStatus.PENDING,
                metadata=metadata or {},
            )
            self.history_tracker.record_deployment(record)
            self._active_deployments.add(lock_key)

        # Execute rollout asynchronously or synchronously
        try:
            self.orchestrator.execute_rollout(record, health_checker=health_checker)
        finally:
            with self._lock:
                self._active_deployments.discard(lock_key)

        return record

    def get_deployment(self, deployment_id: str) -> Optional[DeploymentRecord]:
        """Fetch deployment record."""
        return self.history_tracker.get_deployment(deployment_id)

    def list_deployments(self, service_name: Optional[str] = None, environment: Optional[str] = None) -> List[DeploymentRecord]:
        """Query deployment history."""
        return self.history_tracker.list_deployments(service_name=service_name, environment=environment)
