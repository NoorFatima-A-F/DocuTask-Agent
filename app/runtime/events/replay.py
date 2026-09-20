# Event Replay & Engineering State Reconstruction Engine
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from app.runtime.events.base import RuntimeEvent
from app.runtime.events.persistence import EventStore


@dataclass
class ReplayStateSnapshot:
    mission_id: str
    step_sequence: int
    total_steps: int
    timestamp_iso: str
    active_agent_id: Optional[str] = None
    agent_states: Dict[str, str] = field(default_factory=dict)
    completed_tasks: List[str] = field(default_factory=list)
    running_tasks: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    evidence_count: int = 0
    memory_count: int = 0
    decision_summary: str = ""
    latest_event: Optional[Dict[str, Any]] = None
    total_tokens_consumed: int = 0
    estimated_cost_usd: float = 0.0
    cpu_percent_approx: float = 0.0
    memory_mb_approx: float = 0.0


@dataclass
class ReplayStepDiff:
    mission_id: str
    step_a: int
    step_b: int
    snapshot_a: ReplayStateSnapshot
    snapshot_b: ReplayStateSnapshot
    delta_completed_tasks: List[str]
    delta_running_tasks: List[str]
    delta_agent_states: Dict[str, Tuple[str, str]]
    delta_confidence: float
    delta_evidence_count: int
    delta_memory_count: int
    delta_tokens: int
    delta_cost_usd: float
    intermediate_events: List[Dict[str, Any]]
    total_duration_between_steps_ms: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "step_a": self.step_a,
            "step_b": self.step_b,
            "snapshot_a": asdict(self.snapshot_a),
            "snapshot_b": asdict(self.snapshot_b),
            "delta_completed_tasks": self.delta_completed_tasks,
            "delta_running_tasks": self.delta_running_tasks,
            "delta_agent_states": self.delta_agent_states,
            "delta_confidence": self.delta_confidence,
            "delta_evidence_count": self.delta_evidence_count,
            "delta_memory_count": self.delta_memory_count,
            "delta_tokens": self.delta_tokens,
            "delta_cost_usd": self.delta_cost_usd,
            "intermediate_events": self.intermediate_events,
            "total_duration_between_steps_ms": self.total_duration_between_steps_ms,
        }


