"""SaaS Multi-Tenancy REST API Router (ESP-MOOS)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.tenancy.core.models import (
    SubscriptionTier,
    Region,
)
from app.tenancy.organizations.manager import OrganizationManager
from app.tenancy.workspaces.manager import WorkspaceManager
from app.tenancy.quotas.manager import QuotaManager
from app.tenancy.metering.engine import UsageMeteringPlatform
from app.tenancy.subscriptions.engine import SubscriptionEngine
from app.tenancy.context.context import get_current_tenant_context

router = APIRouter(prefix="/api/v1/saas", tags=["SaaS Multi-Tenancy"])


class CreateOrgRequest(BaseModel):
    id: str
    name: str
    owner_id: str
    industry: str = "Technology"
    region: Region = Region.US_EAST
    subscription_plan: SubscriptionTier = SubscriptionTier.FREE


class CreateWorkspaceRequest(BaseModel):
    workspace_id: str
    name: str
    description: str = ""
    department: str = "General"


def create_saas_router(
    org_manager: OrganizationManager,
    workspace_manager: WorkspaceManager,
    quota_manager: QuotaManager,
    metering_platform: UsageMeteringPlatform,
    subscription_engine: SubscriptionEngine,
) -> APIRouter:
    """Factory to construct SaaS router with dependency injections."""

    @router.post("/organizations")
    def create_organization(req: CreateOrgRequest):
        org = org_manager.create_organization(
            org_id=req.id,
            name=req.name,
            owner_id=req.owner_id,
            industry=req.industry,
            region=req.region,
            subscription_plan=req.subscription_plan,
        )
        return {"status": "SUCCESS", "organization": org}

    @router.get("/organizations/{org_id}")
    def get_organization(org_id: str):
        try:
            org = org_manager.get_organization(org_id)
            return {"organization": org}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    @router.post("/workspaces")
    def create_workspace(req: CreateWorkspaceRequest):
        ctx = get_current_tenant_context()
        if not ctx:
            raise HTTPException(status_code=400, detail="Tenant context missing")

        ws = workspace_manager.create_workspace(
            workspace_id=req.workspace_id,
            organization_id=ctx.organization_id,
            name=req.name,
            description=req.description,
            department=req.department,
        )
        return {"status": "SUCCESS", "workspace": ws}

    @router.get("/workspaces")
    def list_workspaces():
        ctx = get_current_tenant_context()
        if not ctx:
            raise HTTPException(status_code=400, detail="Tenant context missing")
        return {"workspaces": workspace_manager.list_workspaces(ctx.organization_id)}

    @router.get("/usage")
    def get_usage():
        ctx = get_current_tenant_context()
        if not ctx:
            raise HTTPException(status_code=400, detail="Tenant context missing")
        return {
            "organization_id": ctx.organization_id,
            "total_spend_usd": metering_platform.get_total_spend(ctx.organization_id),
            "usage": metering_platform.get_usage_summary(ctx.organization_id),
        }

    @router.get("/subscription")
    def get_subscription():
        ctx = get_current_tenant_context()
        if not ctx:
            raise HTTPException(status_code=400, detail="Tenant context missing")
        return {"subscription": subscription_engine.get_subscription(ctx.organization_id)}

    @router.get("/quotas")
    def get_quotas():
        ctx = get_current_tenant_context()
        if not ctx:
            raise HTTPException(status_code=400, detail="Tenant context missing")
        return {"quotas": quota_manager.list_quotas(ctx.organization_id)}

    return router
