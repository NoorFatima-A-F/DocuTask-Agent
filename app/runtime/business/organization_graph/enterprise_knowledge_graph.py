"""
Phase 13.19: Enterprise Organizational Knowledge Graph.
Models departments, roles, approval hierarchies, and enterprise IT systems.
"""

from typing import Dict, List, Optional, Any
from app.runtime.business.models.schemas import (
    Department,
    EmployeeOrAgentRole,
    EnterpriseSystem,
    OrganizationGraph,
)


class EnterpriseKnowledgeGraph:
    def __init__(self):
        self._graph = OrganizationGraph()
        self._seed_default_org()

    def _seed_default_org(self) -> None:
        """Seeds enterprise organizational ontology."""
        self._graph.departments = [
            Department(
                department_id="dept_exec",
                name="Executive Leadership",
                head_role="role_ceo",
                members_count=5,
                active_processes_count=2,
                operational_budget_monthly=150000.0,
            ),
            Department(
                department_id="dept_finance",
                name="Finance & Accounts Payable",
                head_role="role_cfo",
                parent_department_id="dept_exec",
                members_count=28,
                active_processes_count=8,
                operational_budget_monthly=85000.0,
            ),
            Department(
                department_id="dept_legal",
                name="Legal & Compliance",
                head_role="role_general_counsel",
                parent_department_id="dept_exec",
                members_count=12,
                active_processes_count=5,
                operational_budget_monthly=60000.0,
            ),
            Department(
                department_id="dept_ops",
                name="Global Operations & Supply Chain",
                head_role="role_coo",
                parent_department_id="dept_exec",
                members_count=45,
                active_processes_count=12,
                operational_budget_monthly=110000.0,
            ),
        ]

        self._graph.roles = [
            EmployeeOrAgentRole(
                role_id="role_finance_director",
                title="Finance Director",
                department_id="dept_finance",
                is_autonomous_agent=False,
                approval_limit_amount=100000.0,
                assigned_capabilities=["invoice_approval", "budget_allocation", "tax_signoff"],
            ),
            EmployeeOrAgentRole(
                role_id="role_ap_specialist",
                title="Accounts Payable Specialist (AI Agent)",
                department_id="dept_finance",
                is_autonomous_agent=True,
                approval_limit_amount=5000.0,
                assigned_capabilities=["ocr_data_entry", "line_item_matching", "vendor_lookup"],
            ),
            EmployeeOrAgentRole(
                role_id="role_compliance_officer",
                title="Chief Compliance Officer",
                department_id="dept_legal",
                is_autonomous_agent=False,
                approval_limit_amount=500000.0,
                assigned_capabilities=["contract_signoff", "regulatory_audit", "sla_governance"],
            ),
        ]

        self._graph.systems = [
            EnterpriseSystem(
                system_id="sys_sap_erp",
                name="SAP S/4HANA Enterprise ERP",
                system_type="ERP",
                status="ONLINE",
                connected_departments=["dept_finance", "dept_ops"],
            ),
            EnterpriseSystem(
                system_id="sys_salesforce",
                name="Salesforce Enterprise CRM",
                system_type="CRM",
                status="ONLINE",
                connected_departments=["dept_ops", "dept_exec"],
            ),
            EnterpriseSystem(
                system_id="sys_workday",
                name="Workday Enterprise HRIS",
                system_type="HRIS",
                status="ONLINE",
                connected_departments=["dept_exec", "dept_finance"],
            ),
        ]

        self._graph.approval_matrix = {
            "role_ap_specialist": "role_finance_director",
            "role_finance_director": "role_cfo",
            "role_compliance_officer": "role_general_counsel",
        }

    def get_organization_graph(self) -> OrganizationGraph:
        return self._graph

    def get_department(self, department_id: str) -> Optional[Department]:
        return next((d for d in self._graph.departments if d.department_id == department_id), None)

    def find_approver_for_amount(self, department_id: str, amount: float) -> Optional[EmployeeOrAgentRole]:
        """Traverses role hierarchy to find the appropriate approver for a financial threshold."""
        dept_roles = [r for r in self._graph.roles if r.department_id == department_id]
        sorted_roles = sorted(dept_roles, key=lambda r: r.approval_limit_amount)
        for role in sorted_roles:
            if role.approval_limit_amount >= amount:
                return role
        # fallback to the highest role
        return sorted_roles[-1] if sorted_roles else None

    def add_department(self, dept: Department) -> Department:
        self._graph.departments.append(dept)
        return dept

    def add_role(self, role: EmployeeOrAgentRole) -> EmployeeOrAgentRole:
        self._graph.roles.append(role)
        return role