class EventReplayEngine:
    """
    Deterministic state reconstructor and engineering comparison debugger.
    """

    def __init__(self, store: EventStore):
        self.store = store

    async def reconstruct_at_step(self, mission_id: str, target_step: int) -> ReplayStateSnapshot:
        events = await self.store.query(mission_id=mission_id, limit=10000)
        total_steps = len(events)
        agent_states: Dict[str, str] = {}
        completed_tasks: List[str] = []
        running_tasks: List[str] = []
        confidence = 0.0
        evidence_count = 0
        memory_count = 0
        total_tokens = 0
        cost_usd = 0.0
        decision_summary = "Mission Initialized"
        last_ev: Optional[RuntimeEvent] = None
        active_agent: Optional[str] = None

        for ev in events:
            if ev.sequence_number > target_step:
                break
            last_ev = ev
            if ev.agent_id:
                active_agent = ev.agent_id

            tokens = int(ev.payload.get("tokens_processed", 0))
            total_tokens += tokens
            cost_usd += tokens * 0.000002  # $2 per 1M tokens

            if ev.event_type == "WorkerStarted":
                task_id = ev.payload.get("task_id", ev.worker_id or "task")
                running_tasks.append(task_id)
                if ev.agent_id:
                    agent_states[ev.agent_id] = "RUNNING"
            elif ev.event_type == "WorkerCompleted":
                task_id = ev.payload.get("task_id", ev.worker_id or "task")
                if task_id in running_tasks:
                    running_tasks.remove(task_id)
                if task_id not in completed_tasks:
                    completed_tasks.append(task_id)
                if ev.agent_id:
                    agent_states[ev.agent_id] = "IDLE"
            elif ev.event_type == "WorkerFailed":
                if ev.agent_id:
                    agent_states[ev.agent_id] = "ERROR"
            elif ev.event_type in ("MemoryRetrieved", "MemoryCreated"):
                memory_count += 1
            elif ev.event_type in ("ValidationPassed", "ValidationStarted"):
                evidence_count += 1
                if "confidence" in ev.payload:
                    confidence = float(ev.payload["confidence"])
            elif ev.event_type == "TelemetryUpdated":
                if "confidence_score" in ev.payload:
                    confidence = float(ev.payload["confidence_score"])
            elif ev.event_type == "MissionCreated":
                decision_summary = f"Goal: {ev.payload.get('goal', 'Process documents')}"
            elif ev.event_type == "PlannerCompleted":
                decision_summary = f"DAG plan generated with {len(ev.payload.get('tasks', []))} tasks"
            elif ev.event_type == "InvariantApplied":
                decision_summary = f"Invariant applied: {ev.payload.get('rule_name', 'Rule')}"

        ts_iso = last_ev.timestamp.isoformat() if last_ev else datetime.now(timezone.utc).isoformat()
        return ReplayStateSnapshot(
            mission_id=mission_id,
            step_sequence=target_step,
            total_steps=total_steps,
            timestamp_iso=ts_iso,
            active_agent_id=active_agent,
            agent_states=agent_states,
            completed_tasks=completed_tasks,
            running_tasks=running_tasks,
            confidence_score=confidence,
            evidence_count=evidence_count,
            memory_count=memory_count,
            decision_summary=decision_summary,
            latest_event=last_ev.to_dict() if last_ev else None,
            total_tokens_consumed=total_tokens,
            estimated_cost_usd=round(cost_usd, 4),
            cpu_percent_approx=round(min(98.0, 2.0 + len(running_tasks) * 14.5), 1),
            memory_mb_approx=round(64.0 + len(completed_tasks) * 8.2 + total_tokens * 0.001, 1),
        )

    async def compare_replay_steps(
        self,
        mission_id: str,
        step_a: int,
        step_b: int,
    ) -> ReplayStepDiff:
        """
        Computes delta between state reconstructed at step_a and step_b.
        """
        if step_a > step_b:
            step_a, step_b = step_b, step_a

        snap_a = await self.reconstruct_at_step(mission_id, step_a)
        snap_b = await self.reconstruct_at_step(mission_id, step_b)

        # Query intermediate events
        all_events = await self.store.query(mission_id=mission_id, limit=10000)
        intermediates = [
            e for e in all_events
            if step_a < e.sequence_number <= step_b
        ]

        delta_completed = [t for t in snap_b.completed_tasks if t not in snap_a.completed_tasks]
        delta_running = [t for t in snap_b.running_tasks if t not in snap_a.running_tasks]

        delta_agent_states: Dict[str, Tuple[str, str]] = {}
        all_agents = set(snap_a.agent_states.keys()).union(set(snap_b.agent_states.keys()))
        for ag in all_agents:
            st_a = snap_a.agent_states.get(ag, "IDLE")
            st_b = snap_b.agent_states.get(ag, "IDLE")
            if st_a != st_b:
                delta_agent_states[ag] = (st_a, st_b)

        duration_ms = 0.0
        if intermediates:
            t_start = intermediates[0].timestamp
            t_end = intermediates[-1].timestamp
            duration_ms = max(0.0, (t_end - t_start).total_seconds() * 1000.0)

        return ReplayStepDiff(
            mission_id=mission_id,
            step_a=step_a,
            step_b=step_b,
            snapshot_a=snap_a,
            snapshot_b=snap_b,
            delta_completed_tasks=delta_completed,
            delta_running_tasks=delta_running,
            delta_agent_states=delta_agent_states,
            delta_confidence=round(snap_b.confidence_score - snap_a.confidence_score, 4),
            delta_evidence_count=snap_b.evidence_count - snap_a.evidence_count,
            delta_memory_count=snap_b.memory_count - snap_a.memory_count,
            delta_tokens=snap_b.total_tokens_consumed - snap_a.total_tokens_consumed,
            delta_cost_usd=round(snap_b.estimated_cost_usd - snap_a.estimated_cost_usd, 4),
            intermediate_events=[e.to_dict() for e in intermediates],
            total_duration_between_steps_ms=round(duration_ms, 2),
        )
