# Agent Status Engine
from __future__ import annotations
from datetime import datetime, timezone
from app.runtime.telemetry.store import RuntimeTelemetryStore

class AgentStatusEngine:
    def __init__(self, store: RuntimeTelemetryStore):
        self.store = store

    def get_agent_status_snapshot(self):
        now = datetime.now(timezone.utc)
        snapshots = []
        for agent in self.store.agents.values():
            elapsed_sec = (now - agent.last_active_utc).total_seconds()
            is_active = elapsed_sec < 45.0
            heartbeat_rate_bpm = max(60, int(100 - min(elapsed_sec, 40))) if is_active else 0
            snapshots.append({
                'agent_id': agent.agent_id,
                'role_name': agent.role_name,
                'state': agent.state,
                'is_alive': is_active,
                'heartbeat_bpm': heartbeat_rate_bpm,
                'last_active_seconds_ago': round(elapsed_sec, 1),
                'last_event_type': agent.last_event_type,
                'current_task_id': agent.current_task_id,
                'completed_tasks': agent.completed_task_count,
                'failed_tasks': agent.failed_task_count,
            })
        return snapshots
