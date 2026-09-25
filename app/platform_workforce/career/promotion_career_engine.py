"""
12. Promotion & Career Engine Subsystem
"""
from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.platform_workforce.models.schemas import CareerPromotionPath, EmployeeRole
from app.platform_workforce.registry.workforce_registry import workforce_registry

class PromotionCareerEngine:
    def __init__(self):
        self._career_paths: Dict[str, Dict[str, CareerPromotionPath]] = {}
        self._seed_default_career_paths()

    def _seed_default_career_paths(self):
        tenant = "default-tenant"
        promo = CareerPromotionPath(
            id="promo-doc-spec-lead",
            employee_id="emp-doc-spec-01",
            current_role=EmployeeRole.SENIOR_SPECIALIST,
            target_role=EmployeeRole.LEAD_SPECIALIST,
            eligibility_score=0.96,
            completed_milestones=[
                "Completed 100+ flawless extractions",
                "Authored 5 collective memory best practices",
                "Maintained >98% trust score"
            ],
            status="READY"
        )
        self._career_paths[tenant] = {promo.id: promo}

    def get_career_paths(self, tenant_id: str = "default-tenant") -> List[CareerPromotionPath]:
        return list(self._career_paths.get(tenant_id, {}).values())

    def evaluate_promotion(self, employee_id: str, tenant_id: str = "default-tenant") -> Optional[CareerPromotionPath]:
        emp = workforce_registry.get_employee(employee_id, tenant_id)
        if not emp:
            return None
        
        # Determine next role
        role_ladder = [
            EmployeeRole.JUNIOR_WORKER,
            EmployeeRole.ASSOCIATE_SPECIALIST,
            EmployeeRole.SENIOR_SPECIALIST,
            EmployeeRole.LEAD_SPECIALIST,
            EmployeeRole.PRINCIPAL_ARCHITECT,
            EmployeeRole.MANAGER,
            EmployeeRole.DIRECTOR,
            EmployeeRole.VP,
            EmployeeRole.CEO
        ]
        curr_idx = 0
        for i, r in enumerate(role_ladder):
            if r == emp.role:
                curr_idx = i
                break
        next_role = role_ladder[min(curr_idx + 1, len(role_ladder) - 1)]
        
        path = CareerPromotionPath(
            tenant_id=tenant_id,
            employee_id=employee_id,
            current_role=emp.role,
            target_role=next_role,
            eligibility_score=round(emp.trust_score * 0.95 + emp.task_success_rate * 0.05, 2),
            completed_milestones=[f"Executed {emp.lifetime_tasks_completed} tasks", f"Trust rating: {emp.trust_score}"],
            status="READY" if emp.trust_score >= 0.95 else "IN_PROGRESS"
        )
        if tenant_id not in self._career_paths:
            self._career_paths[tenant_id] = {}
        self._career_paths[tenant_id][path.id] = path
        return path

    def execute_promotion(self, promotion_path_id: str, tenant_id: str = "default-tenant") -> Optional[CareerPromotionPath]:
        path = self._career_paths.get(tenant_id, {}).get(promotion_path_id)
        if not path:
            return None
        emp = workforce_registry.get_employee(path.employee_id, tenant_id)
        if emp:
            emp.role = path.target_role
            emp.level += 1
            emp.hourly_salary_usd = round(emp.hourly_salary_usd * 1.25, 2)
            emp.career_history.append({
                "promoted_to": str(path.target_role),
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        path.status = "PROMOTED"
        path.promoted_at = datetime.now(timezone.utc)
        return path

promotion_career_engine = PromotionCareerEngine()
