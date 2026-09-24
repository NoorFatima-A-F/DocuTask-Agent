"""
FastAPI Endpoints for Phase 13.23 Enterprise Autonomous Agent Workforce & Digital Organization Platform (EAAWDOP)
"""
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.platform_workforce.runtime.workforce_master_orchestrator import workforce_master_orchestrator
from app.platform_workforce.models.schemas import (
    DigitalEmployee, EmployeeRole, DepartmentType, Department, DynamicTeam, TaskMarketplaceListing, NegotiationSession,
    CollaborationVote, ManagerReviewRecord, ExecutiveCouncilProposition,
    WorkforcePerformanceMetric, EconomicResourceBudget, HiringRequisition,
    CareerPromotionPath, WorkforceScheduleEntry, CollectiveMemoryRecord,
    ConflictResolutionRecord, OrganizationOverviewReport
)
from app.platform_workforce.registry.workforce_registry import workforce_registry
from app.platform_workforce.hierarchy.organization_hierarchy_engine import organization_hierarchy_engine
from app.platform_workforce.teams.dynamic_team_formation_engine import dynamic_team_formation_engine
from app.platform_workforce.marketplace.task_marketplace import task_marketplace
from app.platform_workforce.negotiation.negotiation_engine import negotiation_engine
from app.platform_workforce.collaboration.collaboration_protocol_engine import collaboration_protocol_engine
from app.platform_workforce.management.manager_ai_engine import manager_ai_engine
from app.platform_workforce.council.executive_council_engine import executive_council_engine
from app.platform_workforce.performance.workforce_performance_intelligence import workforce_performance_intelligence
from app.platform_workforce.economics.resource_allocation_engine import economic_resource_allocation_engine
from app.platform_workforce.hiring.autonomous_hiring_engine import autonomous_hiring_engine
from app.platform_workforce.career.promotion_career_engine import promotion_career_engine
from app.platform_workforce.scheduler.workforce_scheduler import workforce_scheduler
from app.platform_workforce.memory.collective_memory_engine import collective_memory_engine
from app.platform_workforce.conflict.conflict_resolution_engine import conflict_resolution_engine

router = APIRouter(tags=["Enterprise Autonomous Agent Workforce & Digital Organization"])

# Request Models
class HireEmployeeRequest(BaseModel):
    tenant_id: str = "default-tenant"
    name: str
    role: EmployeeRole
    department: DepartmentType
    manager_id: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    hourly_salary_usd: float = 2.50

class FormTeamRequest(BaseModel):
    tenant_id: str = "default-tenant"
    team_name: str
    mission: str
    required_skills: List[str] = Field(default_factory=list)
    max_budget_usd: float = 200.0
    sla_hours: float = 12.0

class PostTaskRequest(BaseModel):
    tenant_id: str = "default-tenant"
    title: str
    description: str
    required_skills: List[str] = Field(default_factory=list)
    budget_max_usd: float = 30.0
    priority: str = "MEDIUM"

class SubmitBidRequest(BaseModel):
    tenant_id: str = "default-tenant"
    task_id: str
    employee_id: str
    bid_cost_usd: float
    estimated_duration_minutes: float
    solution_outline: str = ""

class StartNegotiationRequest(BaseModel):
    tenant_id: str = "default-tenant"
    topic: str
    participant_ids: List[str] = Field(default_factory=list)
    initial_proposal: str

class CastVoteRequest(BaseModel):
    tenant_id: str = "default-tenant"
    vote_id: str
    employee_id: str
    choice: str  # YES / NO / ABSTAIN

class SubmitCouncilPropRequest(BaseModel):
    tenant_id: str = "default-tenant"
    title: str
    summary: str
    category: str = "STRATEGIC"
    impact_assessment: Dict[str, Any] = Field(default_factory=dict)

class CouncilVoteRequest(BaseModel):
    tenant_id: str = "default-tenant"
    proposition_id: str
    council_role: str
    vote: str

class StoreMemoryRequest(BaseModel):
    tenant_id: str = "default-tenant"
    title: str
    content: str
    author_id: str
    scope: str = "DEPARTMENT"
    scope_id: str = "ENGINEERING"
    tags: List[str] = Field(default_factory=list)

class ArbitrateConflictRequest(BaseModel):
    tenant_id: str = "default-tenant"
    party_a_id: str
    party_b_id: str
    dispute_subject: str
    mediator_id: str
    resolution_summary: str
    binding_agreements: List[str] = Field(default_factory=list)

# 1. Overview & Health
@router.get("/overview", response_model=OrganizationOverviewReport)
def get_workforce_overview(tenant_id: str = Query("default-tenant")):
    return workforce_master_orchestrator.get_organization_overview(tenant_id)

@router.get("/health")
def get_workforce_health(tenant_id: str = Query("default-tenant")):
    overview = workforce_master_orchestrator.get_organization_overview(tenant_id)
    return {
        "tenant_id": tenant_id,
        "status": "OPERATIONAL",
        "workforce_readiness_index": overview.workforce_readiness_index,
        "total_employees": overview.total_employees,
        "average_trust_score": overview.average_trust_score
    }

