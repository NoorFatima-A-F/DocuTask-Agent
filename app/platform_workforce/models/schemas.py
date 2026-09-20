"""
Phase 13.23 - Enterprise Autonomous Agent Workforce & Digital Organization Platform (EAAWDOP) Schemas
"""
from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid

class EmployeeRole(str, Enum):
    CEO = "CEO"
    VP = "VP"
    DIRECTOR = "DIRECTOR"
    MANAGER = "MANAGER"
    PRINCIPAL_ARCHITECT = "PRINCIPAL_ARCHITECT"
    LEAD_SPECIALIST = "LEAD_SPECIALIST"
    SENIOR_SPECIALIST = "SENIOR_SPECIALIST"
    ASSOCIATE_SPECIALIST = "ASSOCIATE_SPECIALIST"
    JUNIOR_WORKER = "JUNIOR_WORKER"
    REVIEWER = "REVIEWER"
    AUDITOR = "AUDITOR"
    ARBITRATOR = "ARBITRATOR"

class DepartmentType(str, Enum):
    EXECUTIVE = "EXECUTIVE"
    ENGINEERING = "ENGINEERING"
    OPERATIONS = "OPERATIONS"
    FINANCE = "FINANCE"
    SECURITY_COMPLIANCE = "SECURITY_COMPLIANCE"
    BUSINESS_STRATEGY = "BUSINESS_STRATEGY"
    QUALITY_ASSURANCE = "QUALITY_ASSURANCE"
    CUSTOMER_SUCCESS = "CUSTOMER_SUCCESS"

class EmployeeStatus(str, Enum):
    ACTIVE = "ACTIVE"
    BUSY = "BUSY"
    IN_MEETING = "IN_MEETING"
    ON_CALL = "ON_CALL"
    STANDBY = "STANDBY"
    MAINTENANCE = "MAINTENANCE"
    PROMOTED = "PROMOTED"
    RETIRED = "RETIRED"

