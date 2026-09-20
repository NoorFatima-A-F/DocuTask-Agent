"""
AMAEOP & Phase 13.14 FastAPI Endpoints - Enterprise Organization & Operations Platform
Exposes REST endpoints for:
- Legacy AMAEOP Pillars (Hierarchy, Executive Coordination, Negotiations, Long Running Ops, Health, Channels, Learning, SLAs, Incidents, Simulations)
- Phase 13.14 Autonomous AI Organization Platform (AAO-MAGEMEP: Missions, Strategy, Organization Design, Workforce, Projects, Resources, Performance, Finance, Governance, Digital Twin Simulation, and Continuous Runtime Coordinator).
"""

from fastapi import APIRouter, Query, Body, HTTPException
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

# Legacy Pillar 1
from app.runtime.organization.organization_graph import OrganizationGraphBuilder
from app.runtime.organization.organizational_state import org_state_manager
from app.runtime.organization.hierarchy_manager import HierarchyManager
from app.runtime.organization.organization_registry import OrganizationRegistry

# Legacy Pillar 2
from app.runtime.executive.executive_controller import executive_controller
from app.runtime.executive.mission_director import mission_director
from app.runtime.executive.coordination_engine import coordination_engine
from app.runtime.executive.delegation_manager import delegation_manager
from app.runtime.executive.executive_metrics import ExecutiveMetricsEngine

# Legacy Pillar 3
from app.runtime.negotiation.auction_manager import vickrey_auction_manager, AuctionBid
from app.runtime.negotiation.resource_negotiation import resource_negotiator
from app.runtime.negotiation.utility_negotiator import UtilityNegotiator
from app.runtime.negotiation.contract_manager import contract_manager

# Legacy Pillar 4
from app.runtime.operations.checkpoint_manager import checkpoint_manager
from app.runtime.operations.heartbeat_manager import heartbeat_manager
from app.runtime.operations.persistent_scheduler import persistent_scheduler
from app.runtime.operations.recovery_snapshot import RecoverySnapshotEngine
from app.runtime.operations.lease_manager import lease_manager

# Legacy Pillar 5
from app.runtime.org_health.org_health_aggregator import OrgHealthAggregator
from app.runtime.org_health.department_health import DepartmentHealthScorer

# Legacy Pillar 6
from app.runtime.communication.communication_bus import communication_bus
from app.runtime.communication.channel_manager import channel_manager
from app.runtime.communication.conversation_history import ConversationHistory

# Legacy Pillar 7
from app.runtime.org_learning.department_memory import department_memory_manager
from app.runtime.org_learning.department_reflection import DepartmentReflectionEngine
from app.runtime.org_learning.organizational_learning import OrganizationalLearningSynthesizer

# Legacy Pillar 8
from app.runtime.sla.sla_tracker import SLATracker
from app.runtime.sla.error_budget_governor import ErrorBudgetGovernor

# Legacy Pillar 9
from app.runtime.incident.incident_commander import incident_commander
from app.runtime.incident.incident_manager import IncidentManager
from app.runtime.incident.postmortem_generator import PostmortemGenerator

# Legacy Pillar 10
from app.runtime.org_simulation.org_simulator import OrganizationSimulator
from app.runtime.org_simulation.resilience_report import ResilienceReportGenerator

# Phase 13.14 AAO-MAGEMEP Subsystems
from app.runtime.organization.events.organization_events import (
    AgentRole,
    MissionPriority,
    org_event_bus,
)
from app.runtime.organization.mission.mission_engine import mission_engine
from app.runtime.organization.strategy.organization_strategy_engine import organization_strategy_engine
from app.runtime.organization.organization.organization_engine import organization_engine
from app.runtime.organization.workforce.workforce_engine import workforce_engine
from app.runtime.organization.project.project_engine import project_engine
from app.runtime.organization.resource.resource_engine import resource_engine
from app.runtime.organization.performance.performance_engine import performance_engine
from app.runtime.organization.finance.finance_engine import finance_engine
from app.runtime.organization.negotiation.negotiation_engine import negotiation_engine
from app.runtime.organization.governance.governance_engine import governance_engine
from app.runtime.organization.simulation.simulation_engine import (
    organization_simulation_engine,
    SimulationScenario,
)
from app.runtime.organization.runtime.organization_runtime import organization_runtime


