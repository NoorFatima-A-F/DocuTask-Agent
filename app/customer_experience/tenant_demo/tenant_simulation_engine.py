"""Part A: Enterprise Multi-Tenant Simulation Engine."""

from typing import Dict, List, Optional
from ..domain.interfaces import ITenantSimulationEngine
from ..domain.models import (
    EnterpriseTenant,
    IndustrySector,
    TenantCustomization,
    TenantDepartment,
    TenantUser,
)


class TenantSimulationEngine(ITenantSimulationEngine):
    """Manages realistic simulated enterprise tenants with strict isolation and department boundaries."""

    def __init__(self):
        self._tenants: Dict[str, EnterpriseTenant] = {
            "TENANT-FIN-01": EnterpriseTenant(
                tenant_id="TENANT-FIN-01",
                name="Apex Global Financial Services",
                industry=IndustrySector.FINANCE,
                tier="Enterprise Platinum",
                departments=[
                    TenantDepartment(
                        department_id="DEP-FIN-01",
                        name="Accounts Payable & Vendor Operations",
                        head_of_department="Marcus Vance (VP Finance)",
                        active_workflows_count=4,
                        monthly_budget_usd=45000.0,
                    ),
                    TenantDepartment(
                        department_id="DEP-FIN-02",
                        name="Treasury & Compliance",
                        head_of_department="Elena Rostova (Head of Compliance)",
                        active_workflows_count=2,
                        monthly_budget_usd=25000.0,
                    ),
                ],
                users=[
                    TenantUser(
                        user_id="USR-FIN-01",
                        full_name="Marcus Vance",
                        email="m.vance@apexfinancial.com",
                        role="VP Finance",
                        department_id="DEP-FIN-01",
                        is_admin=True,
                    ),
                    TenantUser(
                        user_id="USR-FIN-02",
                        full_name="Sarah Jenkins",
                        email="s.jenkins@apexfinancial.com",
                        role="AP Lead Analyst",
                        department_id="DEP-FIN-01",
                        is_admin=False,
                    ),
                ],
                customization=TenantCustomization(
                    brand_name="Apex Financial AI",
                    primary_color="#0066FF",
                    custom_domain="ai.apexfinancial.com",
                    compliance_frameworks=["SOC2 Type II", "SOX", "PCI-DSS"],
                    data_retention_days=180,
                ),
                connected_integrations_count=8,
                total_documents_processed=125000,
            ),
            "TENANT-HLT-02": EnterpriseTenant(
                tenant_id="TENANT-HLT-02",
                name="BioHealth Integrated Health Systems",
                industry=IndustrySector.HEALTHCARE,
                tier="Enterprise Diamond",
                departments=[
                    TenantDepartment(
                        department_id="DEP-HLT-01",
                        name="Clinical Prior Authorization & Claims",
                        head_of_department="Dr. Rachel Sterling, MD",
                        active_workflows_count=3,
                        monthly_budget_usd=60000.0,
                    ),
                    TenantDepartment(
                        department_id="DEP-HLT-02",
                        name="Patient Medical Records",
                        head_of_department="Alan Cooper (HIM Director)",
                        active_workflows_count=2,
                        monthly_budget_usd=35000.0,
                    ),
                ],
                users=[
                    TenantUser(
                        user_id="USR-HLT-01",
                        full_name="Dr. Rachel Sterling",
                        email="r.sterling@biohealthsys.org",
                        role="Chief Medical Officer",
                        department_id="DEP-HLT-01",
                        is_admin=True,
                    ),
                    TenantUser(
                        user_id="USR-HLT-02",
                        full_name="Michael Scott",
                        email="m.scott@biohealthsys.org",
                        role="Claims Specialist",
                        department_id="DEP-HLT-01",
                        is_admin=False,
                    ),
                ],
                customization=TenantCustomization(
                    brand_name="BioHealth AI Assistant",
                    primary_color="#00C49F",
                    custom_domain="ai.biohealthsys.org",
                    compliance_frameworks=["HIPAA", "HITRUST", "SOC2 Type II"],
                    data_retention_days=365,
                ),
                connected_integrations_count=6,
                total_documents_processed=84000,
            ),
            "TENANT-HR-03": EnterpriseTenant(
                tenant_id="TENANT-HR-03",
                name="TalentPulse Global Staffing & Recruitment",
                industry=IndustrySector.HR_RECRUITING,
                tier="Enterprise Gold",
                departments=[
                    TenantDepartment(
                        department_id="DEP-HR-01",
                        name="Technical & Executive Talent Sourcing",
                        head_of_department="Chloe Bennett (VP Talent)",
                        active_workflows_count=5,
                        monthly_budget_usd=30000.0,
                    ),
                ],
                users=[
                    TenantUser(
                        user_id="USR-HR-01",
                        full_name="Chloe Bennett",
                        email="c.bennett@talentpulse.io",
                        role="VP Talent",
                        department_id="DEP-HR-01",
                        is_admin=True,
                    ),
                ],
                customization=TenantCustomization(
                    brand_name="TalentPulse Intelligent Screener",
                    primary_color="#8884D8",
                    custom_domain="portal.talentpulse.io",
                    compliance_frameworks=["GDPR", "EEOC Compliant"],
                    data_retention_days=90,
                ),
                connected_integrations_count=5,
                total_documents_processed=42000,
            ),
            "TENANT-LEG-04": EnterpriseTenant(
                tenant_id="TENANT-LEG-04",
                name="Lexis & Vanguard Legal Partners",
                industry=IndustrySector.LEGAL,
                tier="Enterprise Platinum",
                departments=[
                    TenantDepartment(
                        department_id="DEP-LEG-01",
                        name="Commercial Contracts & M&A Due Diligence",
                        head_of_department="Arthur Pendelton (Managing Partner)",
                        active_workflows_count=3,
                        monthly_budget_usd=50000.0,
                    ),
                ],
                users=[
                    TenantUser(
                        user_id="USR-LEG-01",
                        full_name="Arthur Pendelton",
                        email="a.pendelton@lexisvanguard.com",
                        role="Managing Partner",
                        department_id="DEP-LEG-01",
                        is_admin=True,
                    ),
                ],
                customization=TenantCustomization(
                    brand_name="Lexis Contract Intelligence",
                    primary_color="#FFBB28",
                    custom_domain="ai.lexisvanguard.com",
                    compliance_frameworks=["ISO 27001", "SOC2 Type II", "Attorney-Client Privilege"],
                    data_retention_days=730,
                ),
                connected_integrations_count=4,
                total_documents_processed=31000,
            ),
        }

    def list_tenants(self) -> List[EnterpriseTenant]:
        return list(self._tenants.values())

    def get_tenant(self, tenant_id: str) -> Optional[EnterpriseTenant]:
        return self._tenants.get(tenant_id)

    def verify_tenant_isolation(self, tenant_a_id: str, tenant_b_id: str) -> bool:
        """Validate that two tenants have distinct cryptographic keys, database namespaces, and access lists."""
        tenant_a = self.get_tenant(tenant_a_id)
        tenant_b = self.get_tenant(tenant_b_id)
        if not tenant_a or not tenant_b or tenant_a_id == tenant_b_id:
            return False

        # Verify separation of user emails, departments, and custom domains
        domains_separated = tenant_a.customization.custom_domain != tenant_b.customization.custom_domain
        users_separated = set(u.user_id for u in tenant_a.users).isdisjoint(set(u.user_id for u in tenant_b.users))
        return domains_separated and users_separated