class DigitalEmployee(BaseModel):
    id: str = Field(default_factory=lambda: f"emp-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    name: str
    role: EmployeeRole
    department: DepartmentType
    manager_id: Optional[str] = None
    level: int = 1  # 1 (Junior) to 8 (CEO)
    skills: List[str] = Field(default_factory=list)
    security_clearance: str = "CONFIDENTIAL"  # PUBLIC, CONFIDENTIAL, SECRET, TOP_SECRET
    availability_status: EmployeeStatus = EmployeeStatus.ACTIVE
    capacity_slots: int = 5
    assigned_tasks_count: int = 0
    trust_score: float = 0.95
    hourly_salary_usd: float = 2.50
    token_cost_multiplier: float = 1.0
    lifetime_tasks_completed: int = 0
    task_success_rate: float = 0.98
    burnout_risk_score: float = 0.05
    career_history: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Department(BaseModel):
    id: str = Field(default_factory=lambda: f"dept-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    name: str
    dept_type: DepartmentType
    manager_id: Optional[str] = None
    headcount: int = 0
    monthly_budget_usd: float = 10000.0
    active_projects: List[str] = Field(default_factory=list)
    okrs: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DynamicTeam(BaseModel):
    id: str = Field(default_factory=lambda: f"team-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    team_name: str
    mission: str
    team_lead_id: str
    member_ids: List[str] = Field(default_factory=list)
    required_skills: List[str] = Field(default_factory=list)
    max_budget_usd: float = 500.0
    sla_hours: float = 24.0
    active_tasks: List[str] = Field(default_factory=list)
    team_health_score: float = 0.96
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TaskMarketplaceListing(BaseModel):
    id: str = Field(default_factory=lambda: f"task-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    title: str
    description: str
    required_skills: List[str] = Field(default_factory=list)
    priority: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL
    budget_max_usd: float = 50.0
    deadline: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "OPEN"  # OPEN, BIDDING, ASSIGNED, IN_PROGRESS, COMPLETED
    assigned_employee_id: Optional[str] = None
    bids: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TaskBid(BaseModel):
    bid_id: str = Field(default_factory=lambda: f"bid-{uuid.uuid4().hex[:8]}")
    task_id: str
    employee_id: str
    bid_cost_usd: float
    estimated_duration_minutes: float
    confidence_score: float = 0.95
    proposed_solution_outline: str = ""
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class NegotiationSession(BaseModel):
    id: str = Field(default_factory=lambda: f"neg-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    topic: str
    participant_employee_ids: List[str] = Field(default_factory=list)
    proposals: List[Dict[str, Any]] = Field(default_factory=list)
    consensus_reached: bool = False
    agreed_terms: Dict[str, Any] = Field(default_factory=dict)
    status: str = "IN_PROGRESS"  # IN_PROGRESS, AGREED, DEADLOCKED, ESCALATED
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CollaborationVote(BaseModel):
    id: str = Field(default_factory=lambda: f"vote-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    proposal_title: str
    initiator_employee_id: str
    voter_employee_ids: List[str] = Field(default_factory=list)
    votes: Dict[str, str] = Field(default_factory=dict)  # employee_id -> "YES" / "NO" / "ABSTAIN"
    required_quorum: float = 0.66
    status: str = "PENDING"  # PENDING, APPROVED, REJECTED
    decided_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ManagerReviewRecord(BaseModel):
    id: str = Field(default_factory=lambda: f"rev-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    employee_id: str
    manager_id: str
    review_period: str = "2026-Q1"
    performance_rating: float = 4.8  # out of 5.0
    strengths: List[str] = Field(default_factory=list)
    areas_for_growth: List[str] = Field(default_factory=list)
    workload_balance_action: str = "OPTIMAL"  # OFF_LOAD_TASKS, ASSIGN_MORE, KEEP_STABLE
    promotion_recommended: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ExecutiveCouncilProposition(BaseModel):
    id: str = Field(default_factory=lambda: f"prop-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    title: str
    summary: str
    category: str = "STRATEGIC"  # STRATEGIC, FINANCIAL, SECURITY, ARCHITECTURAL, COMPLIANCE
    council_votes: Dict[str, str] = Field(default_factory=dict)  # council_role -> "APPROVE" | "REJECT" | "DEFER"
    quorum_met: bool = False
    enacted: bool = False
    impact_assessment: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class WorkforcePerformanceMetric(BaseModel):
    tenant_id: str = "default-tenant"
    total_workforce_headcount: int = 0
    active_employees_count: int = 0
    workforce_utilization_rate: float = 0.78
    average_trust_score: float = 0.96
    average_task_success_rate: float = 0.985
    collaboration_index: float = 0.92
    innovation_velocity_score: float = 0.89
    workforce_burnout_risk: float = 0.08
    monthly_salary_burn_usd: float = 12450.0

class EconomicResourceBudget(BaseModel):
    tenant_id: str = "default-tenant"
    allocated_gpu_hours: float = 1200.0
    used_gpu_hours: float = 780.0
    allocated_tokens: int = 500_000_000
    used_tokens: int = 310_000_000
    total_budget_usd: float = 25000.0
    total_spent_usd: float = 14200.0
    efficiency_roi_ratio: float = 4.85
    reallocation_recommendations: List[str] = Field(default_factory=list)

class HiringRequisition(BaseModel):
    id: str = Field(default_factory=lambda: f"req-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    department: DepartmentType
    target_role: EmployeeRole
    required_skills: List[str] = Field(default_factory=list)
    reason: str = "CAPACITY_OVERLOAD"
    status: str = "APPROVED"  # DRAFT, PENDING_APPROVAL, APPROVED, FILLED
    candidate_profiles: List[Dict[str, Any]] = Field(default_factory=list)
    hired_employee_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CareerPromotionPath(BaseModel):
    id: str = Field(default_factory=lambda: f"promo-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    employee_id: str
    current_role: EmployeeRole
    target_role: EmployeeRole
    eligibility_score: float = 0.92
    completed_milestones: List[str] = Field(default_factory=list)
    status: str = "READY"  # IN_PROGRESS, READY, PROMOTED
    promoted_at: Optional[datetime] = None

class WorkforceScheduleEntry(BaseModel):
    id: str = Field(default_factory=lambda: f"sched-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    employee_id: str
    shift_name: str  # "EMEA_MORNING", "APAC_FOLLOW_THE_SUN", "US_CORE", "MAINTENANCE_ROTATION"
    time_zone: str = "UTC"
    start_hour: int = 0
    end_hour: int = 8
    is_active: bool = True

class CollectiveMemoryRecord(BaseModel):
    id: str = Field(default_factory=lambda: f"cmem-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    scope: str = "DEPARTMENT"  # TEAM, DEPARTMENT, EXECUTIVE, ENTERPRISE
    scope_id: str = "ENGINEERING"
    title: str
    content: str
    tags: List[str] = Field(default_factory=list)
    author_employee_id: str
    trust_weight: float = 0.98
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ConflictResolutionRecord(BaseModel):
    id: str = Field(default_factory=lambda: f"conf-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    party_a_id: str
    party_b_id: str
    dispute_subject: str
    mediator_employee_id: str
    status: str = "RESOLVED"  # OPEN, MEDIATING, ARBITRATING, RESOLVED
    resolution_summary: str
    binding_agreements: List[str] = Field(default_factory=list)
    resolved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OrganizationOverviewReport(BaseModel):
    tenant_id: str = "default-tenant"
    total_employees: int = 0
    total_departments: int = 0
    active_teams: int = 0
    marketplace_open_tasks: int = 0
    council_active_propositions: int = 0
    average_trust_score: float = 0.95
    workforce_readiness_index: float = 0.94
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
