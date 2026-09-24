"""
REST API Endpoints for Phase 13.11 (ASC-GEEIP) Strategic Cognition & Executive Platform.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.runtime.strategy.runtime.executive_runtime import ExecutiveRuntime
from app.runtime.strategy.events.strategy_events import (
    GoalPriority,
    GoalStatus,
    StrategicHorizon,
    MissionValue,
)

router = APIRouter()


class CreateGoalRequest(BaseModel):
    title: str = Field(..., description="Goal title")
    description: str = Field("", description="Goal description")
    parent_goal_id: Optional[str] = Field(None, description="Optional parent goal ID for hierarchy")
    priority: GoalPriority = Field(GoalPriority.HIGH, description="Initial goal priority")
    horizon: StrategicHorizon = Field(StrategicHorizon.DAYS_90, description="Strategic horizon")
    value_type: MissionValue = Field(MissionValue.EFFICIENCY_GAIN, description="Value classification")
    estimated_cost_usd: float = Field(500.0, description="Estimated budget requirement in USD")
    expected_latency_reduction_pct: float = Field(10.0, description="Projected latency reduction percentage")
    tags: List[str] = Field(default_factory=list, description="Context tags")


class DecomposeGoalRequest(BaseModel):
    goal_id: str = Field(..., description="Parent goal ID to decompose")
    subtasks: List[Dict[str, Any]] = Field(..., description="List of decomposed subtask definitions")


class ArchiveGoalRequest(BaseModel):
    goal_id: str = Field(..., description="Goal ID to archive")
    reason: str = Field("Retired via strategic mandate", description="Archive reason")


class SimulateScenarioRequest(BaseModel):
    name: str = Field("Quarterly Strategic Scenario", description="Scenario name")
    horizon: StrategicHorizon = Field(StrategicHorizon.DAYS_90, description="Simulation horizon")
    budget_delta_usd: float = Field(0.0, description="Budget change delta in USD")
    worker_scale_delta: int = Field(4, description="Worker scale delta")
    cache_hit_rate_pct: float = Field(80.0, description="Target cache hit rate assumption")
    traffic_growth_pct: float = Field(100.0, description="Projected traffic growth percentage")


class GenerateRoadmapRequest(BaseModel):
    horizon: StrategicHorizon = Field(StrategicHorizon.DAYS_90, description="Roadmap horizon")
    title: str = Field("Strategic Execution Plan", description="Roadmap title")
    theme: str = Field("Scalability & Governance", description="Strategic theme")
    milestones: List[Dict[str, Any]] = Field(..., description="List of milestone specifications")
    estimated_cost_usd: float = Field(10000.0, description="Estimated cost")
    projected_roi: float = Field(3.0, description="Projected ROI multiplier")


class NegotiateResourcesRequest(BaseModel):
    resource_type: str = Field("GPU_VRAM_GB", description="Resource type to negotiate")
    total_capacity: float = Field(48.0, description="Total resource capacity pool")
    proposals: List[Dict[str, Any]] = Field(..., description="List of swarm proposals and bids")


class ApproveDecisionRequest(BaseModel):
    decision_id: str = Field(..., description="Executive decision ID to approve")
    approver_key: str = Field("cso_oracle_node", description="Approver cryptographic key identifier")


class RankCandidatesRequest(BaseModel):
    decision_context: str = Field(..., description="Decision context description")
    candidates: List[Dict[str, Any]] = Field(..., description="Candidates to evaluate")
    criteria_weights: Optional[Dict[str, float]] = Field(None, description="Criteria weights")


@router.get("/overview")
async def get_strategy_overview() -> Dict[str, Any]:
    runtime = ExecutiveRuntime.get_instance()
    return runtime.get_overview()


@router.get("/goals")
async def get_goals(status: Optional[GoalStatus] = None) -> List[Dict[str, Any]]:
    runtime = ExecutiveRuntime.get_instance()
    return runtime.goals.list_goals(status=status)


@router.get("/portfolio")
async def get_portfolio() -> Dict[str, Any]:
    runtime = ExecutiveRuntime.get_instance()
    return runtime.portfolio.get_portfolio()


@router.get("/roadmaps")
async def get_roadmaps() -> List[Dict[str, Any]]:
    runtime = ExecutiveRuntime.get_instance()
    return runtime.roadmaps.list_roadmaps()


@router.get("/executive")
async def get_executive_summary() -> Dict[str, Any]:
    runtime = ExecutiveRuntime.get_instance()
    return {
        "decisions": runtime.executive.list_decisions(),
        "recommendations": runtime.executive.list_recommendations(),
    }


@router.get("/organization")
async def get_organization_memory(
    category: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
) -> List[Dict[str, Any]]:
    runtime = ExecutiveRuntime.get_instance()
    return runtime.memory.query_knowledge(category=category, tag=tag, query_text=q)


@router.get("/negotiations")
async def get_negotiations() -> List[Dict[str, Any]]:
    runtime = ExecutiveRuntime.get_instance()
    return runtime.negotiation.list_sessions()


@router.get("/simulations")
async def get_simulations() -> List[Dict[str, Any]]:
    runtime = ExecutiveRuntime.get_instance()
    return runtime.simulation.list_simulations()


@router.get("/decisions")
async def get_decisions() -> List[Dict[str, Any]]:
    runtime = ExecutiveRuntime.get_instance()
    return runtime.decision.list_rankings()


@router.post("/create-goal")
async def create_goal(req: CreateGoalRequest) -> Dict[str, Any]:
    runtime = ExecutiveRuntime.get_instance()
    goal = runtime.goals.create_goal(
        title=req.title,
        description=req.description,
        parent_goal_id=req.parent_goal_id,
        priority=req.priority,
        horizon=req.horizon,
        value_type=req.value_type,
        estimated_cost_usd=req.estimated_cost_usd,
        expected_latency_reduction_pct=req.expected_latency_reduction_pct,
        tags=req.tags,
    )
    return goal.to_dict()


@router.post("/decompose-goal")
async def decompose_goal(req: DecomposeGoalRequest) -> List[Dict[str, Any]]:
    runtime = ExecutiveRuntime.get_instance()
    try:
        subgoals = runtime.goals.decompose_goal(req.goal_id, req.subtasks)
        return [s.to_dict() for s in subgoals]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/evolve-goals")
async def evolve_goals() -> Dict[str, Any]:
    runtime = ExecutiveRuntime.get_instance()
    return runtime.goals.evolve_generation()


@router.post("/prioritize")
async def reprioritize_goals() -> List[Dict[str, Any]]:
    runtime = ExecutiveRuntime.get_instance()
    reprioritized = runtime.goals.reprioritize_goals()
    return [g.to_dict() for g in reprioritized]


@router.post("/archive-goal")
async def archive_goal(req: ArchiveGoalRequest) -> Dict[str, Any]:
    runtime = ExecutiveRuntime.get_instance()
    try:
        goal = runtime.goals.archive_goal(req.goal_id, reason=req.reason)
        return goal.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/simulate")
async def simulate_scenario(req: SimulateScenarioRequest) -> Dict[str, Any]:
    runtime = ExecutiveRuntime.get_instance()
    sim = runtime.simulation.run_simulation(
        name=req.name,
        horizon=req.horizon,
        budget_delta_usd=req.budget_delta_usd,
        worker_scale_delta=req.worker_scale_delta,
        cache_hit_rate_pct=req.cache_hit_rate_pct,
        traffic_growth_pct=req.traffic_growth_pct,
    )
    return sim.to_dict()


@router.post("/generate-roadmap")
async def generate_roadmap(req: GenerateRoadmapRequest) -> Dict[str, Any]:
    runtime = ExecutiveRuntime.get_instance()
    roadmap = runtime.roadmaps.generate_roadmap(
        horizon=req.horizon,
        title=req.title,
        theme=req.theme,
        milestones_spec=req.milestones,
        estimated_cost_usd=req.estimated_cost_usd,
        projected_roi=req.projected_roi,
    )
    return roadmap.to_dict()


@router.post("/negotiate")
async def negotiate_resources(req: NegotiateResourcesRequest) -> Dict[str, Any]:
    runtime = ExecutiveRuntime.get_instance()
    session = runtime.negotiation.negotiate_resources(
        resource_type=req.resource_type,
        total_capacity=req.total_capacity,
        proposals_data=req.proposals,
    )
    return session.to_dict()


@router.post("/approve")
async def approve_decision(req: ApproveDecisionRequest) -> Dict[str, Any]:
    runtime = ExecutiveRuntime.get_instance()
    try:
        dec = runtime.executive.approve_decision(req.decision_id, approver_key=req.approver_key)
        return dec.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/rank-candidates")
async def rank_candidates(req: RankCandidatesRequest) -> Dict[str, Any]:
    runtime = ExecutiveRuntime.get_instance()
    ranking = runtime.decision.rank_candidates(
        decision_context=req.decision_context,
        candidates_data=req.candidates,
        criteria_weights=req.criteria_weights,
    )
    return ranking.to_dict()


@router.post("/execute-cycle")
async def execute_strategic_cycle() -> Dict[str, Any]:
    runtime = ExecutiveRuntime.get_instance()
    return runtime.execute_strategic_cycle()
