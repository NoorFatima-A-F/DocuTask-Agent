"""
Phase 13.19: Multi-Level Organization Hierarchy Service.
Manages Tenant -> Organization -> Business Unit / Department Tree structures.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid
from app.platform_saas.models.schemas import OrganizationNode


class OrganizationHierarchyService:
    def __init__(self):
        self._organizations: Dict[str, OrganizationNode] = {}
        self._seed_default_orgs()

    def _seed_default_orgs(self) -> None:
        o1 = OrganizationNode(
            organization_id="org_acme_americas",
            tenant_id="tenant_acme_corp",
            name="Acme Americas Division",
            parent_org_id=None,
            business_unit="Americas Enterprise Operations",
            country_code="US",
        )
        o2 = OrganizationNode(
            organization_id="org_acme_emea",
            tenant_id="tenant_acme_corp",
            name="Acme EMEA Division",
            parent_org_id=None,
            business_unit="EMEA Regional Operations",
            country_code="GB",
        )
        o3 = OrganizationNode(
            organization_id="org_acme_amer_rd",
            tenant_id="tenant_acme_corp",
            name="Acme Americas R&D Lab",
            parent_org_id="org_acme_americas",
            business_unit="Advanced AI Research",
            country_code="US",
        )
        o4 = OrganizationNode(
            organization_id="org_globex_clinical",
            tenant_id="tenant_globex_health",
            name="Globex Clinical Operations",
            parent_org_id=None,
            business_unit="Clinical Document Processing",
            country_code="CH",
        )

        for org in [o1, o2, o3, o4]:
            self._organizations[org.organization_id] = org

    def create_organization(
        self,
        tenant_id: str,
        name: str,
        business_unit: str = "General",
        country_code: str = "US",
        parent_org_id: Optional[str] = None,
    ) -> OrganizationNode:
        org_id = f"org_{uuid.uuid4().hex[:8]}"
        org = OrganizationNode(
            organization_id=org_id,
            tenant_id=tenant_id,
            name=name,
            parent_org_id=parent_org_id,
            business_unit=business_unit,
            country_code=country_code,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._organizations[org_id] = org
        return org

    def get_organization(self, org_id: str) -> Optional[OrganizationNode]:
        return self._organizations.get(org_id)

    def list_organizations(self, tenant_id: Optional[str] = None) -> List[OrganizationNode]:
        if tenant_id:
            return [o for o in self._organizations.values() if o.tenant_id == tenant_id]
        return list(self._organizations.values())

    def get_organization_tree(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Constructs a nested tree representation of the tenant organization structure."""
        tenant_orgs = self.list_organizations(tenant_id)
        org_map = {o.organization_id: o.model_dump() for o in tenant_orgs}
        for o_dict in org_map.values():
            o_dict["children"] = []

        root_nodes = []
        for o_dict in org_map.values():
            parent_id = o_dict.get("parent_org_id")
            if parent_id and parent_id in org_map:
                org_map[parent_id]["children"].append(o_dict)
            else:
                root_nodes.append(o_dict)

        return root_nodes
