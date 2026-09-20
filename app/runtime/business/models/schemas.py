"""
Phase 13.19: Enterprise Process Intelligence & Autonomous Business Orchestration Platform (EPI-ABOP)
Pydantic Schemas & Data Models.
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class StepType(str, Enum):
    TASK = "TASK"
    GATEWAY_EXCLUSIVE = "GATEWAY_EXCLUSIVE"
    GATEWAY_PARALLEL = "GATEWAY_PARALLEL"
    HUMAN_APPROVAL = "HUMAN_APPROVAL"
    TIMER = "TIMER"
    EVENT_TRIGGER = "EVENT_TRIGGER"
    SUBPROCESS = "SUBPROCESS"


class StepStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class ProcessStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DELEGATED = "DELEGATED"


class GoalStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    ACHIEVED = "ACHIEVED"
    AT_RISK = "AT_RISK"
    BLOCKED = "BLOCKED"


class ProcessStep(BaseModel):
    step_id: str
    name: str
    step_type: StepType = StepType.TASK
    department_id: str = "general"
    assigned_role: str = "agent"
    status: StepStatus = StepStatus.PENDING
    next_steps: List[str] = Field(default_factory=list)
    condition_expr: Optional[str] = None
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    sla_seconds: float = 300.0
    execution_duration_sec: float = 0.0
    error_message: Optional[str] = None


class BusinessProcess(BaseModel):
    process_id: str
    title: str
    description: str = ""
    owner_department: str = "Finance"
    status: ProcessStatus = ProcessStatus.ACTIVE
    steps: List[ProcessStep] = Field(default_factory=list)
    variables: Dict[str, Any] = Field(default_factory=dict)
    current_step_ids: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None


class Department(BaseModel):
    department_id: str
    name: str
    head_role: str
    parent_department_id: Optional[str] = None
    members_count: int = 10
    active_processes_count: int = 4
    operational_budget_monthly: float = 50000.0


class EmployeeOrAgentRole(BaseModel):
    role_id: str
    title: str
    department_id: str
    is_autonomous_agent: bool = True
    approval_limit_amount: float = 10000.0
    assigned_capabilities: List[str] = Field(default_factory=list)


class EnterpriseSystem(BaseModel):
    system_id: str
    name: str
    system_type: str = "ERP"  # ERP, CRM, HRIS, Core_Banking
    status: str = "ONLINE"
    connected_departments: List[str] = Field(default_factory=list)


class OrganizationGraph(BaseModel):
    departments: List[Department] = Field(default_factory=list)
    roles: List[EmployeeOrAgentRole] = Field(default_factory=list)
    systems: List[EnterpriseSystem] = Field(default_factory=list)
    approval_matrix: Dict[str, str] = Field(default_factory=dict)  # role_id -> manager_role_id


class OKRKeyResult(BaseModel):
    kr_id: str
    description: str
    target_value: float
    current_value: float
    unit: str
    achieved: bool = False


class BusinessGoal(BaseModel):
    goal_id: str
    title: str
    category: str = "EFFICIENCY"  # EFFICIENCY, REVENUE, ACCURACY, COMPLIANCE
    target_department: str = "Finance"
    status: GoalStatus = GoalStatus.IN_PROGRESS
    progress_pct: float = 0.0
    key_results: List[OKRKeyResult] = Field(default_factory=list)
    aligned_process_ids: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DecisionRule(BaseModel):
    rule_id: str
    rule_name: str
    condition_expression: str
    action_decision: str
    priority: int = 1
    enabled: bool = True


class DecisionTable(BaseModel):
    table_id: str
    name: str
    rules: List[DecisionRule] = Field(default_factory=list)


class SLAContract(BaseModel):
    sla_id: str
    process_id: str
    target_turnaround_sec: float
    warning_threshold_pct: float = 0.8
    escalation_role: str = "senior_operations_manager"


class SLABreachRisk(BaseModel):
    process_id: str
    step_id: str
    elapsed_sec: float
    sla_target_sec: float
    breach_probability: float
    is_breached: bool = False
    escalated: bool = False


class HumanApprovalTask(BaseModel):
    task_id: str
    process_id: str
    step_id: str
    title: str
    description: str
    department_id: str
    assigned_role: str
    amount: Optional[float] = None
    status: ApprovalStatus = ApprovalStatus.PENDING
    decision_rationale: Optional[str] = None
    decided_by: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    decided_at: Optional[str] = None


class DiscoveredProcess(BaseModel):
    discovered_id: str
    name: str
    frequency: int
    mean_duration_sec: float
    variants_count: int
    bottleneck_steps: List[str] = Field(default_factory=list)
    compliance_score: float = 0.95


class ProcessOptimizationRecommendation(BaseModel):
    recommendation_id: str
    process_id: str
    title: str
    action_type: str = "PARALLELIZE"  # PARALLELIZE, MERGE_APPROVALS, ELIMINATE_WASTE, AUTOMATE_GATE
    rationale: str
    estimated_cycle_time_reduction_pct: float
    estimated_annual_savings_usd: float
    confidence: float = 0.92


class ProcessSimulationConfig(BaseModel):
    process_id: str
    simulated_transactions_count: int = 1000
    agent_concurrency: int = 10
    human_approval_delay_mean_sec: float = 1800.0


class SimulationResult(BaseModel):
    simulation_id: str
    process_id: str
    baseline_cycle_time_sec: float
    optimized_cycle_time_sec: float
    baseline_cost_usd: float
    optimized_cost_usd: float
    cost_reduction_usd: float
    throughput_increase_pct: float
    simulated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class KPIDefinition(BaseModel):
    kpi_id: str
    name: str
    department: str
    current_value: float
    benchmark_value: float
    unit: str
    trend: str = "IMPROVING"  # IMPROVING, STABLE, DECLINING


class DigitalTwinOrgState(BaseModel):
    total_departments: int
    active_human_workers: int
    active_agent_workers: int
    running_business_processes: int
    pending_approvals: int
    mean_org_sla_compliance_pct: float
    department_workloads: Dict[str, float] = Field(default_factory=dict)  # department_id -> % load
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class BusinessExecutiveOverview(BaseModel):
    platform_name: str = "EPI-ABOP Enterprise Operating System"
    total_active_processes: int
    total_human_approvals_pending: int
    total_goals_tracked: int
    total_annualized_savings_usd: float
    mean_sla_compliance_pct: float
    mean_automation_rate_pct: float
    top_bottlenecks: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