# 2. Employees & Registry
@router.get("/employees", response_model=List[DigitalEmployee])
def list_employees(
    tenant_id: str = Query("default-tenant"),
    department: Optional[DepartmentType] = Query(None),
    role: Optional[EmployeeRole] = Query(None)
):
    return workforce_registry.get_employees(tenant_id, department, role)

@router.get("/employees/{employee_id}", response_model=DigitalEmployee)
def get_employee_by_id(employee_id: str, tenant_id: str = Query("default-tenant")):
    emp = workforce_registry.get_employee(employee_id, tenant_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.post("/employees/hire", response_model=DigitalEmployee)
def hire_employee(req: HireEmployeeRequest):
    emp = DigitalEmployee(
        tenant_id=req.tenant_id,
        name=req.name,
        role=req.role,
        department=req.department,
        manager_id=req.manager_id,
        skills=req.skills,
        hourly_salary_usd=req.hourly_salary_usd
    )
    return workforce_registry.register_employee(emp)

# 3. Hierarchy & Organization
@router.get("/organization")
def get_organization_chart(tenant_id: str = Query("default-tenant")):
    return organization_hierarchy_engine.get_organization_chart(tenant_id)

@router.get("/departments", response_model=List[Department])
def list_departments(tenant_id: str = Query("default-tenant")):
    return organization_hierarchy_engine.get_departments(tenant_id)

# 4. Dynamic Teams
@router.get("/teams", response_model=List[DynamicTeam])
def list_teams(tenant_id: str = Query("default-tenant")):
    return dynamic_team_formation_engine.get_teams(tenant_id)

@router.post("/teams/form", response_model=DynamicTeam)
def form_team(req: FormTeamRequest):
    return dynamic_team_formation_engine.form_dynamic_team(
        team_name=req.team_name,
        mission=req.mission,
        required_skills=req.required_skills,
        max_budget_usd=req.max_budget_usd,
        sla_hours=req.sla_hours,
        tenant_id=req.tenant_id
    )

# 5. Task Marketplace
@router.get("/marketplace/tasks", response_model=List[TaskMarketplaceListing])
def list_marketplace_tasks(tenant_id: str = Query("default-tenant"), status: Optional[str] = Query(None)):
    return task_marketplace.get_tasks(tenant_id, status)

@router.post("/marketplace/tasks", response_model=TaskMarketplaceListing)
def post_marketplace_task(req: PostTaskRequest):
    return task_marketplace.post_task(
        title=req.title,
        description=req.description,
        required_skills=req.required_skills,
        budget_max_usd=req.budget_max_usd,
        priority=req.priority,
        tenant_id=req.tenant_id
    )

@router.post("/marketplace/bid", response_model=TaskMarketplaceListing)
def submit_task_bid(req: SubmitBidRequest):
    task = task_marketplace.submit_bid(
        task_id=req.task_id,
        employee_id=req.employee_id,
        bid_cost_usd=req.bid_cost_usd,
        estimated_duration_minutes=req.estimated_duration_minutes,
        solution_outline=req.solution_outline,
        tenant_id=req.tenant_id
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/marketplace/tasks/{task_id}/assign-optimal", response_model=TaskMarketplaceListing)
def assign_optimal_bid(task_id: str, tenant_id: str = Query("default-tenant")):
    task = task_marketplace.assign_optimal_bid(task_id, tenant_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task or bids not found")
    return task

# 6. Negotiation & Collaboration
@router.get("/negotiations", response_model=List[NegotiationSession])
def list_negotiations(tenant_id: str = Query("default-tenant")):
    return negotiation_engine.get_sessions(tenant_id)

@router.post("/negotiations", response_model=NegotiationSession)
def start_negotiation(req: StartNegotiationRequest):
    return negotiation_engine.start_negotiation(
        topic=req.topic,
        participant_ids=req.participant_ids,
        initial_proposal=req.initial_proposal,
        tenant_id=req.tenant_id
    )

@router.get("/collaborations/votes", response_model=List[CollaborationVote])
def list_collaboration_votes(tenant_id: str = Query("default-tenant")):
    return collaboration_protocol_engine.get_votes(tenant_id)

@router.post("/collaborations/vote", response_model=CollaborationVote)
def cast_collaboration_vote(req: CastVoteRequest):
    vote = collaboration_protocol_engine.cast_vote(
        vote_id=req.vote_id,
        employee_id=req.employee_id,
        choice=req.choice,
        tenant_id=req.tenant_id
    )
    if not vote:
        raise HTTPException(status_code=404, detail="Vote not found or already closed")
    return vote

# 7. Manager AI & Performance Reviews
@router.get("/management/reviews", response_model=List[ManagerReviewRecord])
def list_manager_reviews(tenant_id: str = Query("default-tenant"), employee_id: Optional[str] = Query(None)):
    return manager_ai_engine.get_reviews(tenant_id, employee_id)

@router.post("/management/reviews/conduct", response_model=ManagerReviewRecord)
def conduct_review(employee_id: str = Query(...), manager_id: str = Query(...), tenant_id: str = Query("default-tenant")):
    rev = manager_ai_engine.conduct_performance_review(employee_id, manager_id, tenant_id)
    if not rev:
        raise HTTPException(status_code=404, detail="Employee not found")
    return rev

# 8. Executive AI Council
@router.get("/executive-council/propositions", response_model=List[ExecutiveCouncilProposition])
def list_council_propositions(tenant_id: str = Query("default-tenant")):
    return executive_council_engine.get_propositions(tenant_id)

@router.post("/executive-council/propositions", response_model=ExecutiveCouncilProposition)
def submit_council_proposition(req: SubmitCouncilPropRequest):
    return executive_council_engine.submit_proposition(
        title=req.title,
        summary=req.summary,
        category=req.category,
        impact_assessment=req.impact_assessment,
        tenant_id=req.tenant_id
    )

@router.post("/executive-council/vote", response_model=ExecutiveCouncilProposition)
def vote_council_proposition(req: CouncilVoteRequest):
    prop = executive_council_engine.vote_on_proposition(
        proposition_id=req.proposition_id,
        council_role=req.council_role,
        vote=req.vote,
        tenant_id=req.tenant_id
    )
    if not prop:
        raise HTTPException(status_code=404, detail="Proposition not found")
    return prop

# 9. Performance & Analytics
@router.get("/performance", response_model=WorkforcePerformanceMetric)
def get_workforce_performance(tenant_id: str = Query("default-tenant")):
    return workforce_performance_intelligence.get_workforce_metrics(tenant_id)

# 10. Economics & Budgets
@router.get("/economics", response_model=EconomicResourceBudget)
def get_economic_budget(tenant_id: str = Query("default-tenant")):
    return economic_resource_allocation_engine.get_budget(tenant_id)

# 11. Hiring & Requisitions
@router.get("/hiring/requisitions", response_model=List[HiringRequisition])
def list_hiring_requisitions(tenant_id: str = Query("default-tenant")):
    return autonomous_hiring_engine.get_requisitions(tenant_id)

@router.post("/hiring/hire-candidate", response_model=DigitalEmployee)
def hire_candidate(requisition_id: str = Query(...), candidate_name: str = Query(...), tenant_id: str = Query("default-tenant")):
    emp = autonomous_hiring_engine.hire_candidate(requisition_id, candidate_name, tenant_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Requisition not found")
    return emp

# 12. Career & Promotions
@router.get("/career/paths", response_model=List[CareerPromotionPath])
def list_career_paths(tenant_id: str = Query("default-tenant")):
    return promotion_career_engine.get_career_paths(tenant_id)

@router.post("/career/evaluate/{employee_id}", response_model=CareerPromotionPath)
def evaluate_promotion(employee_id: str, tenant_id: str = Query("default-tenant")):
    path = promotion_career_engine.evaluate_promotion(employee_id, tenant_id)
    if not path:
        raise HTTPException(status_code=404, detail="Employee not found")
    return path

@router.post("/career/promote/{promotion_id}", response_model=CareerPromotionPath)
def execute_promotion(promotion_id: str, tenant_id: str = Query("default-tenant")):
    path = promotion_career_engine.execute_promotion(promotion_id, tenant_id)
    if not path:
        raise HTTPException(status_code=404, detail="Promotion path not found")
    return path

# 13. Workforce Schedules
@router.get("/schedules", response_model=List[WorkforceScheduleEntry])
def list_schedules(tenant_id: str = Query("default-tenant")):
    return workforce_scheduler.get_schedules(tenant_id)

# 14. Collective Memory
@router.get("/collective-memories", response_model=List[CollectiveMemoryRecord])
def list_collective_memories(tenant_id: str = Query("default-tenant"), scope: Optional[str] = Query(None)):
    return collective_memory_engine.get_memories(tenant_id, scope)

@router.post("/collective-memories", response_model=CollectiveMemoryRecord)
def store_collective_memory(req: StoreMemoryRequest):
    return collective_memory_engine.store_memory(
        title=req.title,
        content=req.content,
        author_id=req.author_id,
        scope=req.scope,
        scope_id=req.scope_id,
        tags=req.tags,
        tenant_id=req.tenant_id
    )

# 15. Conflict Resolution
@router.get("/conflicts", response_model=List[ConflictResolutionRecord])
def list_conflicts(tenant_id: str = Query("default-tenant")):
    return conflict_resolution_engine.get_conflicts(tenant_id)

@router.post("/conflicts/arbitrate", response_model=ConflictResolutionRecord)
def arbitrate_conflict(req: ArbitrateConflictRequest):
    return conflict_resolution_engine.arbitrate_dispute(
        party_a_id=req.party_a_id,
        party_b_id=req.party_b_id,
        dispute_subject=req.dispute_subject,
        mediator_id=req.mediator_id,
        resolution_summary=req.resolution_summary,
        binding_agreements=req.binding_agreements,
        tenant_id=req.tenant_id
    )
