"""
11. Autonomous Hiring Engine Subsystem
"""
from typing import Dict, List, Optional
from app.platform_workforce.models.schemas import HiringRequisition, DigitalEmployee, EmployeeRole, DepartmentType
from app.platform_workforce.registry.workforce_registry import workforce_registry

class AutonomousHiringEngine:
    def __init__(self):
        self._requisitions: Dict[str, Dict[str, HiringRequisition]] = {}
        self._seed_default_requisitions()

    def _seed_default_requisitions(self):
        tenant = "default-tenant"
        req = HiringRequisition(
            id="req-auto-scale-01",
            department=DepartmentType.ENGINEERING,
            target_role=EmployeeRole.SENIOR_SPECIALIST,
            required_skills=["High-Throughput Streaming", "FastAPI Concurrency", "Vector Sharding"],
            reason="High Queue Backlog on Distributed Ingestion",
            status="APPROVED",
            candidate_profiles=[
                {"name": "StreamRunner Delta", "score": 0.96, "suggested_salary": 2.80},
                {"name": "AsyncIO Vector Bot", "score": 0.92, "suggested_salary": 2.40}
            ]
        )
        self._requisitions[tenant] = {req.id: req}

    def get_requisitions(self, tenant_id: str = "default-tenant") -> List[HiringRequisition]:
        return list(self._requisitions.get(tenant_id, {}).values())

    def create_requisition(self, department: DepartmentType, target_role: EmployeeRole, skills: List[str], reason: str = "CAPACITY_EXPANSION", tenant_id: str = "default-tenant") -> HiringRequisition:
        req = HiringRequisition(
            tenant_id=tenant_id,
            department=department,
            target_role=target_role,
            required_skills=skills,
            reason=reason,
            status="APPROVED",
            candidate_profiles=[
                {"name": f"Agent-{skills[0] if skills else 'Worker'}-Auto", "score": 0.95, "suggested_salary": 2.50}
            ]
        )
        if tenant_id not in self._requisitions:
            self._requisitions[tenant_id] = {}
        self._requisitions[tenant_id][req.id] = req
        return req

    def hire_candidate(self, requisition_id: str, candidate_name: str, tenant_id: str = "default-tenant") -> Optional[DigitalEmployee]:
        req = self._requisitions.get(tenant_id, {}).get(requisition_id)
        if not req:
            return None
        new_emp = DigitalEmployee(
            tenant_id=tenant_id,
            name=candidate_name,
            role=req.target_role,
            department=req.department,
            skills=req.required_skills,
            hourly_salary_usd=2.50,
            trust_score=0.95
        )
        workforce_registry.register_employee(new_emp)
        req.status = "FILLED"
        req.hired_employee_id = new_emp.id
        return new_emp

autonomous_hiring_engine = AutonomousHiringEngine()