router = APIRouter()


# ---------------------------------------------------------
# Legacy Pillar 1: Organizational Hierarchy Endpoints
# ---------------------------------------------------------
@router.get("/graph", summary="Get full organization hierarchy graph and reporting structure")
async def get_organization_graph() -> Dict[str, Any]:
    return OrganizationGraphBuilder.get_organization_graph()


@router.get("/departments", summary="List all specialized departments with real-time state")
async def list_departments() -> List[Dict[str, Any]]:
    return org_state_manager.list_departments()


@router.get("/departments/{department_id}", summary="Get deep details for specific department")
async def get_department(department_id: str) -> Dict[str, Any]:
    dept = org_state_manager.get_department(department_id)
    if not dept:
        raise HTTPException(status_code=404, detail=f"Department '{department_id}' not found.")
    return dept.to_dict()


@router.get("/roster", summary="Get enterprise agent roster and active workers")
async def get_agent_roster() -> List[Dict[str, Any]]:
    return OrganizationRegistry.get_agent_roster()


@router.get("/kpis", summary="Get macro organizational KPIs and health index")
async def get_organizational_kpis() -> Dict[str, Any]:
    return org_state_manager.get_organizational_kpis()


# ---------------------------------------------------------
# Legacy Pillar 2: Executive Coordination Endpoints
# ---------------------------------------------------------
@router.get("/executive/decisions", summary="List strategic executive decisions")
async def list_executive_decisions(limit: int = Query(50, ge=1, le=100)) -> List[Dict[str, Any]]:
    return executive_controller.list_executive_decisions(limit=limit)


@router.get("/executive/missions", summary="List multi-department strategic missions")
async def list_strategic_missions() -> List[Dict[str, Any]]:
    return mission_director.list_missions()


@router.get("/executive/barriers", summary="List cross-department barrier synchronizations")
async def list_coordination_barriers() -> List[Dict[str, Any]]:
    return coordination_engine.list_barriers()


@router.get("/executive/delegation-policies", summary="List delegation policies and autonomy bounds")
async def list_delegation_policies() -> List[Dict[str, Any]]:
    return delegation_manager.list_delegation_policies()


@router.get("/executive/summary", summary="Get executive leadership metrics and alignment score")
async def get_executive_summary() -> Dict[str, Any]:
    return ExecutiveMetricsEngine.get_executive_summary()


# ---------------------------------------------------------
# Legacy Pillar 3: Autonomous Negotiation Endpoints
# ---------------------------------------------------------
@router.get("/negotiation/auctions", summary="List Vickrey second-price auction history")
async def list_auctions() -> List[Dict[str, Any]]:
    return vickrey_auction_manager.list_auction_history()


class RunAuctionRequest(BaseModel):
    resource_type: str = "GPU_OCR_SLOT"
    units_available: int = 4
    bids: List[Dict[str, Any]]


@router.post("/negotiation/auctions/run", summary="Trigger a live Vickrey auction for compute slots")
async def run_vickrey_auction(req: RunAuctionRequest = Body(...)) -> Dict[str, Any]:
    bid_objects = [
        AuctionBid(
            bidder_department_id=b["bidder_department_id"],
            bid_amount_credits=float(b["bid_amount_credits"]),
            requested_units=int(b.get("requested_units", 1)),
            utility_weight=float(b.get("utility_weight", 0.5)),
        )
        for b in req.bids
    ]
    res = vickrey_auction_manager.run_auction(req.resource_type, req.units_available, bid_objects)
    return res.to_dict()


@router.get("/negotiation/trades", summary="List bilateral resource trade proposals")
async def list_resource_trades() -> List[Dict[str, Any]]:
    return resource_negotiator.list_trades()


@router.get("/negotiation/contracts", summary="List active inter-department resource contracts")
async def list_resource_contracts() -> List[Dict[str, Any]]:
    return contract_manager.list_contracts()


@router.get("/negotiation/nash-solution", summary="Compute Nash Bargaining Pareto resource allocation")
async def get_nash_bargaining(
    dept_a: str = Query("dept_extraction"),
    dept_b: str = Query("dept_ocr"),
    total_resource: float = Query(100.0),
) -> Dict[str, Any]:
    sol = UtilityNegotiator.solve_nash_bargaining(dept_a, dept_b, total_resource)
    return sol.to_dict()


