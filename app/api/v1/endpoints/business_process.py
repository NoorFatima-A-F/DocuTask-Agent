"""
Phase 13.19: REST API Endpoints for Enterprise Process Intelligence & Autonomous Business Orchestration.
Mounted at /api/v1/business
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.runtime.business.models.schemas import (
    BusinessExecutiveOverview,
    BusinessProcess,
    BusinessGoal,
    OrganizationGraph,
    HumanApprovalTask,
    ApprovalStatus,
    DiscoveredProcess,
    ProcessOptimizationRecommendation,
    ProcessSimulationConfig,
    SimulationResult,
    KPIDefinition,
    DigitalTwinOrgState,
)
from app.runtime.business.runtime.business_orchestrator import BusinessOrchestrator

router = APIRouter()
orchestrator = BusinessOrchestrator.get_instance()


@router.get("/overview", response_model=BusinessExecutiveOverview)
async def get_executive_overview():
    """Returns top-level enterprise business health and automation ROI metrics."""
    return orchestrator.get_executive_overview()


@router.get("/processes", response_model=List[BusinessProcess])
async def list_processes():
    """Lists all registered business process workflows."""
    return orchestrator.process_engine.list_processes()


@router.post("/processes", response_model=BusinessProcess)
async def create_process(process: BusinessProcess):
    """Deploys a new business process graph."""
    return orchestrator.process_engine.register_process(process)


@router.post("/processes/{process_id}/execute")
async def execute_process(process_id: str):
    """Triggers execution of a business process until completion or human approval."""
    try:
        return orchestrator.process_engine.run_process_until_pause_or_completion(process_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/goals", response_model=List[BusinessGoal])
async def list_goals(department: Optional[str] = None):
    """Lists enterprise OKRs and business goals."""
    return orchestrator.goal_manager.list_goals(department=department)


@router.post("/goals", response_model=BusinessGoal)
async def create_goal(goal: BusinessGoal):
    """Creates a new business goal with key results."""
    return orchestrator.goal_manager.create_goal(goal)


@router.get("/organization", response_model=OrganizationGraph)
async def get_organization_graph():
    """Queries the enterprise organizational knowledge graph."""
    return orchestrator.org_graph.get_organization_graph()


@router.get("/approvals", response_model=List[HumanApprovalTask])
async def list_approvals(status: Optional[ApprovalStatus] = None):
    """Lists human-in-the-loop approval tasks."""
    return orchestrator.collaboration.list_tasks(status=status)


@router.post("/approvals/{task_id}/decide", response_model=HumanApprovalTask)
async def decide_approval(
    task_id: str,
    decision: ApprovalStatus = Query(..., description="APPROVED or REJECTED"),
    rationale: str = Query("Standard verification passed", description="Decision rationale"),
    decided_by: str = Query("role_finance_director", description="Reviewer role"),
):
    """Decides a pending human approval task and resumes workflow."""
    try:
        task = orchestrator.collaboration.decide_task(
            task_id=task_id,
            decision=decision,
            rationale=rationale,
            decided_by=decided_by,
        )
        # Resume process in process engine
        orchestrator.process_engine.resume_process_after_approval(
            process_id=task.process_id,
            step_id=task.step_id,
            approved=(decision == ApprovalStatus.APPROVED),
        )
        return task
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/discovery", response_model=List[DiscoveredProcess])
async def get_discovered_processes():
    """Returns mined process graphs and discovered bottlenecks."""
    return orchestrator.discovery_engine.list_discovered_processes()


@router.post("/processes/optimize", response_model=List[ProcessOptimizationRecommendation])
async def optimize_process(process_id: Optional[str] = None):
    """Generates process redesign recommendations to eliminate friction."""
    return orchestrator.optimizer.list_recommendations(process_id=process_id)


@router.post("/simulations", response_model=SimulationResult)
async def run_simulation(config: ProcessSimulationConfig):
    """Runs a Monte Carlo discrete-event process simulation."""
    return orchestrator.simulation.run_simulation(config)


@router.get("/kpis", response_model=List[KPIDefinition])
async def get_kpis():
    """Returns enterprise KPI scorecard and financial impact metrics."""
    return orchestrator.kpi_engine.get_kpis()


@router.get("/digital-twin", response_model=DigitalTwinOrgState)
async def get_digital_twin():
    """Returns real-time Digital Twin of the Organization status."""
    return orchestrator.digital_twin.get_digital_twin_state()


@router.post("/orchestration/cycle")
async def trigger_business_orchestration_cycle():
    """Executes master enterprise orchestration cycle across all active business units."""
    return orchestrator.run_business_cycle()
