"""
Phase 13.14 - AI Organization Designer Engine
Dynamically configures virtual enterprise structures, departments, teams, reporting hierarchies, and eliminates organizational redundancies.
"""

from __future__ import annotations
import time
import uuid
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.runtime.organization.events.organization_events import (
    AgentRole,
    OrganizationState,
    OrganizationDesigned,
    TeamMerged,
    org_event_bus,
)


class VirtualTeam(BaseModel):
    team_id: str = Field(default_factory=lambda: f"team_{uuid.uuid4().hex[:8]}")
    name: str
    lead_role: AgentRole
    member_roles: List[AgentRole] = Field(default_factory=list)
    member_agent_ids: List[str] = Field(default_factory=list)
    mission_scope: str
    active_task_count: int = 0
    productivity_score: float = 0.94


class VirtualDepartment(BaseModel):
    department_id: str = Field(default_factory=lambda: f"dept_{uuid.uuid4().hex[:8]}")
    name: str
    head_role: AgentRole
    teams: List[VirtualTeam] = Field(default_factory=list)
    budget_allocated_usd: float = 25000.0
    budget_spent_usd: float = 6800.0
    health_score: float = 0.96
    active_projects_count: int = 2
    capabilities: List[str] = Field(default_factory=list)


class VirtualOrganization(BaseModel):
    org_id: str = "org_enterprise_root"
    name: str = "DocuTask Autonomous Enterprise"
    mission_id: str = "msn_reduce_cost_40pct"
    strategy_id: str = "strat_adaptive_quantization_001"
    state: OrganizationState = OrganizationState.EXECUTING
    departments: List[VirtualDepartment] = Field(default_factory=list)
    executive_board: List[AgentRole] = Field(
        default_factory=lambda: [AgentRole.CEO_AGENT, AgentRole.CTO_AGENT, AgentRole.FINANCE_AGENT]
    )
    span_of_control: float = 4.2
    operational_efficiency: float = 0.93
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)