# ---------------------------------------------------------
# Legacy Pillar 4: Long Running Operations Endpoints
# ---------------------------------------------------------
@router.get("/operations/checkpoints", summary="List checkpoints for mission")
async def list_checkpoints(mission_id: str = Query("mission_live_001")) -> List[Dict[str, Any]]:
    return checkpoint_manager.list_mission_checkpoints(mission_id)


@router.get("/operations/heartbeats", summary="Check department liveliness and heartbeats")
async def check_heartbeats() -> Dict[str, Any]:
    return heartbeat_manager.check_liveness()


@router.get("/operations/scheduler", summary="List scheduled long-running operations")
async def list_scheduled_operations() -> List[Dict[str, Any]]:
    return persistent_scheduler.list_scheduled_operations()


@router.get("/operations/leases", summary="List active distributed resource leases")
async def list_leases() -> List[Dict[str, Any]]:
    return lease_manager.list_leases()


@router.post("/operations/recover", summary="Execute crash recovery for a mission")
async def recover_mission(mission_id: str = Query("mission_live_001")) -> Dict[str, Any]:
    return RecoverySnapshotEngine.recover_mission(mission_id).to_dict()


# ---------------------------------------------------------
# Legacy Pillar 5: Organization Health Intelligence Endpoints
# ---------------------------------------------------------
@router.get("/health", summary="Get comprehensive organization health report")
async def get_organization_health() -> Dict[str, Any]:
    return OrgHealthAggregator.get_organization_health_report()


# ---------------------------------------------------------
# Legacy Pillar 6: Cross-Agent Communication Bus Endpoints
# ---------------------------------------------------------
@router.get("/communication/channels", summary="List all inter-department channels")
async def list_channels() -> List[Dict[str, Any]]:
    return channel_manager.list_channels()


@router.get("/communication/messages", summary="Get real-time signed message stream")
async def get_messages(
    channel_name: Optional[str] = Query(None),
    department_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
) -> List[Dict[str, Any]]:
    return communication_bus.get_messages(channel_name=channel_name, department_id=department_id, limit=limit)


@router.get("/communication/history", summary="Get tamper-evident conversation history for mission")
async def get_conversation_history(mission_id: str = Query("mission_live_001")) -> Dict[str, Any]:
    return ConversationHistory.get_mission_conversation(mission_id)


# ---------------------------------------------------------
# Legacy Pillar 7: Organizational Learning Endpoints
# ---------------------------------------------------------
@router.get("/learning/summary", summary="Get organizational learning synthesis and retrospectives")
async def get_learning_summary() -> Dict[str, Any]:
    return OrganizationalLearningSynthesizer.get_organization_learning_summary()


@router.get("/learning/knowledge", summary="List specialized department procedural knowledge")
async def list_department_knowledge() -> Dict[str, List[Dict[str, Any]]]:
    return department_memory_manager.list_all_knowledge()


# ---------------------------------------------------------
# Legacy Pillar 8: Enterprise SLA Intelligence Endpoints
# ---------------------------------------------------------
@router.get("/sla/summary", summary="Get enterprise SLA, MTTR, MTBF, and availability summary")
async def get_sla_summary() -> Dict[str, Any]:
    return SLATracker.get_enterprise_sla_summary()


@router.get("/sla/error-budgets", summary="Get SRE error budget status and burn rates")
async def get_error_budgets() -> Dict[str, Any]:
    return ErrorBudgetGovernor.get_summary()


# ---------------------------------------------------------
# Legacy Pillar 9: Enterprise Incident Command Center Endpoints
# ---------------------------------------------------------
@router.get("/incident/incidents", summary="List active and resolved enterprise incidents")
async def list_incidents() -> List[Dict[str, Any]]:
    return incident_commander.list_incidents()


@router.get("/incident/postmortem", summary="Get postmortem report for incident")
async def get_postmortem(incident_id: str = Query("inc_2026_001")) -> Dict[str, Any]:
    return PostmortemGenerator.generate_postmortem(incident_id)


@router.get("/incident/blast-radius", summary="Get incident impact and blast radius assessment")
async def get_blast_radius(incident_id: str = Query("inc_2026_001")) -> Dict[str, Any]:
    return IncidentManager.analyze_incident_blast_radius(incident_id)


