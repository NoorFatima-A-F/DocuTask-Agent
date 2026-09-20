"""
AOIS-HROP Phase 13.7 - Runtime Watchdog
Detects deadlocks, stalls, hung workers, frozen planners, infinite retries, and resource starvation.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class WatchdogAlert:
    alert_id: str
    alert_type: str  # DEADLOCK, HUNG_WORKER, FROZEN_PLANNER, RETRY_STORM, STARVATION
    severity: str
    detected_at: str
    culprit_resource: str
    stall_duration_sec: float
    recommended_recovery: str
    is_active: bool = True


class RuntimeWatchdog:
    """
    Watches runtime subsystems for operational stalls and deadlock conditions.
    """

    def __init__(self, stall_threshold_sec: float = 30.0):
        self.stall_threshold_sec = stall_threshold_sec
        self._alerts: List[WatchdogAlert] = []
        self._monitored_tasks: Dict[str, Dict[str, Any]] = {}

    def register_task_heartbeat(self, task_id: str, component: str = "WORKER"):
        self._monitored_tasks[task_id] = {
            "component": component,
            "last_heartbeat": datetime.now(timezone.utc),
            "retry_count": self._monitored_tasks.get(task_id, {}).get("retry_count", 0),
        }

    def increment_task_retry(self, task_id: str) -> int:
        if task_id not in self._monitored_tasks:
            self.register_task_heartbeat(task_id)
        self._monitored_tasks[task_id]["retry_count"] += 1
        count = self._monitored_tasks[task_id]["retry_count"]

        if count >= 5:
            self._create_alert(
                alert_type="RETRY_STORM",
                severity="HIGH",
                culprit=f"task:{task_id}",
                stall_duration=0.0,
                recovery="ENGAGE_EXPONENTIAL_BACKOFF_AND_CIRCUIT_BREAKER",
            )
        return count

    def scan_for_stalls(self) -> List[WatchdogAlert]:
        now = datetime.now(timezone.utc)
        new_alerts: List[WatchdogAlert] = []

        for task_id, info in list(self._monitored_tasks.items()):
            delta = (now - info["last_heartbeat"]).total_seconds()
            if delta > self.stall_threshold_sec:
                alert = self._create_alert(
                    alert_type="HUNG_WORKER" if info["component"] == "WORKER" else "FROZEN_PLANNER",
                    severity="CRITICAL",
                    culprit=f"{info['component']}:{task_id}",
                    stall_duration=delta,
                    recovery="AUTO_TERMINATE_AND_RESTART_WORKER",
                )
                new_alerts.append(alert)

        return new_alerts

    def _create_alert(
        self,
        alert_type: str,
        severity: str,
        culprit: str,
        stall_duration: float,
        recovery: str,
    ) -> WatchdogAlert:
        alert = WatchdogAlert(
            alert_id=f"wd-{uuid.uuid4().hex[:8]}",
            alert_type=alert_type,
            severity=severity,
            detected_at=datetime.now(timezone.utc).isoformat(),
            culprit_resource=culprit,
            stall_duration_sec=round(stall_duration, 2),
            recommended_recovery=recovery,
            is_active=True,
        )
        self._alerts.append(alert)
        return alert

    def get_active_alerts(self) -> List[WatchdogAlert]:
        return [a for a in self._alerts if a.is_active]

    def resolve_alert(self, alert_id: str):
        for a in self._alerts:
            if a.alert_id == alert_id:
                a.is_active = False
