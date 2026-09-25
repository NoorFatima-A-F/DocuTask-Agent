"""
Planner Reconstructor for Phase 13.4.
Rebuilds 14-state planner lifecycle, goal decompositions, DAG structure, and mutation histories from events.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ReconstructedPlannerState(BaseModel):
    lifecycle_state: str = "IDLE"
    active_goal: Optional[str] = None
    tasks: List[Dict[str, Any]] = Field(default_factory=list)
    dag_nodes: Dict[str, Any] = Field(default_factory=dict)
    dag_edges: List[Dict[str, str]] = Field(default_factory=list)
    mutations: List[Dict[str, Any]] = Field(default_factory=list)
    decisions: List[Dict[str, Any]] = Field(default_factory=list)
    critical_path: List[str] = Field(default_factory=list)
    estimated_duration_ms: float = 0.0


class PlannerReconstructor:
    """
    Reconstructs exact planner lifecycle state from event streams.
    """

    @classmethod
    def reconstruct_from_events(
        cls,
        events: List[Dict[str, Any]],
        target_cursor: Optional[int] = None,
    ) -> ReconstructedPlannerState:
        state = ReconstructedPlannerState()
        sliced = events[: (target_cursor + 1)] if target_cursor is not None else events

        for ev in sliced:
            evt_type = ev.get("event_type") or ev.get("type", "")
            payload = ev.get("payload", {})

            if "planner.lifecycle" in evt_type or "planner.state" in evt_type:
                state.lifecycle_state = payload.get("state", state.lifecycle_state)
            elif "planner.goal" in evt_type:
                state.active_goal = payload.get("goal", state.active_goal)
            elif "planner.task_decomposed" in evt_type or "task.created" in evt_type:
                tasks = payload.get("tasks", [])
                if isinstance(tasks, list):
                    state.tasks.extend(tasks)
                elif "task_id" in payload:
                    state.tasks.append(payload)
            elif "dag.node_added" in evt_type or "dag.node" in evt_type:
                node_id = payload.get("node_id") or payload.get("id")
                if node_id:
                    state.dag_nodes[node_id] = payload
            elif "dag.edge_added" in evt_type or "dag.edge" in evt_type:
                if "from_node" in payload and "to_node" in payload:
                    state.dag_edges.append({"from": payload["from_node"], "to": payload["to_node"]})
            elif "dag.mutated" in evt_type or "planner.mutation" in evt_type:
                state.mutations.append(payload)
            elif "planner.decision" in evt_type:
                state.decisions.append(payload)
            elif "planner.critical_path" in evt_type:
                state.critical_path = payload.get("critical_path", state.critical_path)

        return state