# ---------------------------------------------------------
# Legacy Pillar 10: Autonomous Organization Simulation Endpoints
# ---------------------------------------------------------
@router.get("/simulation/monte-carlo", summary="Run 100-organization Monte Carlo digital twin simulation")
async def run_simulation(
    orgs: int = Query(100, ge=10, le=500),
    missions_per_org: int = Query(10, ge=1, le=50),
    seed: int = Query(42),
) -> Dict[str, Any]:
    return OrganizationSimulator.run_monte_carlo_simulation(orgs, missions_per_org, seed)


@router.get("/simulation/resilience-report", summary="Get official enterprise resilience certification dossier")
async def get_resilience_report() -> Dict[str, Any]:
    return ResilienceReportGenerator.generate_resilience_dossier()


# ===========================================================================
# Phase 13.14 - Autonomous AI Organization Platform (AAO-MAGEMEP) Endpoints
# ===========================================================================

# ---------------------------------------------------------
# 1. Overview & Health Cockpit
# ---------------------------------------------------------
@router.get("/overview", summary="Macro organizational health, missions, workforce and ROI summary")
async def get_organization_overview() -> Dict[str, Any]:
    return organization_runtime.get_overview()


# ---------------------------------------------------------
# 2. Mission Understanding & Decomposition
# ---------------------------------------------------------
class DecomposeGoalRequest(BaseModel):
    goal: str = Field(..., example="Reduce document processing cost by 40% while maintaining >=98% accuracy")
    priority: MissionPriority = MissionPriority.HIGH
    timeline_days: int = 90
    custom_constraints: Optional[List[str]] = None


@router.get("/missions", summary="List all active, planned, and completed enterprise missions")
async def list_enterprise_missions() -> List[Dict[str, Any]]:
    return [m.model_dump() for m in mission_engine.list_missions()]


@router.post("/missions", summary="Decompose natural language goal into structured machine mission")
async def create_mission(req: DecomposeGoalRequest = Body(...)) -> Dict[str, Any]:
    mission = mission_engine.decompose_goal(
        goal=req.goal,
        priority=req.priority,
        timeline_days=req.timeline_days,
        custom_constraints=req.custom_constraints,
    )
    return mission.model_dump()


@router.post("/missions/{mission_id}/validate", summary="Validate mission feasibility, constraints, and alignment")
async def validate_mission(mission_id: str) -> Dict[str, Any]:
    res = mission_engine.validate_mission(mission_id)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res


# ---------------------------------------------------------
# 3. Strategy Generation & Simulation
# ---------------------------------------------------------
class GenerateStrategiesRequest(BaseModel):
    mission_id: str = "msn_reduce_cost_40pct"
    count: int = 3


@router.get("/strategies", summary="List generated strategy plans")
async def list_strategies(mission_id: Optional[str] = Query(None)) -> List[Dict[str, Any]]:
    return [s.model_dump() for s in organization_strategy_engine.list_strategies(mission_id=mission_id)]


@router.post("/strategies/generate", summary="Synthesize candidate strategy plans for a mission")
async def generate_strategies(req: GenerateStrategiesRequest = Body(...)) -> List[Dict[str, Any]]:
    strats = organization_strategy_engine.generate_strategies(mission_id=req.mission_id, count=req.count)
    return [s.model_dump() for s in strats]


@router.post("/strategies/{strategy_id}/evaluate", summary="Run Monte Carlo simulation on strategy")
async def evaluate_strategy(strategy_id: str, iterations: int = Query(500, ge=50, le=2000)) -> Dict[str, Any]:
    res = organization_strategy_engine.evaluate_strategy_monte_carlo(strategy_id, iterations=iterations)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res


# ---------------------------------------------------------
# 4. Organization Design & Structure
# ---------------------------------------------------------
class DesignOrgRequest(BaseModel):
    mission_id: str = "msn_reduce_cost_40pct"
    strategy_id: str = "strat_adaptive_quantization_001"


@router.get("/structure", summary="Get virtual organization structure, departments, and teams")
async def get_organization_structure(org_id: Optional[str] = Query(None)) -> Dict[str, Any]:
    return organization_engine.get_structure(org_id=org_id).model_dump()


@router.post("/design", summary="Dynamically design virtual organization for mission strategy")
async def design_organization(req: DesignOrgRequest = Body(...)) -> Dict[str, Any]:
    org = organization_engine.design_organization_for_mission(req.mission_id, req.strategy_id)
    return org.model_dump()


