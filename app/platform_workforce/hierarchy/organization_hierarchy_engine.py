"""
2. Organization Hierarchy Engine Subsystem
"""
from typing import Dict, List, Any
from app.platform_workforce.models.schemas import Department, DepartmentType, DigitalEmployee
from app.platform_workforce.registry.workforce_registry import workforce_registry

class OrganizationHierarchyEngine:
    def __init__(self):
        self._departments: Dict[str, Dict[str, Department]] = {}
        self._seed_default_departments()

    def _seed_default_departments(self):
        tenant = "default-tenant"
        depts = [
            Department(id="dept-exec", name="Executive Leadership", dept_type=DepartmentType.EXECUTIVE, manager_id="emp-ceo-01", headcount=1, monthly_budget_usd=25000.0, okrs=["Autonomous Enterprise Scale", "99.99% Reliability"]),
            Department(id="dept-eng", name="Autonomous Engineering", dept_type=DepartmentType.ENGINEERING, manager_id="emp-eng-vp", headcount=2, monthly_budget_usd=50000.0, okrs=["Distributed Fleet Scaling", "Sub-100ms Inference"]),
            Department(id="dept-sec", name="Security & Governance", dept_type=DepartmentType.SECURITY_COMPLIANCE, manager_id="emp-sec-dir", headcount=2, monthly_budget_usd=20000.0, okrs=["Zero Fabrication Guarantee", "SOC2/HIPAA Autonomous Auditing"]),
            Department(id="dept-ops", name="Autonomous Operations", dept_type=DepartmentType.OPERATIONS, manager_id="emp-eng-mgr", headcount=2, monthly_budget_usd=30000.0, okrs=["High Throughput Extraction", "Autonomous Process Discovery"]),
            Department(id="dept-qa", name="Quality & Verification", dept_type=DepartmentType.QUALITY_ASSURANCE, manager_id="emp-sec-dir", headcount=1, monthly_budget_usd=15000.0, okrs=["100% Test Pass Rate", "Autonomous Drift Detection"]),
        ]
        self._departments[tenant] = {d.id: d for d in depts}

    def get_departments(self, tenant_id: str = "default-tenant") -> List[Department]:
        return list(self._departments.get(tenant_id, {}).values())

    def get_organization_chart(self, tenant_id: str = "default-tenant") -> Dict[str, Any]:
        employees = workforce_registry.get_employees(tenant_id)
        emp_map = {e.id: e for e in employees}
        
        # Build hierarchy tree starting from CEO or top-level nodes (no manager or CEO)
        tree = []
        for emp in employees:
            if not emp.manager_id or emp.manager_id not in emp_map:
                tree.append(self._build_sub_tree(emp, employees))
                
        return {
            "tenant_id": tenant_id,
            "root_nodes": tree,
            "total_headcount": len(employees),
            "departments": [d.dict() for d in self.get_departments(tenant_id)]
        }

    def _build_sub_tree(self, employee: DigitalEmployee, all_employees: List[DigitalEmployee]) -> Dict[str, Any]:
        direct_reports = [e for e in all_employees if e.manager_id == employee.id]
        return {
            "employee": employee.dict(),
            "direct_reports": [self._build_sub_tree(dr, all_employees) for dr in direct_reports]
        }

organization_hierarchy_engine = OrganizationHierarchyEngine()
