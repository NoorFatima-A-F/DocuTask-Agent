"""FastAPI Endpoints for Autonomous Planning Operating System.

Provides REST APIs for mission planning, strategy comparison, counterfactual what-if analysis,
mutable DAG visualization and mutation, resource scheduler monitoring, adaptive replanning, and planner self-evaluation.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.runtime.planning.planner_runtime import AutonomousPlanningRuntime, MissionPlanResult
from app.runtime.planning.mutable_dag import MutableExecutionDAG, DAGNode, DAGMutationType
from app.runtime.planning.strategy_ranker import StrategySelectionRecord, StrategyComparisonMatrix
from app.runtime.planning.counterfactual_engine import CounterfactualExplanation, CounterfactualQuery
from app.runtime.planning.scheduler import WorkerLease, QueuePriority
from app.runtime.planning.adaptive_replanner import ReplanningTrigger, ReplanningTriggerType, SubGraphReplanningResult
from app.runtime.planning.self_evaluator import PlanCalibrationMetric
from app.runtime.planning.planning_memory import PlanSignature

router = APIRouter()

# Global runtime instance
_planning_runtime = AutonomousPlanningRuntime()


class PlanMissionRequest(BaseModel):
    mission_id: str = Field(..., description="Unique ID for the mission")
    intent: str = Field(..., description="Natural language mission objective")
    user_constraints: Optional[Dict[str, Any]] = None
    signature: Optional[PlanSignature] = None


class DAGMutateRequest(BaseModel):
    mutation_type: DAGMutationType
    target_node_id: str
    split_count: Optional[int] = 2
    merged_node_ids: Optional[List[str]] = None
    merged_name: Optional[str] = "Consolidated Step"
    new_capability_id: Optional[str] = None
    new_provider: Optional[str] = None
    rationale: str = "Operator or automated optimizer request"


class CounterfactualQueryRequest(BaseModel):
    mission_id: str
    query_type: str = "WHAT_IF_WEIGHT_CHANGED"
    target_strategy_id: Optional[str] = None
    weight_overrides: Optional[Dict[str, float]] = None


class AdaptiveReplanRequest(BaseModel):
    mission_id: Optional[str] = None
    trigger_type: ReplanningTriggerType
    node_id: Optional[str] = None
    metric_value: Optional[float] = None
    threshold: Optional[float] = None
    rationale: str = ""


class EvaluateMissionRequest(BaseModel):
    mission_id: str
    actual_latency_ms: float
    actual_cost_usd: float
    actual_accuracy: float
    actual_failure: bool = False


class LeaseWorkerRequest(BaseModel):
    mission_id: str
    step_id: str
    capability_id: str
    duration_seconds: float = 60.0
    priority: QueuePriority = QueuePriority.HIGH
    required_gpu: bool = False


@router.post("/plan", response_model=MissionPlanResult, summary="Plan Mission Autonomously")
async def plan_mission(req: PlanMissionRequest) -> MissionPlanResult:
    """Runs complete autonomous planning pipeline: goal graph, constraints, strategies, simulation, ranking, DAG."""
    try:
        result = _planning_runtime.plan_mission(
            mission_id=req.mission_id,
            raw_intent=req.intent,
            user_constraints=req.user_constraints,
            signature=req.signature,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/plan/{mission_id}", response_model=MissionPlanResult, summary="Get Mission Plan")
async def get_plan(mission_id: str) -> MissionPlanResult:
    plan = _planning_runtime.get_plan(mission_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Plan for mission {mission_id} not found.")
    return plan


@router.get("/strategies/{mission_id}", response_model=StrategyComparisonMatrix, summary="Get Strategy Comparison Matrix")
async def get_strategy_matrix(mission_id: str) -> StrategyComparisonMatrix:
    plan = _planning_runtime.get_plan(mission_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Plan for mission {mission_id} not found.")
    return plan.selection_record.comparison_matrix


@router.post("/counterfactuals/query", response_model=CounterfactualExplanation, summary="Evaluate Counterfactual Hypothesis")
async def evaluate_counterfactual(req: CounterfactualQueryRequest) -> CounterfactualExplanation:
    plan = _planning_runtime.get_plan(req.mission_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Plan for mission {req.mission_id} not found.")

    if req.query_type == "WHAT_IF_WEIGHT_CHANGED" and req.weight_overrides:
        return _planning_runtime.counterfactual_engine.evaluate_what_if_weights(
            weight_overrides=req.weight_overrides,
            strategies=plan.candidate_strategies,
            cost_predictions=plan.cost_predictions,
            latency_predictions=plan.latency_predictions,
            risk_profiles=plan.risk_profiles,
        )
    elif req.query_type == "WHY_STRATEGY_REJECTED" and req.target_strategy_id:
        return _planning_runtime.counterfactual_engine.explain_rejection(
            rejected_strategy_id=req.target_strategy_id,
            selected_strategy_id=plan.selection_record.selected_strategy_id,
            strategies=plan.candidate_strategies,
            utility_scores={s.strategy_id: plan.selection_record.utility_breakdown for s in plan.candidate_strategies},
            cost_predictions=plan.cost_predictions,
            latency_predictions=plan.latency_predictions,
            risk_profiles=plan.risk_profiles,
        )
    else:
        return _planning_runtime.counterfactual_engine.explain_selection(
            selected_strategy_id=plan.selection_record.selected_strategy_id,
            strategies=plan.candidate_strategies,
            utility_scores={s.strategy_id: plan.selection_record.utility_breakdown for s in plan.candidate_strategies},
            cost_predictions=plan.cost_predictions,
            latency_predictions=plan.latency_predictions,
            risk_profiles=plan.risk_profiles,
        )


@router.get("/dag/{mission_id}", response_model=MutableExecutionDAG, summary="Get Active Mutable DAG")
async def get_dag(mission_id: str) -> MutableExecutionDAG:
    dag = _planning_runtime.get_dag(mission_id)
    if not dag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Active DAG for mission {mission_id} not found.")
    return dag


@router.post("/dag/{mission_id}/mutate", response_model=MutableExecutionDAG, summary="Mutate Active Execution DAG")
async def mutate_dag(mission_id: str, req: DAGMutateRequest) -> MutableExecutionDAG:
    dag = _planning_runtime.get_dag(mission_id)
    if not dag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Active DAG for mission {mission_id} not found.")

    try:
        if req.mutation_type == DAGMutationType.NODE_SPLIT:
            _planning_runtime.mutate_dag_split(mission_id, req.target_node_id, req.split_count or 2, req.rationale)
        elif req.mutation_type == DAGMutationType.NODE_REPLACE:
            if not req.new_capability_id or not req.new_provider:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="new_capability_id and new_provider required for replace.")
            _planning_runtime.mutate_dag_replace(mission_id, req.target_node_id, req.new_capability_id, req.new_provider, req.rationale)
        elif req.mutation_type == DAGMutationType.NODE_CLONE:
            dag.clone_node(req.target_node_id, req.rationale)
        elif req.mutation_type == DAGMutationType.NODE_MERGE and req.merged_node_ids:
            dag.merge_nodes(req.merged_node_ids, req.merged_name or "Merged Node", req.rationale)
        return dag
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/replan/{mission_id}", response_model=SubGraphReplanningResult, summary="Trigger Adaptive Sub-Graph Replanning")
async def trigger_replan(mission_id: str, req: AdaptiveReplanRequest) -> SubGraphReplanningResult:
    try:
        trigger = ReplanningTrigger(
            trigger_type=req.trigger_type,
            node_id=req.node_id,
            metric_value=req.metric_value,
            threshold=req.threshold,
            rationale=req.rationale,
        )
        return _planning_runtime.trigger_adaptive_replanning(mission_id, trigger)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/scheduler/status", summary="Get Resource Scheduler & Cluster Status")
async def get_scheduler_status() -> Dict[str, Any]:
    return _planning_runtime.scheduler.get_cluster_status()


@router.post("/scheduler/lease", response_model=Optional[WorkerLease], summary="Acquire Worker Lease")
async def acquire_lease(req: LeaseWorkerRequest) -> Optional[WorkerLease]:
    lease = _planning_runtime.scheduler.acquire_lease(
        mission_id=req.mission_id,
        step_id=req.step_id,
        capability_id=req.capability_id,
        duration_seconds=req.duration_seconds,
        priority=req.priority,
        required_gpu=req.required_gpu,
    )
    if not lease:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="No worker capacity available for lease.")
    return lease


@router.post("/scheduler/release/{lease_id}", summary="Release Worker Lease")
async def release_lease(lease_id: str) -> Dict[str, bool]:
    success = _planning_runtime.scheduler.release_lease(lease_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Lease {lease_id} not found.")
    return {"released": True}


@router.post("/evaluate/{mission_id}", response_model=PlanCalibrationMetric, summary="Evaluate Mission Outcome & Self-Calibrate")
async def evaluate_mission(mission_id: str, req: EvaluateMissionRequest) -> PlanCalibrationMetric:
    try:
        return _planning_runtime.evaluate_mission_outcome(
            mission_id=mission_id,
            actual_latency_ms=req.actual_latency_ms,
            actual_cost_usd=req.actual_cost_usd,
            actual_accuracy=req.actual_accuracy,
            actual_failure=req.actual_failure,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/capabilities", summary="List Registered Capabilities")
async def list_capabilities() -> List[Dict[str, Any]]:
    return [c.model_dump() for c in _planning_runtime.capability_discovery.list_all()]
