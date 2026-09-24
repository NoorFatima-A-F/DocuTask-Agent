"""
Phase 13.19: Multi-Tenant Workspace & Project Manager.
Handles scoped workspaces, project namespaces, and resource quotas.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
import uuid
from app.platform_saas.models.schemas import Workspace, Project


class WorkspaceManager:
    def __init__(self):
        self._workspaces: Dict[str, Workspace] = {}
        self._projects: Dict[str, Project] = {}
        self._seed_default_workspaces()

    def _seed_default_workspaces(self) -> None:
        w1 = Workspace(
            workspace_id="ws_acme_invoicing",
            tenant_id="tenant_acme_corp",
            organization_id="org_acme_americas",
            name="Invoice Automation Production",
            slug="invoice-auto-prod",
            owner_email="analyst@acmecorp.com",
            allocated_agents_count=25,
            allocated_storage_gb=100,
        )
        w2 = Workspace(
            workspace_id="ws_acme_claims",
            tenant_id="tenant_acme_corp",
            organization_id="org_acme_emea",
            name="EMEA Insurance Claims Processing",
            slug="emea-claims",
            owner_email="emea-admin@acmecorp.com",
            allocated_agents_count=15,
            allocated_storage_gb=50,
        )
        w3 = Workspace(
            workspace_id="ws_globex_records",
            tenant_id="tenant_globex_health",
            organization_id="org_globex_clinical",
            name="Patient Records Extraction",
            slug="patient-records-extract",
            owner_email="compliance@globexhealth.com",
            allocated_agents_count=20,
            allocated_storage_gb=200,
        )

        for ws in [w1, w2, w3]:
            self._workspaces[ws.workspace_id] = ws

        p1 = Project(
            project_id="prj_acme_vendor_invoices",
            tenant_id="tenant_acme_corp",
            workspace_id="ws_acme_invoicing",
            name="Global Vendor Invoicing Pipeline",
            description="Autonomous multi-agent invoice validation and reconciliation",
            active_workflows_count=8,
        )
        p2 = Project(
            project_id="prj_globex_hipaa_ocr",
            tenant_id="tenant_globex_health",
            workspace_id="ws_globex_records",
            name="HIPAA Redaction & Extraction",
            description="Autonomous PII/PHI scrubbing and medical entity extraction",
            active_workflows_count=5,
        )

        self._projects[p1.project_id] = p1
        self._projects[p2.project_id] = p2

    def create_workspace(
        self,
        tenant_id: str,
        organization_id: str,
        name: str,
        slug: str,
        owner_email: str,
        allocated_agents_count: int = 10,
        allocated_storage_gb: int = 50,
    ) -> Workspace:
        ws_id = f"ws_{uuid.uuid4().hex[:8]}"
        ws = Workspace(
            workspace_id=ws_id,
            tenant_id=tenant_id,
            organization_id=organization_id,
            name=name,
            slug=slug,
            owner_email=owner_email,
            allocated_agents_count=allocated_agents_count,
            allocated_storage_gb=allocated_storage_gb,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._workspaces[ws_id] = ws
        return ws

    def get_workspace(self, workspace_id: str) -> Optional[Workspace]:
        return self._workspaces.get(workspace_id)

    def list_workspaces(
        self, tenant_id: Optional[str] = None, organization_id: Optional[str] = None
    ) -> List[Workspace]:
        items = list(self._workspaces.values())
        if tenant_id:
            items = [w for w in items if w.tenant_id == tenant_id]
        if organization_id:
            items = [w for w in items if w.organization_id == organization_id]
        return items

    def create_project(
        self,
        tenant_id: str,
        workspace_id: str,
        name: str,
        description: str = "",
    ) -> Project:
        prj_id = f"prj_{uuid.uuid4().hex[:8]}"
        prj = Project(
            project_id=prj_id,
            tenant_id=tenant_id,
            workspace_id=workspace_id,
            name=name,
            description=description,
            active_workflows_count=0,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._projects[prj_id] = prj
        return prj

    def list_projects(
        self, tenant_id: Optional[str] = None, workspace_id: Optional[str] = None
    ) -> List[Project]:
        items = list(self._projects.values())
        if tenant_id:
            items = [p for p in items if p.tenant_id == tenant_id]
        if workspace_id:
            items = [p for p in items if p.workspace_id == workspace_id]
        return items