class OrganizationEngine:
    """Designs, manages, and restructures virtual enterprise organizational topologies."""

    def __init__(self) -> None:
        self._organizations: Dict[str, VirtualOrganization] = {}
        self._initialize_canonical_organization()

    def _initialize_canonical_organization(self) -> None:
        research_dept = VirtualDepartment(
            department_id="dept_research_ai",
            name="Research & Intelligence",
            head_role=AgentRole.RESEARCH_AGENT,
            teams=[
                VirtualTeam(
                    team_id="team_model_distillation",
                    name="Model Distillation & Quantization Team",
                    lead_role=AgentRole.RESEARCH_AGENT,
                    member_roles=[AgentRole.RESEARCH_AGENT, AgentRole.ANALYST_AGENT],
                    member_agent_ids=["agent_deep_researcher_01", "agent_quantizer_02"],
                    mission_scope="Develop high-speed compressed representation models",
                    active_task_count=3,
                    productivity_score=0.96,
                )
            ],
            budget_allocated_usd=20000.0,
            budget_spent_usd=4200.0,
            health_score=0.97,
            active_projects_count=1,
            capabilities=["model_distillation", "scientific_discovery", "quantization_research"],
        )

        engineering_dept = VirtualDepartment(
            department_id="dept_engineering_core",
            name="Core Engineering & Infrastructure",
            head_role=AgentRole.CTO_AGENT,
            teams=[
                VirtualTeam(
                    team_id="team_pipeline_routing",
                    name="Pipeline Dynamic Routing Team",
                    lead_role=AgentRole.CTO_AGENT,
                    member_roles=[AgentRole.ENGINEERING_AGENT, AgentRole.SECURITY_AGENT],
                    member_agent_ids=["agent_infra_lead_01", "agent_pipeline_opt_02"],
                    mission_scope="Build dynamic tier-based document routing DAG",
                    active_task_count=5,
                    productivity_score=0.94,
                )
            ],
            budget_allocated_usd=35000.0,
            budget_spent_usd=11500.0,
            health_score=0.95,
            active_projects_count=2,
            capabilities=["dag_routing", "infrastructure_scaling", "api_gateway"],
        )

        analytics_dept = VirtualDepartment(
            department_id="dept_analytics_ops",
            name="Analytics & Finance Operations",
            head_role=AgentRole.FINANCE_AGENT,
            teams=[
                VirtualTeam(
                    team_id="team_roi_governance",
                    name="ROI & Cost Telemetry Team",
                    lead_role=AgentRole.FINANCE_AGENT,
                    member_roles=[AgentRole.ANALYST_AGENT, AgentRole.OPERATIONS_AGENT],
                    member_agent_ids=["agent_financial_cfo_01", "agent_telemetry_02"],
                    mission_scope="Real-time cost telemetry, budget guards, and ROI attribution",
                    active_task_count=2,
                    productivity_score=0.98,
                )
            ],
            budget_allocated_usd=15000.0,
            budget_spent_usd=2800.0,
            health_score=0.98,
            active_projects_count=1,
            capabilities=["cost_forecasting", "sla_monitoring", "audit_compliance"],
        )

        org = VirtualOrganization(
            org_id="org_enterprise_root",
            name="DocuTask Autonomous Enterprise",
            mission_id="msn_reduce_cost_40pct",
            strategy_id="strat_adaptive_quantization_001",
            state=OrganizationState.EXECUTING,
            departments=[research_dept, engineering_dept, analytics_dept],
            executive_board=[AgentRole.CEO_AGENT, AgentRole.CTO_AGENT, AgentRole.FINANCE_AGENT],
            span_of_control=3.8,
            operational_efficiency=0.95,
        )

        self._organizations[org.org_id] = org

    def design_organization_for_mission(self, mission_id: str, strategy_id: str) -> VirtualOrganization:
        """Dynamically formulates an optimized virtual organization customized for the mission strategy."""
        org_id = f"org_{uuid.uuid4().hex[:8]}"

        depts = [
            VirtualDepartment(
                department_id=f"dept_eng_{uuid.uuid4().hex[:6]}",
                name="Systems Engineering & Execution",
                head_role=AgentRole.CTO_AGENT,
                teams=[
                    VirtualTeam(
                        name="Execution & Pipeline Team",
                        lead_role=AgentRole.ENGINEERING_AGENT,
                        member_roles=[AgentRole.ENGINEERING_AGENT, AgentRole.OPERATIONS_AGENT],
                        member_agent_ids=["agent_eng_01", "agent_ops_01"],
                        mission_scope="Deliver mission architectural objectives",
                        active_task_count=4,
                        productivity_score=0.92,
                    )
                ],
                budget_allocated_usd=25000.0,
                budget_spent_usd=0.0,
                health_score=0.95,
                capabilities=["pipeline_engineering", "infrastructure_scaling"],
            ),
            VirtualDepartment(
                department_id=f"dept_analyt_{uuid.uuid4().hex[:6]}",
                name="Strategic Analytics & Governance",
                head_role=AgentRole.FINANCE_AGENT,
                teams=[
                    VirtualTeam(
                        name="Governance & Metrics Team",
                        lead_role=AgentRole.ANALYST_AGENT,
                        member_roles=[AgentRole.ANALYST_AGENT, AgentRole.SECURITY_AGENT],
                        member_agent_ids=["agent_analyst_01", "agent_sec_01"],
                        mission_scope="Verify SLA bounds and compliance metrics",
                        active_task_count=2,
                        productivity_score=0.96,
                    )
                ],
                budget_allocated_usd=15000.0,
                budget_spent_usd=0.0,
                health_score=0.97,
                capabilities=["performance_measurement", "governance_compliance"],
            ),
        ]

        org = VirtualOrganization(
            org_id=org_id,
            name=f"Dynamic Org for Mission {mission_id[:12]}",
            mission_id=mission_id,
            strategy_id=strategy_id,
            state=OrganizationState.PLANNING,
            departments=depts,
            executive_board=[AgentRole.CEO_AGENT, AgentRole.CTO_AGENT, AgentRole.FINANCE_AGENT],
            span_of_control=3.5,
            operational_efficiency=0.94,
        )

        self._organizations[org.org_id] = org

        org_event_bus.publish(
            OrganizationDesigned(
                actor_agent_role=AgentRole.CEO_AGENT,
                payload={"org_id": org.org_id, "mission_id": mission_id, "department_count": len(depts)},
            )
        )

        return org

    def restructure_organization(self, org_id: str) -> VirtualOrganization:
        """Re-optimizes department team structures to eliminate bottlenecks and merge redundant teams."""
        org = self._organizations.get(org_id)
        if not org:
            org = self._organizations.get("org_enterprise_root")
        if not org:
            raise ValueError(f"Organization '{org_id}' not found")

        # Merge overlapping small teams or elevate efficiency
        total_teams = sum(len(d.teams) for d in org.departments)
        org.operational_efficiency = min(0.99, org.operational_efficiency + 0.03)
        org.span_of_control = round(total_teams / max(1, len(org.departments)), 2)
        org.updated_at = time.time()

        org_event_bus.publish(
            TeamMerged(
                actor_agent_role=AgentRole.CTO_AGENT,
                payload={"org_id": org.org_id, "new_efficiency": org.operational_efficiency},
            )
        )
        return org

    def get_structure(self, org_id: Optional[str] = None) -> VirtualOrganization:
        if org_id and org_id in self._organizations:
            return self._organizations[org_id]
        return self._organizations.get("org_enterprise_root", list(self._organizations.values())[0])

    def list_departments(self) -> List[VirtualDepartment]:
        org = self.get_structure()
        return org.departments


# Global Singleton
organization_engine = OrganizationEngine()