@router.post("/restructure", summary="Restructure organization to eliminate bottlenecks")
async def restructure_organization(org_id: str = Query("org_enterprise_root")) -> Dict[str, Any]:
    return organization_engine.restructure_organization(org_id).model_dump()


# ---------------------------------------------------------
# 5. Workforce & Agent Employees
# ---------------------------------------------------------
class HireAgentRequest(BaseModel):
    name: str
    role: AgentRole
    department_id: str
    skill_names: Optional[List[str]] = None
    hourly_cost: float = 0.12


@router.get("/agents", summary="List autonomous agent employees, skill profiles, and workloads")
async def list_workforce_agents(department_id: Optional[str] = Query(None)) -> List[Dict[str, Any]]:
    return [a.model_dump() for a in workforce_engine.list_agents(department_id=department_id)]


@router.post("/assign", summary="Hire or assign specialized agent employee")
async def hire_agent(req: HireAgentRequest = Body(...)) -> Dict[str, Any]:
    agent = workforce_engine.hire_agent(
        name=req.name,
        role=req.role,
        department_id=req.department_id,
        skill_names=req.skill_names,
        hourly_cost=req.hourly_cost,
    )
    return agent.model_dump()


@router.post("/workforce/optimize", summary="Rebalance workloads across agent workforce")
async def optimize_workforce() -> Dict[str, Any]:
    return workforce_engine.optimize_workforce_allocation()


# ---------------------------------------------------------
# 6. Autonomous Projects & Critical Path
# ---------------------------------------------------------
class CreateProjectRequest(BaseModel):
    mission_id: str = "msn_reduce_cost_40pct"
    title: str
    description: str = ""
    task_specs: List[Dict[str, Any]]
    lead_agent_id: str = "agent_cto_architect"


@router.get("/projects", summary="List active virtual projects, milestones, and critical paths")
async def list_projects(mission_id: Optional[str] = Query(None)) -> List[Dict[str, Any]]:
    return [p.model_dump() for p in project_engine.list_projects(mission_id=mission_id)]


@router.post("/projects/create", summary="Create structured project with CPM critical path schedule")
async def create_project(req: CreateProjectRequest = Body(...)) -> Dict[str, Any]:
    proj = project_engine.create_project(
        mission_id=req.mission_id,
        title=req.title,
        description=req.description,
        task_specs=req.task_specs,
        lead_agent_id=req.lead_agent_id,
    )
    return proj.model_dump()


@router.post("/projects/{project_id}/replan", summary="Autonomously replan project to resolve bottlenecks")
async def replan_project(project_id: str) -> Dict[str, Any]:
    return project_engine.replan_project(project_id).model_dump()


# ---------------------------------------------------------
# 7. Resource Allocation & Intelligence
# ---------------------------------------------------------
@router.get("/resources", summary="Get resource pool status and department quotas")
async def get_resources() -> Dict[str, Any]:
    return {
        "pool": resource_engine.get_pool_status().model_dump(),
        "allocation_plan": resource_engine.get_current_allocation().model_dump(),
    }


@router.post("/resources/optimize", summary="Solve Pareto linear optimization for compute and token quotas")
async def optimize_resources(prioritize_metric: str = Query("COST_EFFICIENCY")) -> Dict[str, Any]:
    return resource_engine.optimize_resources(prioritize_metric=prioritize_metric).model_dump()


# ---------------------------------------------------------
# 8. Performance Scorecards
# ---------------------------------------------------------
@router.get("/scorecard", summary="Get comprehensive organization, team, and agent scorecards")
async def get_performance_scorecard() -> Dict[str, Any]:
    return performance_engine.generate_scorecard().model_dump()


# ---------------------------------------------------------
# 9. Finance & Unit Economics
# ---------------------------------------------------------
@router.get("/roi", summary="Get financial summary, cost metrics, and ROI projection")
async def get_finance_roi() -> Dict[str, Any]:
    return finance_engine.get_financial_summary().model_dump()


@router.post("/finance/forecast", summary="Run multi-month operational cost forecast")
async def forecast_finance(months: int = Query(12, ge=1, le=36)) -> Dict[str, Any]:
    return finance_engine.forecast_costs(horizon_months=months).model_dump()


