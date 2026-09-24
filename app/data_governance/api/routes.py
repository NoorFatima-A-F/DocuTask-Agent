"""Data Governance REST API Router (Phase 8B)."""

from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.data_governance.registry.models import (
    AssetType,
    ClassificationLevel,
    DataOwnership,
)
from app.data_governance.registry.service import DataGovernanceRegistryService
from app.data_governance.classification.classifier import DataClassificationEngine
from app.data_governance.lineage.graph import LineageGraphEngine
from app.data_governance.provenance.history import ProvenanceHistoryEngine
from app.data_governance.catalog.search import EnterpriseDataCatalog

router = APIRouter(prefix="/api/v1/data", tags=["Data Governance"])


class RegisterAssetRequest(BaseModel):
    asset_id: str
    organization_id: str
    workspace_id: str
    name: str
    asset_type: AssetType
    source: str
    location_uri: str
    owner_id: str
    responsible_team: str = "General"
    department: str = "General"
    creator_id: str
    classification: ClassificationLevel = ClassificationLevel.INTERNAL


class ClassifyTextRequest(BaseModel):
    text: str


def create_data_governance_router(
    registry_service: DataGovernanceRegistryService,
    classifier_engine: DataClassificationEngine,
    lineage_graph: LineageGraphEngine,
    provenance_engine: ProvenanceHistoryEngine,
    catalog: EnterpriseDataCatalog,
) -> APIRouter:
    """Construct data governance API router with injected services."""

    @router.post("/assets")
    def register_asset(req: RegisterAssetRequest):
        owner = DataOwnership(
            owner_user_id=req.owner_id,
            responsible_team=req.responsible_team,
            department=req.department,
        )
        asset = registry_service.register_asset(
            asset_id=req.asset_id,
            organization_id=req.organization_id,
            workspace_id=req.workspace_id,
            name=req.name,
            asset_type=req.asset_type,
            source=req.source,
            location_uri=req.location_uri,
            owner=owner,
            creator_id=req.creator_id,
            classification=req.classification,
        )
        return {"status": "SUCCESS", "asset": asset}

    @router.get("/assets/{asset_id}")
    def get_asset(asset_id: str, organization_id: str):
        asset = registry_service.get_asset(asset_id, organization_id)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        return {"asset": asset}

    @router.post("/classify")
    def classify_text(req: ClassifyTextRequest):
        res = classifier_engine.classify_text(req.text)
        return {"result": res}

    @router.get("/assets/{asset_id}/lineage")
    def get_asset_lineage(asset_id: str):
        upstream = lineage_graph.get_upstream_lineage(asset_id)
        downstream = lineage_graph.get_downstream_lineage(asset_id)
        return {
            "asset_id": asset_id,
            "upstream_nodes": upstream,
            "downstream_nodes": downstream,
        }

    @router.get("/assets/{asset_id}/provenance")
    def get_asset_provenance(asset_id: str):
        source = provenance_engine.get_source(asset_id)
        transforms = provenance_engine.get_transformations(asset_id)
        reproducibility = provenance_engine.verify_reproducibility(asset_id)
        return {
            "source": source,
            "transformations": transforms,
            "reproducibility": reproducibility,
        }

    @router.get("/catalog/search")
    def search_catalog(organization_id: str, q: Optional[str] = None):
        results = catalog.search(organization_id=organization_id, query=q)
        return {"results": results}

    return router
