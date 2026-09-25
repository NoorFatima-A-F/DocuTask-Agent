"""
AOIS-HROP Phase 13.7 - Operational Runtime
Master runtime coordinator orchestrating supervisor, inspector, heartbeat, watchdog, and operational subsystems.
"""

from typing import Any, Dict, Optional
from app.runtime.operations.runtime.runtime_supervisor import RuntimeSupervisor
from app.runtime.operations.runtime.runtime_inspector import RuntimeInspector
from app.runtime.operations.runtime.runtime_heartbeat import RuntimeHeartbeat
from app.runtime.operations.runtime.runtime_watchdog import RuntimeWatchdog


class OperationalRuntime:
    """
    Master operational coordinator providing unified access to live SRE monitoring and supervision.
    """

    def __init__(self):
        self.supervisor = RuntimeSupervisor()
        self.inspector = RuntimeInspector()
        self.heartbeat = RuntimeHeartbeat()
        self.watchdog = RuntimeWatchdog()

    def get_runtime_overview(self) -> Dict[str, Any]:
        pulse = self.heartbeat.emit_pulse()
        inspection = self.inspector.inspect_live_runtime()
        supervision = self.supervisor.get_all_supervision_states()
        alerts = [
            {
                "id": a.alert_id,
                "type": a.alert_type,
                "severity": a.severity,
                "culprit": a.culprit_resource,
                "recovery": a.recommended_recovery,
                "duration_sec": a.stall_duration_sec,
            }
            for a in self.watchdog.get_active_alerts()
        ]

        return {
            "status": "OPERATIONAL_AUTONOMIC",
            "heartbeat": {
                "sequence": pulse.sequence_number,
                "liveness": pulse.liveness_status,
                "last_pulse": pulse.timestamp_utc,
                "is_fresh": self.heartbeat.is_heartbeat_fresh(),
            },
            "inspection": {
                "cpu_pct": inspection.cpu_utilization_pct,
                "memory_pct": inspection.memory_utilization_pct,
                "gpu_pct": inspection.gpu_utilization_pct,
                "queue_backlog": inspection.queue_backlog_count,
                "workers": inspection.active_worker_threads,
                "p95_ms": inspection.p95_latency_ms,
                "starvation_risk": inspection.starvation_risk_score,
            },
            "supervision_summary": {
                "all_healthy": self.supervisor.is_all_healthy(),
                "subsystems": supervision,
            },
            "active_alerts": alerts,
        }


_GLOBAL_RUNTIME: Optional[OperationalRuntime] = None


def get_operational_runtime() -> OperationalRuntime:
    global _GLOBAL_RUNTIME
    if _GLOBAL_RUNTIME is None:
        _GLOBAL_RUNTIME = OperationalRuntime()
    return _GLOBAL_RUNTIME
