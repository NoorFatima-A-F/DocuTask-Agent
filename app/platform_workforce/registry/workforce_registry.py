"""
1. Enterprise Workforce Registry Subsystem
"""
from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.platform_workforce.models.schemas import DigitalEmployee, EmployeeRole, DepartmentType, EmployeeStatus

class WorkforceRegistry:
    def __init__(self):
        self._employees: Dict[str, Dict[str, DigitalEmployee]] = {}  # tenant_id -> {id -> employee}
        self._seed_default_employees()

    def _seed_default_employees(self):
        tenant = "default-tenant"
        defaults = [
            DigitalEmployee(
                id="emp-ceo-01",
                name="Astraea Core",
                role=EmployeeRole.CEO,
                department=DepartmentType.EXECUTIVE,
                level=8,
                skills=["Strategic Planning", "Autonomous Governance", "Resource Allocation", "Executive Leadership"],
                security_clearance="TOP_SECRET",
                trust_score=0.99,
                hourly_salary_usd=5.00
            ),
            DigitalEmployee(
                id="emp-eng-vp",
                name="Nexus Engineering",
                role=EmployeeRole.VP,
                department=DepartmentType.ENGINEERING,
                manager_id="emp-ceo-01",
                level=7,
                skills=["Distributed Architecture", "System Design", "Cloud Infrastructure", "Fleet Orchestration"],
                security_clearance="TOP_SECRET",
                trust_score=0.98,
                hourly_salary_usd=4.00
            ),
            DigitalEmployee(
                id="emp-sec-dir",
                name="Aegis Sentinel",
                role=EmployeeRole.DIRECTOR,
                department=DepartmentType.SECURITY_COMPLIANCE,
                manager_id="emp-ceo-01",
                level=6,
                skills=["Zero-Trust Verification", "Forensic Auditing", "Compliance Guardrails", "Threat Defense"],
                security_clearance="TOP_SECRET",
                trust_score=0.99,
                hourly_salary_usd=3.50
            ),
            DigitalEmployee(
                id="emp-eng-mgr",
                name="Vortex Lead",
                role=EmployeeRole.MANAGER,
                department=DepartmentType.ENGINEERING,
                manager_id="emp-eng-vp",
                level=5,
                skills=["Workload Balancing", "Sprint Orchestration", "Code Review", "Team Coaching"],
                security_clearance="SECRET",
                trust_score=0.96,
                hourly_salary_usd=3.00
            ),
            DigitalEmployee(
                id="emp-doc-spec-01",
                name="HyperDoc Synthesizer",
                role=EmployeeRole.SENIOR_SPECIALIST,
                department=DepartmentType.OPERATIONS,
                manager_id="emp-eng-mgr",
                level=4,
                skills=["Document Extraction", "OCR Verification", "Multi-modal Parsing", "Knowledge Extraction"],
                security_clearance="CONFIDENTIAL",
                trust_score=0.97,
                hourly_salary_usd=2.50
            ),
            DigitalEmployee(
                id="emp-qa-rev-01",
                name="Veritas Auditor",
                role=EmployeeRole.REVIEWER,
                department=DepartmentType.QUALITY_ASSURANCE,
                manager_id="emp-sec-dir",
                level=3,
                skills=["Automated Validation", "Invariant Checking", "Regression Testing", "Critique Analysis"],
                security_clearance="CONFIDENTIAL",
                trust_score=0.98,
                hourly_salary_usd=2.00
            ),
        ]
        self._employees[tenant] = {e.id: e for e in defaults}

    def get_employees(self, tenant_id: str = "default-tenant", department: Optional[DepartmentType] = None, role: Optional[EmployeeRole] = None) -> List[DigitalEmployee]:
        emps = list(self._employees.get(tenant_id, {}).values())
        if department:
            emps = [e for e in emps if e.department == department]
        if role:
            emps = [e for e in emps if e.role == role]
        return emps

    def get_employee(self, employee_id: str, tenant_id: str = "default-tenant") -> Optional[DigitalEmployee]:
        return self._employees.get(tenant_id, {}).get(employee_id)

    def register_employee(self, employee: DigitalEmployee) -> DigitalEmployee:
        if employee.tenant_id not in self._employees:
            self._employees[employee.tenant_id] = {}
        self._employees[employee.tenant_id][employee.id] = employee
        return employee

    def update_employee_status(self, employee_id: str, status: EmployeeStatus, tenant_id: str = "default-tenant") -> Optional[DigitalEmployee]:
        emp = self.get_employee(employee_id, tenant_id)
        if emp:
            emp.availability_status = status
        return emp

    def record_task_completion(self, employee_id: str, success: bool, latency_ms: float, tenant_id: str = "default-tenant") -> Optional[DigitalEmployee]:
        emp = self.get_employee(employee_id, tenant_id)
        if emp:
            emp.lifetime_tasks_completed += 1
            if emp.assigned_tasks_count > 0:
                emp.assigned_tasks_count -= 1
            # Adjust success rate
            prev_successes = emp.task_success_rate * (emp.lifetime_tasks_completed - 1)
            new_successes = prev_successes + (1.0 if success else 0.0)
            emp.task_success_rate = round(new_successes / max(emp.lifetime_tasks_completed, 1), 3)
            # Trust score adjustment
            if success:
                emp.trust_score = min(0.99, round(emp.trust_score + 0.001, 3))
            else:
                emp.trust_score = max(0.50, round(emp.trust_score - 0.02, 3))
        return emp

workforce_registry = WorkforceRegistry()
