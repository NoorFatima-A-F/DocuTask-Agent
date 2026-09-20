"""
Workforce Master Orchestrator Subsystem
"""
from typing import Dict, Any
from app.platform_workforce.models.schemas import OrganizationOverviewReport
from app.platform_workforce.registry.workforce_registry import workforce_registry
from app.platform_workforce.hierarchy.organization_hierarchy_engine import organization_hierarchy_engine
from app.platform_workforce.teams.dynamic_team_formation_engine import dynamic_team_formation_engine
from app.platform_workforce.marketplace.task_marketplace import task_marketplace
from app.platform_workforce.council.executive_council_engine import executive_council_engine

class WorkforceMasterOrchestrator:
    def get_organization_overview(self, tenant_id: str = "default-tenant") -> OrganizationOverviewReport:
        employees = workforce_registry.get_employees(tenant_id)
        departments = organization_hierarchy_engine.get_departments(tenant_id)
        teams = dynamic_team_formation_engine.get_teams(tenant_id)
        open_tasks = len(task_marketplace.get_tasks(tenant_id, status="OPEN"))
        active_props = len(executive_council_engine.get_propositions(tenant_id))
        
        avg_trust = sum(e.trust_score for e in employees) / max(len(employees), 1)
        
        return OrganizationOverviewReport(
            tenant_id=tenant_id,
            total_employees=len(employees),
            total_departments=len(departments),
            active_teams=len(teams),
            marketplace_open_tasks=open_tasks,
            council_active_propositions=active_props,
            average_trust_score=round(avg_trust, 3),
            workforce_readiness_index=0.96
        )

workforce_master_orchestrator = WorkforceMasterOrchestrator()