# ---------------------------------------------------------
# 10. Multi-Agent Negotiation
# ---------------------------------------------------------
class InitiateNegotiationRequest(BaseModel):
    initiator: AgentRole = AgentRole.RESEARCH_AGENT
    respondent: AgentRole = AgentRole.OPERATIONS_AGENT
    topic: str = "GPU Inference Slot Dispute"
    requested_resource: str = "GPU_SLOTS"
    requested_units: float = 16.0
    rationale: str = "Needed for urgent model compression benchmarking."


@router.get("/negotiations", summary="List multi-agent negotiation logs and Nash settlements")
async def list_negotiations() -> List[Dict[str, Any]]:
    return [n.model_dump() for n in negotiation_engine.list_negotiations()]


@router.post("/negotiate", summary="Initiate bargaining session and solve for Nash equilibrium")
async def initiate_negotiation(req: InitiateNegotiationRequest = Body(...)) -> Dict[str, Any]:
    neg = negotiation_engine.initiate_negotiation(
        initiator=req.initiator,
        respondent=req.respondent,
        topic=req.topic,
        requested_resource=req.requested_resource,
        requested_units=req.requested_units,
        rationale=req.rationale,
    )
    agreement = negotiation_engine.solve_nash_equilibrium(neg.negotiation_id)
    return {
        "negotiation": negotiation_engine.get_negotiation(neg.negotiation_id).model_dump(),
        "settled_agreement": agreement.model_dump(),
    }


# ---------------------------------------------------------
# 11. Organizational Governance
# ---------------------------------------------------------
class ReviewDecisionRequest(BaseModel):
    decision_title: str
    proposing_role: AgentRole = AgentRole.CEO_AGENT
    decision_payload: Dict[str, Any] = Field(default_factory=dict)
    simulation_verified: bool = True


@router.get("/governance/reviews", summary="List organizational governance reviews and seals")
async def list_governance_reviews() -> List[Dict[str, Any]]:
    return [r.model_dump() for r in governance_engine.list_reviews()]


@router.post("/governance/review", summary="Submit decision for multi-pillar governance review")
async def review_governance_decision(req: ReviewDecisionRequest = Body(...)) -> Dict[str, Any]:
    rev = governance_engine.review_decision(
        decision_title=req.decision_title,
        proposing_role=req.proposing_role,
        decision_payload=req.decision_payload,
        simulation_verified=req.simulation_verified,
    )
    return rev.model_dump()


@router.post("/governance/approve", summary="Approve governance decision")
async def approve_governance(review_id: str = Query(...), human_override: bool = Query(False)) -> Dict[str, Any]:
    return governance_engine.approve_decision(review_id, human_override=human_override).model_dump()


@router.post("/governance/reject", summary="Reject governance decision")
async def reject_governance(review_id: str = Query(...), reason: str = Query("Violates budget ceiling")) -> Dict[str, Any]:
    return governance_engine.reject_decision(review_id, reason=reason).model_dump()


# ---------------------------------------------------------
# 12. Digital Twin Simulations
# ---------------------------------------------------------
@router.get("/simulations", summary="List digital twin simulation reports")
async def list_simulation_reports() -> List[Dict[str, Any]]:
    return [r.model_dump() for r in organization_simulation_engine.list_reports()]


@router.post("/simulations/run", summary="Run stochastic digital twin organizational simulation")
async def run_org_simulation(runs: int = Query(100, ge=10, le=500)) -> Dict[str, Any]:
    rep = organization_simulation_engine.run_simulation(runs=runs)
    return rep.model_dump()


# ---------------------------------------------------------
# 13. Master Autonomous Cycle
# ---------------------------------------------------------
class RunCycleRequest(BaseModel):
    mission_goal: str = "Reduce document processing cost by 40% while maintaining >=98% accuracy"


@router.get("/cycles", summary="List executed autonomous organizational cycles")
async def list_cycles() -> List[Dict[str, Any]]:
    return [c.model_dump() for c in organization_runtime.list_cycles()]


@router.post("/cycle", summary="Trigger complete end-to-end autonomous organization execution cycle")
async def run_organization_cycle(req: RunCycleRequest = Body(...)) -> Dict[str, Any]:
    summary = organization_runtime.run_full_autonomous_cycle(mission_goal=req.mission_goal)
    return summary.model_dump()
