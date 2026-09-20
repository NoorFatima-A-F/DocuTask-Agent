"""
REST API Endpoints for Autonomous Planner Visualization, Dynamic DAG Execution & Live Replanning (APDLE & Phase 13.2 APEV-DAG).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.runtime.planning.graph.graph_builder import ExecutionGraphBuilder
from app.runtime.planning.graph.graph_serializer import GraphSerializer
from app.runtime.planning.replanning.replanner import AdaptiveReplanner
from app.runtime.planning.scheduler.critical_path import CriticalPathEngine as LegacyCriticalPathEngine
from app.runtime.planning.scheduler.scheduler import DAGScheduler
from app.runtime.planning.simulation.planner_simulator import PlannerSimulator
from app.runtime.planning.visualization.graph_snapshot import VisualGraphSnapshot

from app.runtime.planner_visualization.api.planner_api_service import PlannerAPIService

router = APIRouter()

# Global in-memory mission DAG store
_active_mission_dags: Dict[str, Any] = {}
_replanner_instances: Dict[str, AdaptiveReplanner] = {}


def _get_or_create_dag(mission_id: str):
    if mission_id not in _active_mission_dags:
        dag = ExecutionGraphBuilder.build_financial_invoice_audit_dag(mission_id=mission_id)
        _active_mission_dags[mission_id] = dag
        _replanner_instances[mission_id] = AdaptiveReplanner()
    return _active_mission_dags[mission_id], _replanner_instances[mission_id]


class ReplanRequest(BaseModel):
    failed_node_id: Optional[str] = None
    error_reason: str = "Validation invariant breached"
    confidence_drop: Optional[float] = None


# ==========================================
# Phase 13.2 APEV-DAG Endpoints
# ==========================================

@router.get('/state')
async def get_planner_state(mission_id: str = Query("mission-001")):
    """
    Returns current 14-state planner lifecycle status.
    """
    return PlannerAPIService.get_instance(mission_id).get_state()


@router.get('/lifecycle')
async def get_planner_lifecycle(mission_id: str = Query("mission-001")):
    """
    Returns full state transition history of planner lifecycle.
    """
    return PlannerAPIService.get_instance(mission_id).get_lifecycle_timeline()


@router.get('/goals')
async def get_planner_goals(mission_id: str = Query("mission-001")):
    """
    Returns structured goal decomposition, sub-objectives, and constraints.
    """
    return PlannerAPIService.get_instance(mission_id).get_goal_analysis()


@router.get('/tasks')
async def get_planner_tasks(mission_id: str = Query("mission-001")):
    """
    Returns multi-stage generated execution tasks.
    """
    return PlannerAPIService.get_instance(mission_id).get_task_decomposition()


@router.get('/dag')
async def get_planner_dag_snapshot(mission_id: str = Query("mission-001")):
    """
    Returns live execution DAG snapshot with nodes, edges, and critical path.
    """
    return PlannerAPIService.get_instance(mission_id).get_dag_snapshot()


@router.get('/dag/history')
async def get_planner_dag_history(mission_id: str = Query("mission-001")):
    """
    Returns history of runtime DAG mutations.
    """
    return PlannerAPIService.get_instance(mission_id).get_replanning_history()


@router.get('/critical-path')
async def get_planner_cpm_critical_path(mission_id: str = Query("mission-001")):
    """
    Returns CPM (Critical Path Method) analysis and top bottlenecks.
    """
    return PlannerAPIService.get_instance(mission_id).get_critical_path()


@router.get('/queues')
async def get_planner_queues(mission_id: str = Query("mission-001")):
    """
    Returns task distribution across the 7 execution queue states.
    """
    return PlannerAPIService.get_instance(mission_id).get_queues()


@router.get('/scheduler')
async def get_planner_scheduler_state(mission_id: str = Query("mission-001")):
    """
    Returns worker pool status, load balancing, and concurrency limits.
    """
    return PlannerAPIService.get_instance(mission_id).get_scheduler_status()


@router.get('/workers')
async def get_planner_workers(mission_id: str = Query("mission-001")):
    """
    Returns worker assignments with capability match scores and rationale.
    """
    return PlannerAPIService.get_instance(mission_id).get_workers()


@router.get('/replanning')
async def get_planner_replanning_state(mission_id: str = Query("mission-001")):
    """
    Returns replanning history and dynamic recovery branches.
    """
    return PlannerAPIService.get_instance(mission_id).get_replanning_history()


@router.get('/metrics')
async def get_planner_metrics(mission_id: str = Query("mission-001")):
    """
    Returns runtime planner performance metrics and parallelism factors.
    """
    return PlannerAPIService.get_instance(mission_id).get_metrics()


@router.get('/decisions')
async def get_planner_decisions(mission_id: str = Query("mission-001")):
    """
    Returns inspectable planner decision cards with truth hashes and alternatives.
    """
    return PlannerAPIService.get_instance(mission_id).get_decisions()


@router.get('/dependencies')
async def get_planner_dependencies(mission_id: str = Query("mission-001")):
    """
    Returns DAG dependency topology.
    """
    snapshot = PlannerAPIService.get_instance(mission_id).get_dag_snapshot()
    return {
        "mission_id": mission_id,
        "nodes": snapshot.get("nodes", []),
        "edges": snapshot.get("edges", []),
    }


@router.get('/timeline')
async def get_planner_timeline(mission_id: str = Query("mission-001")):
    """
    Returns event-sourced chronological planner timeline.
    """
    return PlannerAPIService.get_instance(mission_id).get_timeline()


# ==========================================
# Legacy APDLE Endpoints (Preserved for compatibility)
# ==========================================

@router.get('/graph/{mission_id}')
async def get_legacy_planner_graph(mission_id: str):
    dag, _ = _get_or_create_dag(mission_id)
    return VisualGraphSnapshot.generate_snapshot(dag)


@router.get('/critical-path/{mission_id}')
async def get_legacy_planner_critical_path(mission_id: str):
    dag, _ = _get_or_create_dag(mission_id)
    return LegacyCriticalPathEngine.analyze(dag)


@router.get('/schedule/{mission_id}')
async def get_legacy_planner_schedule(mission_id: str):
    dag, _ = _get_or_create_dag(mission_id)
    scheduler = DAGScheduler()
    status_info = scheduler.get_status(dag)
    wavefronts = dag.compute_concurrency_wavefronts()
    
    return {
        **status_info,
        "wavefronts": [[n.node_id for n in w] for w in wavefronts],
        "workers": [w.model_dump() for w in scheduler.allocator.workers.values()],
    }


@router.get('/simulation/{mission_id}')
async def get_legacy_planner_simulation(mission_id: str, num_trials: int = Query(100, ge=10, le=1000)):
    dag, _ = _get_or_create_dag(mission_id)
    sim_result = PlannerSimulator.simulate_dag(dag, num_trials=num_trials)
    return sim_result.model_dump()


@router.post('/replan/{mission_id}', status_code=status.HTTP_200_OK)
async def trigger_legacy_live_replan(mission_id: str, body: ReplanRequest):
    dag, replanner = _get_or_create_dag(mission_id)

    if body.confidence_drop is not None:
        target_node = body.failed_node_id or "node_ocr_01"
        rec = replanner.handle_low_confidence(dag, target_node, body.confidence_drop)
    else:
        target_node = body.failed_node_id or "node_extract_items"
        rec = replanner.handle_node_failure(dag, target_node, body.error_reason)

    return {
        "status": "REPLANNED",
        "mutation": rec.model_dump(),
        "updated_dag": VisualGraphSnapshot.generate_snapshot(dag),
    }


@router.get('/events/{mission_id}')
async def get_legacy_planner_events(mission_id: str):
    from app.runtime.observability.runtime_monitor import get_runtime_monitor
    monitor = get_runtime_monitor()
    events = monitor.event_store.query(mission_id=mission_id, category="PLANNER")
    return [e.model_dump() for e in events]


@router.get('/mutations/{mission_id}')
async def get_legacy_planner_mutations(mission_id: str):
    dag, replanner = _get_or_create_dag(mission_id)
    return [m.model_dump() for m in replanner.mutation_history]
