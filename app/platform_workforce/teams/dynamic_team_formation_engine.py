"""
3. Dynamic Team Formation Engine Subsystem
"""
from typing import Dict, List
from app.platform_workforce.models.schemas import DynamicTeam, EmployeeStatus
from app.platform_workforce.registry.workforce_registry import workforce_registry

class DynamicTeamFormationEngine:
    def __init__(self):
        self._teams: Dict[str, Dict[str, DynamicTeam]] = {}
        self._seed_default_teams()

    def _seed_default_teams(self):
        tenant = "default-tenant"
        teams = [
            DynamicTeam(
                id="team-hyper-extract",
                team_name="Hyper-Scale Extraction Force",
                mission="Parse high-throughput enterprise invoices with 99.9% verification",
                team_lead_id="emp-eng-mgr",
                member_ids=["emp-eng-mgr", "emp-doc-spec-01", "emp-qa-rev-01"],
                required_skills=["Document Extraction", "OCR Verification", "Automated Validation"],
                max_budget_usd=100.0,
                sla_hours=4.0,
                active_tasks=["task-inv-001", "task-inv-002"],
                team_health_score=0.98
            )
        ]
        self._teams[tenant] = {t.id: t for t in teams}

    def get_teams(self, tenant_id: str = "default-tenant") -> List[DynamicTeam]:
        return list(self._teams.get(tenant_id, {}).values())

    def form_dynamic_team(
        self,
        team_name: str,
        mission: str,
        required_skills: List[str],
        max_budget_usd: float = 200.0,
        sla_hours: float = 12.0,
        tenant_id: str = "default-tenant"
    ) -> DynamicTeam:
        available_employees = workforce_registry.get_employees(tenant_id)
        
        # Rank employees by skill match and trust
        scored_employees = []
        for emp in available_employees:
            if emp.availability_status in [EmployeeStatus.ACTIVE, EmployeeStatus.STANDBY]:
                matched_skills = set(emp.skills).intersection(set(required_skills))
                match_score = len(matched_skills) * 2.0 + emp.trust_score
                scored_employees.append((match_score, emp))
        
        scored_employees.sort(key=lambda x: x[0], reverse=True)
        selected_members = [emp for _, emp in scored_employees[:3]]
        
        if not selected_members:
            selected_members = available_employees[:2]
            
        lead_id = selected_members[0].id if selected_members else "emp-eng-mgr"
        member_ids = [m.id for m in selected_members]
        
        new_team = DynamicTeam(
            tenant_id=tenant_id,
            team_name=team_name,
            mission=mission,
            team_lead_id=lead_id,
            member_ids=member_ids,
            required_skills=required_skills,
            max_budget_usd=max_budget_usd,
            sla_hours=sla_hours,
            team_health_score=0.95
        )
        if tenant_id not in self._teams:
            self._teams[tenant_id] = {}
        self._teams[tenant_id][new_team.id] = new_team
        return new_team

dynamic_team_formation_engine = DynamicTeamFormationEngine()
