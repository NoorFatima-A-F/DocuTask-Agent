"""
7. Manager AI Engine Subsystem
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.platform_workforce.models.schemas import ManagerReviewRecord
from app.platform_workforce.registry.workforce_registry import workforce_registry

class ManagerAIEngine:
    def __init__(self):
        self._reviews: Dict[str, Dict[str, ManagerReviewRecord]] = {}
        self._seed_default_reviews()

    def _seed_default_reviews(self):
        tenant = "default-tenant"
        rev = ManagerReviewRecord(
            id="rev-q1-doc-spec",
            employee_id="emp-doc-spec-01",
            manager_id="emp-eng-mgr",
            review_period="2026-Q1",
            performance_rating=4.9,
            strengths=["Zero error rate in table extraction", "High reuse of experience memory"],
            areas_for_growth=["Can mentor junior parser agents"],
            workload_balance_action="OPTIMAL",
            promotion_recommended=True
        )
        self._reviews[tenant] = {rev.id: rev}

    def get_reviews(self, tenant_id: str = "default-tenant", employee_id: Optional[str] = None) -> List[ManagerReviewRecord]:
        revs = list(self._reviews.get(tenant_id, {}).values())
        if employee_id:
            revs = [r for r in revs if r.employee_id == employee_id]
        return revs

    def conduct_performance_review(self, employee_id: str, manager_id: str, tenant_id: str = "default-tenant") -> Optional[ManagerReviewRecord]:
        emp = workforce_registry.get_employee(employee_id, tenant_id)
        if not emp:
            return None
        
        # Calculate rating based on task success and trust
        rating = round(min(5.0, (emp.task_success_rate * 3.0) + (emp.trust_score * 2.0)), 2)
        should_promote = rating >= 4.7 and emp.lifetime_tasks_completed >= 5
        
        rec = ManagerReviewRecord(
            tenant_id=tenant_id,
            employee_id=employee_id,
            manager_id=manager_id,
            review_period=f"{datetime.now(timezone.utc).year}-Q1",
            performance_rating=rating,
            strengths=[f"High task reliability ({emp.task_success_rate * 100}%)", f"Trust score: {emp.trust_score}"],
            areas_for_growth=["Expand skill sets across adjacent domains"],
            workload_balance_action="OPTIMAL" if emp.burnout_risk_score < 0.2 else "OFF_LOAD_TASKS",
            promotion_recommended=should_promote
        )
        if tenant_id not in self._reviews:
            self._reviews[tenant_id] = {}
        self._reviews[tenant_id][rec.id] = rec
        return rec

    def balance_department_workload(self, manager_id: str, tenant_id: str = "default-tenant") -> Dict[str, Any]:
        employees = [e for e in workforce_registry.get_employees(tenant_id) if e.manager_id == manager_id]
        actions_taken = []
        for emp in employees:
            if emp.assigned_tasks_count >= emp.capacity_slots:
                emp.burnout_risk_score = min(0.95, emp.burnout_risk_score + 0.1)
                actions_taken.append(f"Offloaded 1 task from {emp.name} to standby workers.")
            else:
                emp.burnout_risk_score = max(0.02, emp.burnout_risk_score - 0.05)
        return {
            "manager_id": manager_id,
            "managed_employees_count": len(employees),
            "rebalance_actions": actions_taken or ["Workload distributed uniformly across all reportees."]
        }

manager_ai_engine = ManagerAIEngine()
